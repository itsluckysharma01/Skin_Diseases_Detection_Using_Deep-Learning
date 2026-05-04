# Skin Disease Detection Using Deep Learning

AI-powered skin disease classification project with:

- 30-class TensorFlow model (from notebook training outputs)
- Flask web app with camera capture + upload
- Interactive disease explorer with recommendations

## Quick Links

- [Overview](#overview)
- [Flask Web App](#flask-web-app)
- [Run Locally](#run-locally)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Medical Disclaimer](#medical-disclaimer)
- [Author](#author)

## Overview

This project predicts skin disease classes from an image and returns:

- Top prediction + confidence
- Top-3 ranked classes
- Class-wise guidance and suggested next action
- Full 30-class reference data loaded from notebook output artifacts

The model and class map are loaded from:

- `Output/outputs/skin_disease_final.keras` (preferred)
- `Output/outputs/best_phase2.keras` (fallback)
- `Output/outputs/class_names.json`

## Flask Web App

### Features

- Upload image from desktop/mobile
- Direct camera capture in browser
- Prediction panel with doctor-focused recommendations
- Searchable explorer of all 30 classes
- Classification workflow explanation section
- About and contact section (GitHub, LinkedIn, email)

### Frontend Stack

- HTML + CSS + JavaScript
- Responsive design for desktop and mobile
- Camera support using `navigator.mediaDevices.getUserMedia`

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start Flask app from the `Files` directory:

```bash
python app.py
```

3. Open in browser:

```text
http://127.0.0.1:5000
```

### Optional Environment Variables

- `FLASK_HOST` (default: `127.0.0.1`)
- `FLASK_PORT` (default: `5000`)
- `FLASK_DEBUG` (default: `1`)

## API Endpoints

<details>
<summary><strong>POST /api/predict</strong></summary>

- Accepts multipart form with `image`
- Returns prediction result with top-3 classes and recommendations

</details>

<details>
<summary><strong>GET /api/diseases</strong></summary>

- Returns all class metadata used by frontend explorer

</details>

<details>
<summary><strong>GET /health</strong></summary>

- Returns model load status and class count

</details>

## Project Structure

```text
Files/
|-- app.py
|-- data/
|   `-- disease_info.json
|-- static/
|   |-- css/
|   |   `-- style.css
|   `-- js/
|       `-- app.js
|-- templates/
|   `-- index.html
|-- Output/
|   `-- outputs/
|       |-- class_names.json
|       |-- best_phase2.keras
|       `-- skin_disease_final.keras
|-- requirements.txt
`-- *.ipynb
```

## Notebook + Training Artifacts

Training notebooks and outputs are included in this repository. The deployed Flask app uses the saved model and metadata generated during notebook training.

## Medical Disclaimer

This tool is for educational and assistive use only.
It is not a substitute for professional medical diagnosis, treatment, or emergency care.

## Author

<<<<<<< HEAD
- Lucky Sharma
-@itsluckysharma01
- GitHub: https://github.com/itsluckysharma01
- LinkedIn: https://www.linkedin.com/in/itsluckysharma01/
- Email: itsluckysharma001@gmail.com
=======
- Lucky Sharma (@itsluckysharma01)

## Acknowledgments

- Thanks to all contributors who helped in developing this project
- Special thanks to the medical professionals who helped in validating the results

## Contact
- Lucky Sharma (@itsluckysharma01)
- ---
  Gmail:- itsluckysharma001@gmail.com

>>>>>>> 24a5c91c70feabc4bde18654d88bbce1142d92b1
