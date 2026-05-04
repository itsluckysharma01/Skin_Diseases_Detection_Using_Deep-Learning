"""
Flask web app for skin lesion classification using the EfficientNetB3 model
from the training notebook (300×300 input, 30 classes).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL = BASE_DIR / "Models(67)" / "effBb3" / "best_phase2.keras"
DEFAULT_DISEASE_INFO = BASE_DIR / "data" / "disease_info.json"

MODEL_PATH = Path(os.environ.get("SKIN_MODEL_PATH", str(DEFAULT_MODEL)))
DISEASE_INFO_PATH = Path(os.environ.get("SKIN_DISEASE_INFO_PATH", str(DEFAULT_DISEASE_INFO)))

IMG_SIZE = (300, 300)
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

_model = None
_class_names: list[str] | None = None
HINDI_LABELS = {
    "1. Eczema": "1. एक्जिमा",
    "11. Pigment": "11. पिगमेंटेशन समस्या",
    "13. Akne": "13. मुंहासे",
    "15. Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions": "15. एक्टिनिक केराटोसिस / बेसल सेल कार्सिनोमा / अन्य घातक घाव",
    "16. Bullous Disease Photos": "16. फफोले वाली त्वचा बीमारी",
    "17. Cellulitis Impetigo and other Bacterial Infections": "17. सेल्युलाइटिस / इम्पेटिगो / बैक्टीरियल संक्रमण",
    "18. Exanthems and Drug Eruptions": "18. दवा या वायरल रैश",
    "19. Hair Loss Photos Alopecia and other Hair Diseases": "19. बाल झड़ना / एलोपेसिया और अन्य बाल रोग",
    "2. Melanoma": "2. मेलानोमा",
    "20. Herpes HPV and other STDs Photos": "20. हरपीज / एचपीवी / अन्य यौन संक्रमण",
    "21. Light Diseases and Disorders of Pigmentation": "21. रंगत से जुड़ी त्वचा समस्याएं",
    "22. Lupus and other Connective Tissue diseases": "22. लूपस और कनेक्टिव टिश्यू रोग",
    "23. Nail Fungus and other Nail Disease": "23. नाखून फंगस और अन्य नाखून रोग",
    "24. Poison Ivy Photos and other Contact Dermatitis": "24. कॉन्टैक्ट डर्मेटाइटिस / पॉइजन आइवी रैश",
    "25. Rosacea Photos": "25. रोजेसिया",
    "26. Scabies Lyme Disease and other Infestations and Bites": "26. खुजली (स्केबीज) / लाइम / कीट काटने की समस्या",
    "28. Systemic Disease": "28. सिस्टमिक बीमारी के त्वचा संकेत",
    "3. Atopic Dermatitis": "3. एटॉपिक डर्मेटाइटिस",
    "30. Urticaria Hives": "30. अर्टिकेरिया (हाइव्स)",
    "31. Vascular Tumors": "31. रक्तवाहिका ट्यूमर",
    "32. Vasculitis Photos": "32. वैस्कुलाइटिस",
    "34. Normal Skin": "34. सामान्य त्वचा",
    "4. Basal Cell Carcinoma": "4. बेसल सेल कार्सिनोमा",
    "5. Melanocytic Nevi": "5. तिल (मेलानोसाइटिक नेवी)",
    "6. Benign Keratosis-like Lesions": "6. सौम्य केराटोसिस जैसे घाव",
    "7. Psoriasis pictures Lichen Planus and related diseases": "7. सोरायसिस / लाइकेन प्लेनस और संबंधित रोग",
    "Enfeksiyonel": "संक्रामक त्वचा रोग",
    "Seborrheic Keratoses and other Benign Tumors": "सेबोरहाइक केराटोसिस और अन्य सौम्य ट्यूमर",
    "Tinea Ringworm Candidiasis and other Fungal Infections": "दाद / कैंडिडायसिस और अन्य फंगल संक्रमण",
    "Warts Molluscum and other Viral Infections": "मस्से / मोलस्कम और अन्य वायरल संक्रमण",
}


def _apply_keras_quantization_compat() -> None:
    """Models saved in Colab (Keras 2.20+) may include ``quantization_config`` on Dense; strip it for older Keras."""
    try:
        from keras.src.layers.core import dense as _dense_mod
    except ImportError:
        return
    dense_cls = _dense_mod.Dense
    if getattr(dense_cls, "_skin_quant_compat_applied", False):
        return
    _orig = dense_cls.from_config.__func__

    @classmethod
    def _from_config(cls, config):
        c = dict(config)
        c.pop("quantization_config", None)
        return _orig(cls, c)

    dense_cls.from_config = _from_config
    dense_cls._skin_quant_compat_applied = True


def get_class_names() -> list[str]:
    global _class_names
    if _class_names is None:
        if not DISEASE_INFO_PATH.is_file():
            raise FileNotFoundError(f"Missing disease info: {DISEASE_INFO_PATH}")
        with open(DISEASE_INFO_PATH, encoding="utf-8") as f:
            data: dict[str, dict] = json.load(f)
        _class_names = list(data.keys())
    return _class_names


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(f"Missing model weights: {MODEL_PATH}")
        import tensorflow as tf

        _apply_keras_quantization_compat()
        _model = tf.keras.models.load_model(str(MODEL_PATH))
    return _model


def prepare_image(file_storage) -> np.ndarray:
    img = Image.open(file_storage.stream).convert("RGB")
    img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
    arr = np.asarray(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    return arr


def get_hindi_label(label: str) -> str:
    return HINDI_LABELS.get(label, label)


def get_recommendation(label: str) -> str:
    l = label.lower()
    if "normal skin" in l:
        return "Skin appears likely normal. Keep gentle cleansing, moisturization, and daily sunscreen."
    if any(k in l for k in ["carcinoma", "melanoma", "malignant", "tumor"]):
        return "High-risk category. Please consult a dermatologist urgently and avoid self-treatment."
    if any(k in l for k in ["fungal", "ringworm", "candidiasis", "nail fungus"]):
        return "Keep affected area dry and clean. Avoid sharing towels/clothes and consult for antifungal treatment."
    if any(k in l for k in ["viral", "warts", "molluscum", "herpes", "hpv"]):
        return "Avoid touching/scratching lesions and avoid skin-to-skin spread. Seek medical advice for antivirals."
    if any(k in l for k in ["bacterial", "cellulitis", "impetigo"]):
        return "Possible bacterial infection. Keep area clean and consult a doctor soon; antibiotics may be required."
    if any(k in l for k in ["psoriasis", "dermatitis", "eczema", "rosacea", "urticaria", "hives"]):
        return "Use mild skincare, avoid triggers (heat/fragrance/scratching), and consult dermatology for long-term control."
    if any(k in l for k in ["scabies", "bites", "infestations"]):
        return "Wash bedding/clothes in hot water and avoid close contact until medical treatment is started."
    return "This is an AI-based suggestion only. Please consult a dermatologist for proper diagnosis and treatment."


@app.route("/")
def index():
    return render_template(
        "index.html",
        num_classes=len(get_class_names()),
        img_size=IMG_SIZE[0],
        model_name="EfficientNetB3 (phase 2)",
    )


@app.route("/favicon.ico")
@app.route("/icon/favicon-32x32.png")
def favicon():
    return send_from_directory(BASE_DIR / "icon", "favicon-32x32.png", mimetype="image/png")


@app.route("/api/health")
def health():
    ok_model = MODEL_PATH.is_file()
    ok_disease_info = DISEASE_INFO_PATH.is_file()
    return jsonify(
        {
            "status": "ok" if ok_model and ok_disease_info else "degraded",
            "model_path": str(MODEL_PATH),
            "model_exists": ok_model,
            "disease_info_path": str(DISEASE_INFO_PATH),
            "disease_info_exists": ok_disease_info,
        }
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No file field 'image' in request."}), 400
    f = request.files["image"]
    if not f or f.filename == "":
        return jsonify({"error": "No file selected."}), 400

    ext = Path(secure_filename(f.filename)).suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"Unsupported type. Use: {', '.join(sorted(ALLOWED_EXT))}"}), 400

    try:
        batch = prepare_image(f)
    except Exception as e:
        return jsonify({"error": f"Could not read image: {e}"}), 400

    try:
        model = get_model()
        preds = model.predict(batch, verbose=0)[0]
    except Exception as e:
        return jsonify({"error": f"Inference failed: {e}"}), 500

    names = get_class_names()
    if len(preds) != len(names):
        return jsonify(
            {
                "error": f"Model output size {len(preds)} does not match labels {len(names)}.",
            }
        ), 500

    top_k = min(5, len(names))
    idx = np.argsort(preds)[::-1][:top_k]
    results = []
    for i, j in enumerate(idx):
        eng_label = names[j]
        results.append(
            {
                "rank": i + 1,
                "label": eng_label,
                "label_hi": get_hindi_label(eng_label),
                "confidence": float(preds[j]),
                "recommendation": get_recommendation(eng_label),
            }
        )

    return jsonify(
        {
            "top_prediction": results[0],
            "top_k": results,
            "disclaimer": "Educational demo only — not a medical device. See a clinician for diagnosis.",
            "disclaimer_hi": "यह केवल शैक्षणिक डेमो है, चिकित्सा उपकरण नहीं। सही निदान के लिए त्वचा विशेषज्ञ से मिलें।",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
