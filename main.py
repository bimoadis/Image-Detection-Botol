import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from tkinter import Tk, filedialog

# === 1. Load model ===
model = load_model("botol_model.h5") 

# === 2. Daftar label ===
class_labels = ['aqua', 'coca-cola', 'fanta', 'teh']

# === 3. Buka file dialog untuk memilih gambar ===
root = Tk()
root.withdraw() 
file_paths = filedialog.askopenfilenames(
    title="Pilih gambar untuk diklasifikasikan",
    filetypes=[("Image files", "*.jpg *.jpeg *.png")]
)

# === 4. Loop file yang dipilih ===
for filepath in file_paths:
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (150, 150))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Prediksi
    pred = model.predict(img)[0]
    label_index = np.argmax(pred)
    confidence = pred[label_index]
    label = class_labels[label_index]

    print(f"{filepath} -> Prediksi: {label} ({confidence:.2f})")

    # Tampilkan gambar dan hasil
    plt.imshow(cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB))
    plt.title(f"{label} ({confidence:.2f})")
    plt.axis('off')
    plt.show()
