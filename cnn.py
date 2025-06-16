import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

# 1. Load direktori
def load_dataset(base_dir):
    train_dir = os.path.join(base_dir, "train")
    validation_dir = os.path.join(base_dir, "validation")
    return train_dir, validation_dir

# 2. Preprocessing + augmentasi
def do_data_preprocessing(train_dir, validation_dir):
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1. / 255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        batch_size=20,
        class_mode="categorical",
        target_size=(150, 150),
        shuffle=True,
        seed=42
    )


    val_gen = val_datagen.flow_from_directory(
        validation_dir,
        batch_size=20,
        class_mode="categorical",
        target_size=(150, 150),
        shuffle=False,
        seed=42
    )

    return train_gen, val_gen

# 3. CNN Model
def create_cnn_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(150,150,3)),
        tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')  # 4 kelas
    ])

    model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 4. Visualisasi hasil training
def plot_history(train, val, title):
    epochs = range(len(train))
    plt.figure()
    plt.plot(epochs, train, label='Train')
    plt.plot(epochs, val, label='Validation')
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

# 5. Main eksekusi
if __name__ == "__main__":
    base_path = "botol_image"  # Ganti jika path kamu beda
    train_dir, val_dir = load_dataset(base_path)
    train_gen, val_gen = do_data_preprocessing(train_dir, val_dir)

    model = create_cnn_model()

    # Training
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        steps_per_epoch=train_gen.samples // train_gen.batch_size,
        epochs=100,
        validation_steps=val_gen.samples // val_gen.batch_size,
    )

    # Save model
    model.save("botol_model.h5")

    # Plot hasil training
    plot_history(history.history["accuracy"], history.history["val_accuracy"], "Training & Validation Accuracy")
    plot_history(history.history["loss"], history.history["val_loss"], "Training & Validation Loss")