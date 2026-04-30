import base64
import io
import json
import os
from pathlib import Path
from threading import Lock

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output" / "outputs"
CLASS_NAMES_PATH = OUTPUT_DIR / "class_names.json"
DISEASE_INFO_PATH = BASE_DIR / "data" / "disease_info.json"

# Model candidates - ordered by priority
# Note: .keras files with mixed_float16 have compatibility issues, use .h5 models instead
MODEL_CANDIDATES = [
	BASE_DIR / "Models(67)" / "skin_disease_model.h5",
	BASE_DIR / "Models(67)" / "2.h5",
	BASE_DIR / "Models(67)" / "1.keras",
	OUTPUT_DIR / "skin_disease_final.keras",  # Fallback - may have compatibility issues
	OUTPUT_DIR / "best_phase2.keras",         # Fallback - may have compatibility issues
]

IMAGE_SIZE = (224, 224)  # Will be adjusted based on model
TOP_K = 3


def load_json(path: Path, default):
	if not path.exists():
		return default
	with path.open("r", encoding="utf-8") as file:
		return json.load(file)


def load_class_names() -> list[str]:
	class_map = load_json(CLASS_NAMES_PATH, default={})
	if not class_map:
		return []
	sorted_items = sorted(class_map.items(), key=lambda item: int(item[0]))
	return [name for _, name in sorted_items]


def normalize_label(label: str) -> str:
	return " ".join(label.replace("_", " ").split()).strip()


def default_disease_info(label: str) -> dict:
	readable = normalize_label(label)
	return {
		"display_name": readable,
		"clinical_summary": "This class may include visual patterns that overlap with other skin conditions.",
		"common_signs": [
			"Color, texture, or border changes in the skin area",
			"Visible lesion or patch with persistent appearance",
		],
		"possible_triggers": [
			"Inflammation, infection, allergy, or chronic skin irritation",
			"Environmental and genetic factors",
		],
		"recommended_actions": [
			"Take clear photos in natural light and monitor progression",
			"Consult a dermatologist for clinical confirmation",
			"Avoid self-medication without medical advice",
		],
		"urgency": "Moderate",
		"specialist": "Dermatologist",
	}


def format_probability(value: float) -> float:
	return round(float(value) * 100.0, 2)


def read_image_from_request() -> Image.Image:
	if "image" in request.files:
		return Image.open(request.files["image"].stream)

	payload = request.form.get("camera_image", "")
	if payload.startswith("data:image"):
		_, encoded = payload.split(",", 1)
		decoded = base64.b64decode(encoded)
		return Image.open(io.BytesIO(decoded))

	raise ValueError("No image found in request payload.")


def preprocess_image(img: Image.Image, target_size: tuple = None) -> np.ndarray:
	if target_size is None:
		target_size = IMAGE_SIZE
	
	rgb_image = img.convert("RGB")
	resized = rgb_image.resize(target_size)
	array = np.asarray(resized, dtype=np.float32) / 255.0
	return np.expand_dims(array, axis=0)


def select_model_path() -> Path:
	for candidate in MODEL_CANDIDATES:
		if candidate.exists():
			return candidate
	raise FileNotFoundError(
		"No model file found. Expected one of: "
		+ ", ".join(str(path) for path in MODEL_CANDIDATES)
	)


def load_model_with_fallback(model_path: Path):
	"""Load model with error handling - skip incompatible models"""
	try:
		model = tf.keras.models.load_model(str(model_path), compile=False)
		return model, True
	except (TypeError, ValueError) as e:
		if "quantization_config" in str(e) or "mixed_float" in str(e):
			print(f"Skipping {model_path.name} - Keras/TensorFlow version incompatibility")
			return None, False
		raise
	except Exception as e:
		print(f"Error loading {model_path.name}: {e}")
		return None, False


