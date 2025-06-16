from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
from keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load model hanya sekali
model = load_model("botol_model.h5")
class_labels = ['aqua', 'coca-cola', 'fanta', 'teh']

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img = img.resize((150, 150))
    img = np.array(img).astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0]
    label_index = np.argmax(pred)
    confidence = float(pred[label_index])
    label = class_labels[label_index]

    return jsonify({
        'label': label,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
