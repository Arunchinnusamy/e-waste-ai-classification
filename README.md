# AI-Based E-Waste Classification & Recycling Recommendation

<div align="center">

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=microsoft&logoColor=white)

</div>

A practical AI-powered solution for classifying electronic waste from images and recommending responsible recycling actions. The project combines a modern React frontend with a FastAPI backend and a MobileNetV2-based deep learning model to support faster, more accessible e-waste identification.

## Overview

Electronic waste is growing rapidly, and improper disposal can create serious environmental and health risks. This project helps reduce that problem by allowing users to upload an image of e-waste and receive an AI-based prediction along with a relevant recycling suggestion.

The system is designed for local demos, learning environments, and small-scale waste management assistance, with a clear web interface and a lightweight backend workflow.

## Problem Statement

Manual identification of discarded electronics is often inconsistent, slow, and dependent on user experience. Waste handlers, students, and general users often need a quick and reliable way to recognize common e-waste categories and determine the appropriate disposal or recycling path.

This project addresses that need by combining:

- a React + Vite user interface,
- a FastAPI backend for inference,
- a MobileNetV2 transfer-learning model trained for e-waste classification.

## Objectives

- Classify common electronic waste items from an uploaded image.
- Provide a suitable recycling recommendation for the predicted item.
- Keep the system simple, lightweight, and easy to run locally.
- Demonstrate an AI workflow suitable for education and prototype deployment.
- Support confident predictions while handling clear low-confidence cases safely.

## Key Features

- Image upload and validation in the browser
- Client-side error handling for invalid or missing files
- FastAPI prediction endpoint
- TensorFlow/Keras model inference
- Confidence score for each prediction
- Recycling recommendation based on category
- Low-confidence handling for unclear images
- Responsive web interface for local use
- Windows-friendly local setup and run workflow

## Supported E-Waste Classes

- Battery
- Keyboard
- Microwave
- Mobile
- Mouse
- PCB
- Player
- Printer
- Television
- Washing Machine

## System Architecture and Workflow

```text
User uploads image
        │
        ▼
React frontend (Vite)
        │
        ├─ validates image file
        └─ sends multipart request to backend
                        │
                        ▼
                FastAPI backend (/predict)
                        │
                        ├─ reads image
                        ├─ resizes and normalizes input
                        └─ runs TensorFlow model
                        │
                        ▼
             MobileNetV2 prediction + confidence
                        │
                        ▼
       Recommendation returned to frontend
                        │
                        ▼
         Result displayed to the user
```

## Dataset and Model Details

The project uses a custom e-waste image dataset with a combined total of 3,000 images across 10 classes.

### Dataset split

- Training: 2,400 images
- Validation: 300 images
- Test: 300 images

### Model approach

The base model uses MobileNetV2 as a transfer-learning backbone. This allows the project to leverage pretrained visual features and adapt the final layers for the e-waste classification task.

### Reported test accuracy

This project reports a measured test accuracy of 95.33% on the held-out test set.

> Important: the reported 95.33% is a measured benchmark on the evaluation dataset and should be treated as a model performance result, not as proof that every real-world image will classify perfectly.

## Technology Stack

### Frontend
- React
- Vite
- JavaScript / JSX
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- Pillow
- NumPy
- TensorFlow / Keras

### AI model
- MobileNetV2 transfer learning
- Local Keras model file

## Project Structure

```text
e-waste-website/
├── backend/
│   ├── main.py
│   └── model/
│       └── class_names.json
├── public/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
├── train_model.py
├── vite.config.js
└── README.md
```

The trained `e_waste_classifier.keras` file and training dataset are intentionally excluded from Git tracking. The model must be supplied separately and placed in `backend/model/` before starting the backend. The `class_names.json` metadata file remains part of the project structure.

## Setup Instructions

### Frontend dependencies

From the project root:

```powershell
cd <project-folder>
npm install
```

### Backend environment

Use a Python environment that already has the required libraries installed, or create a new one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install tensorflow fastapi uvicorn pillow numpy python-multipart
```

If using an existing local ML environment, activate it instead and confirm the required packages are available before running the backend.

### Optional model training

The training script is located at the project root as `train_model.py`. If training is performed locally, supply the dataset separately under this project-relative structure:

```text
backend/data/modified-dataset/
├── train/
├── val/
└── test/
```

The dataset is excluded from Git tracking. The training script is not required to run the existing application; the separately supplied trained model is required for backend inference.

## Local Run Guide

### 1. Start the backend

```powershell
cd <project-folder>
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Before starting the backend, confirm that the separately supplied model file is available at `backend/model/e_waste_classifier.keras` and that `backend/model/class_names.json` is present.

### 2. Start the frontend

```powershell
cd <project-folder>
npm run dev
```

Then open:

- Frontend: http://localhost:5173/
- Backend health: http://127.0.0.1:8000/health

## API Endpoints

### GET /
Returns a basic backend message.

```json
{
  "message": "E-Waste AI Backend is running!"
}
```

### GET /health
Returns a simple health check for the backend and model load path.

```json
{
  "status": "healthy",
  "model": "loaded"
}
```

### POST /predict
Uploads an image and returns the predicted class, confidence level, and recycling guidance.

Request format:

- multipart/form-data
- field name: `file`
- file type: image

Example response:

```json
{
  "filename": "example.png",
  "prediction": "PCB",
  "confidence": 71.4,
  "recommendation": "Send PCBs to a specialized e-waste recycler for safe component and metal recovery.",
  "is_low_confidence": false
}
```

Low-confidence response example:

```json
{
  "filename": "unclear.png",
  "prediction": "Mobile",
  "confidence": 62.1,
  "recommendation": null,
  "is_low_confidence": true,
  "message": "Low confidence prediction. Please upload a clearer image of the e-waste item."
}
```

## Limitations

- The model was trained on a specific dataset and may not generalize perfectly to every real-world image.
- Variations in lighting, camera angle, blur, and object background can reduce prediction quality.
- The app is best suited for local demos, educational use, and small-scale classification support rather than production-scale deployment without further validation.
- The backend relies on locally available model files and environment packages.
- Measured test accuracy should be interpreted as a benchmark value, not as a claim that every live upload will be correct.

## Future Improvements

- Improve preprocessing and augmentation for harder real-world images
- Add configurable confidence threshold controls in the frontend
- Expand the dataset for more categories and edge cases
- Add stronger accessibility and mobile UX improvements
- Implement better logging and user feedback collection
- Explore deployment options and production-ready hosting
- Add more extensive validation across diverse e-waste item types

## Repository and Large-File Guidance

This project should avoid committing large model files, datasets, virtual environments, and local dependencies unless repository rules explicitly allow them and the storage impact is reviewed first.

Recommended practices include:

- keeping large dataset/model files outside the tracked working set when possible,
- ensuring `.gitignore` is used for local environment folders,
- checking repository size and Git configuration before committing large assets.

## Summary of Changes

This documentation update preserves the accurate project information and improves the presentation for a final-year engineering portfolio:

- refined project title and introduction
- added technology badges
- organized key features and supported e-waste classes
- clarified architecture/workflow
- preserved dataset split and reported 95.33% benchmark metric
- kept setup instructions for Windows
- documented the separately supplied model requirement
- documented limitations and future improvements

No application source code was modified as part of this documentation update.