class PredictionService:
	def __init__(self):
		self._model = None
		self._lock = Lock()
		self._model_image_size = IMAGE_SIZE
		self.class_names = load_class_names()
		self.disease_info = load_json(DISEASE_INFO_PATH, default={})

	def get_model(self):
		if self._model is not None:
			return self._model

		with self._lock:
			if self._model is None:
				# Try each model candidate in order
				for model_path in MODEL_CANDIDATES:
					if not model_path.exists():
						continue
					
					print(f"Attempting to load model: {model_path.name}")
					model, success = load_model_with_fallback(model_path)
					
					if success and model is not None:
						self._model = model
						
						# Get model's input size from its shape
						# Model input shape is typically (None, height, width, channels)
						if len(model.input_shape) >= 3:
							height = model.input_shape[1]
							width = model.input_shape[2]
							if height and width:
								self._model_image_size = (height, width)
								print(f"Using model image size: {self._model_image_size}")
						
						# Handle class names - ensure they match model output
						model_output_size = int(self._model.output_shape[-1])
						if self.class_names and len(self.class_names) < model_output_size:
							# Pad missing class names
							print(f"WARNING: Model outputs {model_output_size} classes but only {len(self.class_names)} class names loaded.")
							print(f"Padding with generic class names for classes {len(self.class_names)}-{model_output_size-1}")
							for i in range(len(self.class_names), model_output_size):
								self.class_names.append(f"Class {i}")
						elif not self.class_names:
							self.class_names = [f"Class {idx}" for idx in range(model_output_size)]
						
						print(f"Successfully loaded model: {model_path.name}")
						print(f"Model input shape: {model.input_shape}")
						print(f"Model output shape: {model.output_shape}")
						print(f"Available class names: {len(self.class_names)}")
						return self._model
				
				# If no model loaded, raise error
				raise FileNotFoundError(
					"Could not load any model. All models either don't exist or have compatibility issues."
				)
		
		return self._model

	def predict(self, image_array: np.ndarray) -> dict:
		model = self.get_model()
		predictions = model.predict(image_array, verbose=0)[0]

		top_indices = np.argsort(predictions)[::-1][:TOP_K]
		top_predictions = []
		for index in top_indices:
			label = self.class_names[index] if index < len(self.class_names) else f"Class {index}"
			info = self.disease_info.get(label, default_disease_info(label))
			top_predictions.append(
				{
					"class_index": int(index),
					"class_name": label,
					"probability": format_probability(predictions[index]),
					"details": info,
				}
			)

		predicted = top_predictions[0]
		return {
			"predicted": predicted,
			"top_predictions": top_predictions,
			"disclaimer": (
				"This AI result is informational only and is not a medical diagnosis. "
				"Please consult a licensed dermatologist for clinical confirmation."
			),
		}


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
service = PredictionService()


@app.route("/")
def index():
	model_path = None
	model_dims = f"{IMAGE_SIZE[0]}x{IMAGE_SIZE[1]}"
	
	try:
		# Initialize service to load model and get actual dimensions
		service.get_model()
		model_path = "Model loaded successfully"
		model_dims = f"{service._model_image_size[0]}x{service._model_image_size[1]}"
	except Exception as e:
		model_path = f"Error: {str(e)[:50]}"

	all_diseases = []
	for idx, name in enumerate(service.class_names):
		all_diseases.append(
			{
				"index": idx,
				"name": name,
				"details": service.disease_info.get(name, default_disease_info(name)),
			}
		)

	return render_template(
		"index.html",
		disease_count=len(all_diseases),
		diseases=all_diseases,
		model_path=model_path,
		image_size=model_dims,
		project_owner={
			"name": "Lucky Sharma",
			"github": "https://github.com/itsluckysharma01",
			"linkedin": "https://www.linkedin.com/in/itsluckysharma01/",
			"email": "itsluckysharma001@gmail.com",
		},
	)


@app.route("/api/predict", methods=["POST"])
def predict():
	try:
		image = read_image_from_request()
		# Use the model's actual image size for preprocessing
		image_array = preprocess_image(image, service._model_image_size)
		result = service.predict(image_array)
		return jsonify({"ok": True, "result": result})
	except (ValueError, UnidentifiedImageError) as error:
		return jsonify({"ok": False, "error": str(error)}), 400
	except FileNotFoundError as error:
		return jsonify({"ok": False, "error": str(error)}), 500
	except Exception:
		return jsonify(
			{
				"ok": False,
				"error": "Unexpected error while processing prediction. Try again.",
			}
		), 500


@app.route("/api/diseases", methods=["GET"])
def get_diseases():
	diseases = []
	for idx, name in enumerate(service.class_names):
		diseases.append(
			{
				"index": idx,
				"name": name,
				"details": service.disease_info.get(name, default_disease_info(name)),
			}
		)
	return jsonify({"ok": True, "count": len(diseases), "diseases": diseases})


@app.route("/health", methods=["GET"])
def health():
	model_ready = False
	model_error = None
	try:
		service.get_model()
		model_ready = True
	except Exception as error:
		model_error = str(error)

	return jsonify(
		{
			"ok": True,
			"model_ready": model_ready,
			"model_error": model_error,
			"class_count": len(service.class_names),
		}
	)


if __name__ == "__main__":
	host = os.getenv("FLASK_HOST", "127.0.0.1")
	port = int(os.getenv("FLASK_PORT", "5000"))
	debug = os.getenv("FLASK_DEBUG", "1") == "1"
	app.run(host=host, port=port, debug=debug)
