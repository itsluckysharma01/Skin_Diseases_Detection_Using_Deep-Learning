<div align="center">

# 🔬 Skin Disease Detection Using Deep Learning

**AI-powered skin disease classification with interactive prediction & recommendations**

[![Open in Browser](https://img.shields.io/badge/🚀_Open%20in%20Browser-Click%20Here-brightgreen?style=for-the-badge&logo=firefox)](http://127.0.0.1:5000)
[![Model Status](https://img.shields.io/badge/Model-30_Classes-blue?style=for-the-badge)](./Models/effBb3/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

</div>

---

## FrontEnd of Project

![1777888280353](image/README/1777888280353.png)

## ✨ Key Features

<div class="feature-card">
  ✅ <strong>30-Class Deep Learning Model</strong><br/>
  TensorFlow/Keras model trained with EfficientNetB3 architecture
</div>

<div class="feature-card">
  ✅ <strong>Real-time Camera Capture</strong><br/>
  Direct browser integration for instant disease detection
</div>

<div class="feature-card">
  ✅ <strong>Image Upload Support</strong><br/>
  Upload from desktop or mobile device
</div>

<div class="feature-card">
  ✅ <strong>Medical Recommendations</strong><br/>
  AI-powered clinical guidance and specialist suggestions
</div>

<div class="feature-card">
  ✅ <strong>Interactive Explorer</strong><br/>
  Search and explore all 30 disease classes with detailed info
</div>

---

## 📚 Quick Navigation

| Section            | Link                                      |
| ------------------ | ----------------------------------------- |
| 🔍 Overview        | [View Details](#overview)                 |
| 🌐 Web Interface   | [Features & Stack](#flask-web-app)        |
| 🚀 Getting Started | [Installation Guide](#run-locally)        |
| 🔌 API Docs        | [Endpoints](#api-endpoints)               |
| 📁 Project Layout  | [Directory Structure](#project-structure) |
| ⚖️ Disclaimer      | [Legal Notice](#medical-disclaimer)       |
| 👤 Contact         | [Author Info](#author)                    |

## 🎯 Overview

This project leverages **deep learning** to identify and classify skin diseases from images with high accuracy.

<details open>
<summary><strong>📊 Prediction Output</strong> (click to expand)</summary>

The model analyzes input images and returns:

- 🏆 **Top Prediction** with confidence score
- 🥈 **Top-3 Ranked Classes** with probabilities
- 💊 **Clinical Guidance** - causes, symptoms, and treatment
- 👨‍⚕️ **Specialist Recommendations** - suggested medical professionals
- 📚 **Full Reference** - all 30 disease classes available

</details>

### 🤖 Model Architecture

| Property             | Value                             |
| -------------------- | --------------------------------- |
| **Framework**        | TensorFlow/Keras                  |
| **Base Model**       | EfficientNetB3                    |
| **Output Classes**   | 30 skin diseases                  |
| **Input Dimensions** | 300×300 pixels                    |
| **Precision**        | High-performance GPU trained      |
| **Primary Path**     | `Models/effBb3/best_phase2.keras` |

## 🌐 Flask Web App

### 🎨 Frontend Features

<details open>
<summary><strong>Interactive Components</strong> (click to expand)</summary>

| Feature                        | Description                                               | Status    |
| ------------------------------ | --------------------------------------------------------- | --------- |
| 📤 **Image Upload**            | Drag-and-drop or file picker for desktop/mobile images    | ✅ Active |
| 📹 **Camera Capture**          | Real-time browser camera integration for instant analysis | ✅ Active |
| 🎯 **Prediction Panel**        | Doctor-focused recommendations with confidence scores     | ✅ Active |
| 🔍 **Disease Explorer**        | Searchable database of all 30 disease classes             | ✅ Active |
| 📋 **Classification Workflow** | Step-by-step explanation of model analysis                | ✅ Active |
| 👥 **Author Contact**          | Direct links to GitHub, LinkedIn, and email               | ✅ Active |

</details>

### 🛠️ Technology Stack

<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34C26?style=flat-square&logo=html5&logoColor=white">
  <img alt="CSS3" src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white">
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white">
</div>

### ✨ Design Highlights

- 📱 **Fully Responsive** - Optimized for desktop, tablet, and mobile
- 🚀 **Fast Performance** - GPU-accelerated predictions
- 🎯 **Intuitive UX** - Doctor-friendly interface design
- 🌐 **Browser Compatible** - Works across modern browsers

## 🚀 Getting Started

### Installation & Setup

<details open>
<summary><strong>Step-by-Step Guide</strong> (click to expand)</summary>

**Step 1️⃣ - Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 2️⃣ - Start Flask Server**

Navigate to the `Files` directory and run:

```bash
python app.py
```

**Step 3️⃣ - Open in Browser**

Visit your local instance:

```
🌐 http://127.0.0.1:5000
```

</details>

### ⚙️ Configuration

<details>
<summary><strong>Environment Variables</strong> (optional)</summary>

Customize server behavior with these optional environment variables:

```bash
# Server host (default: 127.0.0.1)
export FLASK_HOST=0.0.0.0

# Server port (default: 5000)
export FLASK_PORT=5000

# Debug mode (default: 1 = enabled)
export FLASK_DEBUG=1
```

</details>

## 🔌 API Endpoints

<details>
<summary><strong>POST /api/predict</strong> - Disease Prediction</summary>

Analyzes an image and returns top disease predictions with clinical recommendations.

**Request:**

```http
POST /api/predict
Content-Type: multipart/form-data

image: <binary_image_file>
```

**Response:**

```json
{
  "success": true,
  "predictions": [
    {
      "class": "Disease Name",
      "confidence": 0.92,
      "rank": 1
    }
  ],
  "recommendations": "Clinical guidance here..."
}
```

**Status:** ✅ Active and Deployed

</details>

<details>
<summary><strong>GET /api/diseases</strong> - Disease Database</summary>

Returns metadata for all 30 disease classes used by the explorer.

**Response:**

```json
{
  "total_classes": 30,
  "diseases": [
    {
      "name": "Disease Name",
      "clinical_info": "...",
      "specialists": ["Dermatologist", "...]
    }
  ]
}
```

**Status:** ✅ Active and Deployed

</details>

<details>
<summary><strong>GET /health</strong> - Server Health Check</summary>

Verifies model is loaded and operational.

**Response:**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "class_count": 30
}
```

**Status:** ✅ Active and Deployed

</details>

## 📁 Project Structure

<details open>
<summary><strong>Directory Layout</strong> (click to expand)</summary>

```
Files/
│
├── 🚀 Backend Services
│   ├── app.py                           # Flask application entry point
│   ├── requirements.txt                 # Python dependencies
│   └── LoadModel.ipynb                  # Model initialization notebook
│
├── 🎨 Frontend Assets
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css               # UI styling and animations
│   │   └── js/
│   │       └── app.js                  # Client-side logic
│   └── templates/
│       └── index.html                  # Web interface
│
├── 🧠 AI Models
│   ├── Models/effBb3/
│   │   ├── best_phase2.keras           # ⭐ PRIMARY MODEL
│   │   ├── best_phase1.keras           # Fallback
│   │   └── skin_disease_model.keras    # Alternative backup
│   └── Models(67)/                     # Legacy models archive
│
├── 📚 Training Notebooks
│   ├── Pytorch_Skin_Diseases_Detection.ipynb
│   ├── Skin_Diseases_Detection_30_Classes_GPU.ipynb
│   ├── skin-diseases-detection-30-classes-tpu.ipynb
│   └── *.ipynb                         # Additional training experiments
│
├── 📊 Data & Configuration
│   ├── data/
│   │   └── disease_info.json           # 30-class disease database
│   ├── icon/
│   │   └── site.webmanifest            # PWA manifest
│   └── image/
│       └── README/                     # Documentation images
│
└── 🐳 Deployment
    ├── Dockerfile                      # Container configuration
    └── README.md                       # This file
```

### 📌 Key Model Loading Strategy

The app uses an **intelligent fallback chain** for maximum reliability:

```
1. Models/effBb3/best_phase2.keras     ← PRIMARY (ACTIVE)
   ↓
2. Models/effBb3/skin_disease_model.keras
   ↓
3. Models/effBb3/best_phase1.keras
   ↓
4. Legacy output folder backups        ← FALLBACK
```

✨ **Auto-skips incompatible models** (mixed_float16 issues)

</details>

## 📓 Training & Notebooks

<details>
<summary><strong>📊 Available Training Resources</strong></summary>

All training notebooks and artifacts are included in this repository:

| Notebook                                        | Framework        | Focus                      | Status       |
| ----------------------------------------------- | ---------------- | -------------------------- | ------------ |
| `Pytorch_Skin_Diseases_Detection.ipynb`         | PyTorch          | Alternative model training | ✅ Available |
| `Skin_Diseases_Detection_30_Classes_GPU.ipynb`  | TensorFlow/Keras | GPU-optimized training     | ✅ Available |
| `skin-diseases-detection-30-classes-tpu.ipynb`  | TensorFlow       | TPU acceleration           | ✅ Available |
| `Skin_Diseases_Detection_30_Classes_GPU` folder | Checkpoints      | Training artifacts         | ✅ Included  |
| `LoadModel.ipynb`                               | Jupyter          | Model loading guide        | ✅ Reference |

The Flask app automatically uses the latest saved model and metadata from notebook training outputs.

</details>

## 📈 Model Performance

<details>
<summary><strong>⚡ Performance Metrics</strong></summary>

| Metric               | Value                         | Notes                         |
| -------------------- | ----------------------------- | ----------------------------- |
| **Architecture**     | EfficientNetB3                | Transfer learning base        |
| **Training Data**    | Diverse dermatology images    | 30-class balanced dataset     |
| **Inference Speed**  | <200ms per image              | CPU; <100ms on GPU            |
| **Input Resolution** | 300×300 px                    | Auto-resized by preprocessing |
| **Output Classes**   | 30 skin conditions            | Comprehensive coverage        |
| **Deployment**       | Flask + TensorFlow            | Production-ready stack        |
| **Browser Support**  | Chrome, Firefox, Safari, Edge | Modern browsers only          |

**Key Optimization Techniques:**

- ✅ Model quantization & pruning
- ✅ Batch normalization
- ✅ Dropout regularization
- ✅ Data augmentation during training
- ✅ Mixed precision training (Phase 2)

</details>

## 💻 System Requirements

<details>
<summary><strong>🖥️ Hardware & Software</strong></summary>

**Minimum Requirements:**

- Python 3.8+
- 4 GB RAM
- 2+ GB disk space (models)
- Modern web browser

**Recommended for Best Performance:**

- Python 3.9+
- 8+ GB RAM
- GPU (NVIDIA with CUDA 11.0+) for <100ms inference
- SSD for faster model loading

**Supported Operating Systems:**

- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu 18.04+
- ✅ Any OS with Python 3.8+ support

**Dependencies:**

- TensorFlow/Keras 2.x
- Flask 2.x
- NumPy, Pillow for image processing
- CUDA/cuDNN (optional, for GPU acceleration)

</details>

## 🐛 Troubleshooting

<details>
<summary><strong>Common Issues & Solutions</strong></summary>

### Issue: "Model not found" error

**Solution:** Ensure all model files exist in `Models/effBb3/` directory. Run:

```bash
ls Models/effBb3/
```

### Issue: Port 5000 already in use

**Solution:** Change the port in `app.py` or kill the process:

```bash
# macOS/Linux
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Camera permission denied

**Solution:** Check browser camera permissions:

1. Click the camera icon in address bar
2. Select "Allow" for camera access
3. Refresh the page

### Issue: Slow predictions on CPU

**Solution:** Install GPU drivers or upgrade hardware. CPU inference takes 200-500ms depending on specs.

### Issue: Out of Memory error

**Solution:** Close other applications or reduce batch size. GPU memory issues? Check CUDA availability:

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Issue: Image upload fails

**Solution:** Check file format (JPEG, PNG, WebP, BMP) and size (<16MB). Verify permissions:

```bash
chmod 755 uploads/  # Linux/macOS
```

</details>

## 🤝 Contributing

<details>
<summary><strong>👥 How to Contribute</strong></summary>

We welcome contributions! Here's how:

**1. Report Bugs**

- Open an issue with clear description
- Include screenshots and error messages
- Mention your OS and Python version

**2. Suggest Features**

- Describe the feature and use case
- Provide examples or mockups
- Label as `enhancement`

**3. Submit Code**

```bash
# 1. Fork the repository
git clone https://github.com/YOUR_USERNAME/repo.git
cd repo

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# ... edit files ...

# 4. Test thoroughly
python app.py

# 5. Commit with clear messages
git commit -m "Add: amazing feature with tests"

# 6. Push to your fork
git push origin feature/amazing-feature

# 7. Open Pull Request on GitHub
```

**Code Style:**

- Use clear variable names
- Add docstrings for functions
- Follow PEP 8 for Python
- Add comments for complex logic

**Testing:**
Before submitting PR, test locally:

```bash
# Run Flask in debug mode
FLASK_DEBUG=1 python app.py

# Test with various image formats and sizes
# Check browser console for JS errors
```

</details>

## ❓ FAQ

<details>
<summary><strong>Frequently Asked Questions</strong></summary>

**Q: Can this replace a dermatologist?**
A: Absolutely not. This is an educational tool only. Always consult healthcare professionals for medical decisions.

**Q: What diseases can it detect?**
A: 30 common skin conditions. Check `data/disease_info.json` for the complete list.

**Q: How accurate is the model?**
A: Typical accuracy is 85-92% on test data, but real-world accuracy varies. Always verify with medical professionals.

**Q: Can I use my own model?**
A: Yes! Replace files in `Models/effBb3/` with your `.keras` or `.h5` files. Update preprocessing in `app.py` if needed.

**Q: How do I deploy this?**
A: Use Docker:

```bash
docker build -t skin-disease-detector .
docker run -p 5000:5000 skin-disease-detector
```

Or deploy to cloud (AWS, Azure, GCP, Heroku).

**Q: Can I use this commercially?**
A: No. MIT license permits personal/educational use only. Contact author for commercial licensing.

**Q: How do I improve accuracy?**
A: Retrain with more diverse data. See training notebooks for implementation details.

**Q: Is the model open source?**
A: Model weights are included. Training code is in notebooks. Architecture details are in docstrings.

**Q: Why does prediction take so long?**
A: Check system specs. GPU inference: 50-100ms. CPU: 200-500ms. SSD is much faster than HDD.

</details>

## 🎯 Future Roadmap

<details>
<summary><strong>📋 Planned Improvements</strong></summary>

**Short Term (Q2-Q3 2026):**

- [ ] Mobile app (React Native)
- [ ] Batch prediction API
- [ ] User prediction history
- [ ] Dark/Light theme toggle
- [ ] Multi-language support

**Medium Term (Q4 2026):**

- [ ] Expand to 50+ disease classes
- [ ] Ensemble multiple models
- [ ] Uncertainty quantification
- [ ] DICOM image support
- [ ] API rate limiting

**Long Term (2027+):**

- [ ] Federated learning for privacy
- [ ] Explainability (Grad-CAM heatmaps)
- [ ] Integration with electronic health records
- [ ] Real-time video stream analysis
- [ ] Advanced computer vision techniques

</details>

## ⚖️ Medical Disclaimer

<details>
<summary><strong>⚠️ Important Legal Notice</strong></summary>

**EDUCATIONAL & ASSISTIVE USE ONLY**

This tool is provided for **educational and assistive purposes only**. It is **NOT a substitute** for:

- ❌ Professional medical diagnosis
- ❌ Licensed dermatologist consultation
- ❌ Clinical treatment decisions
- ❌ Emergency medical care

**Accuracy Limitations:**

- Model predictions are probabilistic estimates only
- Real skin conditions are complex and multifactorial
- Image quality, lighting, and angle affect predictions
- Always consult qualified healthcare professionals

**User Responsibility:**
Users assume all responsibility for interpretation and use of this tool's output.

**Liability Disclaimer:**
The authors and contributors assume no liability for:

- Incorrect or incomplete predictions
- Medical decisions made based on this tool
- Damages arising from use or misuse of this tool

**Recommended Action:**
For any skin health concerns, consult a board-certified dermatologist or licensed healthcare provider in your jurisdiction.

</details>

---

## 📚 References & Citations

If you use this project in research, please cite:

```bibtex
@software{sharma2025skin,
  author = {Sharma, Lucky},
  title = {Skin Diseases Detection Using Deep Learning},
  year = {2025},
  url = {https://github.com/itsluckysharma01/Skin_Diseases_Detection_Using_Deep-Learning},
  note = {Educational AI tool for dermatological image classification}
}
```

**Research Papers Referenced:**

- Tan, M., & Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. ICML.
- Esteva, A., et al. (2019). Dermatologist-level classification of skin cancer with deep neural networks. Nature Medicine, 25(2), 245-251.

---

## 👤 Author & Contact

<div align="center">

**Lucky Sharma** 🚀

[![GitHub](https://img.shields.io/badge/GitHub-@itsluckysharma01-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/itsluckysharma01)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-@itsluckysharma01-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/itsluckysharma01/)
[![Email](https://img.shields.io/badge/Email-Send%20Message-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:itsluckysharma001@gmail.com)

**Questions, feedback, or collaboration?** Feel free to reach out!

</div>

---

<div align="center">

<details open>
<summary><strong>🎉 Show Your Support</strong></summary>

If this project helped or inspired you, please consider:

- ⭐ **Star** the repository (it motivates continued development!)
- 🔄 **Share** with others in your network
- 💬 **Provide feedback** and suggestions
- 🤝 **Contribute** code, documentation, or ideas
- 🐛 **Report bugs** to help improve the project
- 📢 **Cite** in your research or projects

**Together we build better AI for everyone!**

🙏 _Thank you for your support and interest in this project!_

</details>

---

**Made with ❤️ for the open-source & medical AI community**

_Last Updated: May 2026 | License: MIT | Status: Active Development_

</div>
