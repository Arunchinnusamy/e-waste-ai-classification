from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path

app = FastAPI(
    title="E-Waste AI API",
    description="AI-Based E-Waste Classification & Recycling Recommendation"
)

RECOMMENDATION_THRESHOLD = 70.0

RECOMMENDATIONS = {
    "Battery": "Battery waste should be taken to an authorized battery/e-waste collection center. Do not mix with household waste.",
    "Keyboard": "Send the keyboard to an authorized e-waste recycling center.",
    "Microwave": "Send the microwave to an authorized e-waste recycling center.",
    "Mobile": "Send mobile phones to an authorized e-waste recycling center.",
    "Mouse": "Send the mouse to an authorized e-waste recycling center.",
    "PCB": "Send PCBs to a specialized e-waste recycler for safe component and metal recovery.",
    "Player": "Send the electronic player to an authorized e-waste recycling center.",
    "Printer": "Send the printer to an authorized e-waste recycling center.",
    "Television": "Send the television to an authorized e-waste recycling center.",
    "Washing Machine": "Send the washing machine to an authorized e-waste recycling center.",
}

# React frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load AI Model
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "e_waste_classifier.keras"
CLASS_PATH = BASE_DIR / "model" / "class_names.json"

model = None
class_names = []

def load_model_and_classes():
    global model, class_names
    try:
        if MODEL_PATH.exists():
            model = tf.keras.models.load_model(str(MODEL_PATH))
        else:
            print(f"Model file not found at {MODEL_PATH}")

        if CLASS_PATH.exists():
            with open(CLASS_PATH, "r") as f:
                class_names = json.load(f)
        else:
            print(f"Class names file not found at {CLASS_PATH}")

        if model is not None:
            print("AI Model loaded successfully!")
            print("Classes:", class_names)
    except Exception as e:
        print("Failed to load model or class names:", e)

# Attempt initial load, but continue even if it fails (lazy load on predict)
load_model_and_classes()


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "E-Waste AI Backend is running!"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "loaded"
    }


# -----------------------------
# AI Prediction
# -----------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    image_bytes = await file.read()

    # Convert image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Resize to model input size
    image = image.resize((160, 160))

    # Convert to NumPy
    image_array = np.array(image)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Ensure model is loaded
    if model is None:
        try:
            load_model_and_classes()
        except Exception:
            raise HTTPException(status_code=503, detail="Model not available")

    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    # Prediction
    predictions = model.predict(image_array, verbose=0)

    # Get highest probability
    predicted_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_index])

    predicted_class = class_names[predicted_index]
    confidence_percent = round(confidence * 100, 2)

    if confidence_percent < RECOMMENDATION_THRESHOLD:
        return {
            "filename": file.filename,
            "prediction": predicted_class,
            "confidence": confidence_percent,
            "recommendation": None,
            "is_low_confidence": True,
            "message": "Low confidence prediction. Please upload a clearer image of the e-waste item.",
        }

    return {
        "filename": file.filename,
        "prediction": predicted_class,
        "confidence": confidence_percent,
        "recommendation": RECOMMENDATIONS.get(
            predicted_class,
            "Send the item to an authorized e-waste recycling center.",
        ),
        "is_low_confidence": False,
    }