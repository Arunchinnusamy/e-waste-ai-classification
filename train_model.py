import tensorflow as tf
from tensorflow.keras
import layers, models
from tensorflow.keras.applications import MobileNetV2
from pathlib import Path

# =========================
# 1. Dataset path
# =========================

BASE_DIR = Path(__file__).resolve().parent
dataset_path = BASE_DIR / "backend" / "data" / "modified-dataset"
# Fallback to the original absolute path when the local dataset isn't present
if not dataset_path.exists():
    dataset_path = Path(r"D:\e-waste-python\e_waste_dataset\modified-dataset")

IMG_SIZE = (160, 160)
BATCH_SIZE = 8
SEED = 42

# =========================
# 2. Load datasets
# =========================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path + r"\train",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED
)

val_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path + r"\val",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path + r"\test",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = train_dataset.class_names

print("\nClasses:")
print(class_names)

print("\nNumber of classes:", len(class_names))

# =========================
# 3. Data augmentation
# =========================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

# =========================
# 4. MobileNetV2
# =========================

base_model = MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

# =========================
# 5. Build model
# =========================

model = models.Sequential([
  layers.Input(shape=(160, 160, 3)),

    data_augmentation,

    layers.Rescaling(1./127.5, offset=-1),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.2),

])

# =========================
# 6. Compile
# =========================

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# 7. Train
# =========================

EPOCHS = 5

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS
)

# =========================
# 8. Test
# =========================

test_loss, test_accuracy = model.evaluate(test_dataset)

print("\nTest Accuracy:", test_accuracy)
print("Test Accuracy (%):", test_accuracy * 100)

# =========================
# 9. Save model
# =========================

from pathlib import Path

out_dir = Path(__file__).resolve().parent / "backend" / "model"
out_dir.mkdir(parents=True, exist_ok=True)

model.save(str(out_dir / "e_waste_classifier.keras"))

# =========================
# 10. Save class names
# =========================

import json

with open(out_dir / "class_names.json", "w") as f:
    json.dump(class_names, f)

print("\nModel saved successfully!")
print(out_dir / "e_waste_classifier.keras")
print(out_dir / "class_names.json")