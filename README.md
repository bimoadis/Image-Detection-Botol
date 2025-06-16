⚙️ Instalasi
1. Clone Repository
    git clone https://github.com/bimoadis/Image-Detection-Botol.git
    cd Image-Detection-Botol
2. Buat Virtual Environment (Opsional tapi direkomendasikan)

    # Windows
    python -m venv venv
    venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

3. Install Semua Dependensi
    pip install tensorflow keras numpy matplotlib opencv-python pillow flask flask-cors

   
    🧠 Training Model
    Untuk melatih model dari awal:
    python model_training.py
   
    Struktur folder dataset yang diperlukan:
    
    botol_image/
    ├── train/
    │   ├── aqua/
    │   ├── coca-cola/
    │   ├── fanta/
    │   └── teh/
    └── validation/
        ├── aqua/
        ├── coca-cola/
        ├── fanta/
        └── teh/

🔍 Prediksi Manual (dari File Gambar)
python predict_image.py

🌐 Menjalankan API Flask
python app.py

Contoh request menggunakan curl:

curl -X POST -F "image=@test.jpg" http://127.0.0.1:5000/predict

🖥️ Menjalankan Frontend (Opsional)

cd frontend
npm install
npm run dev

✅ Dependensi Utama

tensorflow
keras
numpy
matplotlib
opencv-python
pillow
flask
flask-cors
