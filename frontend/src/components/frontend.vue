<template>
  <div class="page">
    <div class="container">
      <h1 class="title">🧃Validasi Botol Minuman</h1>

      <!-- Area Upload -->
      <div
        v-if="!previewUrl"
        class="upload-area"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input type="file" ref="fileInput" @change="onFileChange" hidden />
        <p class="upload-text">
          Seret dan lepaskan gambar di sini<br />
          atau klik untuk memilih gambar
        </p>
      </div>

      <!-- Hasil Preview dan Prediksi -->
      <div v-if="previewUrl" class="result-wrapper">
        <!-- Preview Gambar -->
        <div class="card preview-card">
          <h2 class="card-title">Preview Gambar</h2>
          <div class="image-box">
            <img :src="previewUrl" alt="Preview Gambar" class="preview-img" />
          </div>
        </div>

        <!-- Hasil Prediksi -->
        <div v-if="prediction" class="card prediction-card">
          <h2 class="card-title">Hasil Prediksi</h2>
          <p><strong>Label:</strong> {{ prediction.label }}</p>
          <p><strong>Validasi:</strong> {{ (prediction.confidence * 100).toFixed(2) }}%</p>
        </div>
      </div>

      <!-- Tombol -->
      <div class="form-group">
        <button @click="submitImage" :disabled="!image || loading">
          Kirim Gambar
        </button>
        <button class="reset-btn" @click="resetForm">Reset</button>
        <div v-if="loading" class="loading">Sedang memproses gambar...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const image = ref(null)
const previewUrl = ref(null)
const prediction = ref(null)
const loading = ref(false)
const fileInput = ref(null)

function onFileChange(event) {
  const file = event.target.files[0]
  handleFile(file)
}

function handleDrop(event) {
  const file = event.dataTransfer.files[0]
  handleFile(file)
}

function handleFile(file) {
  if (file && file.type.startsWith("image/")) {
    image.value = file
    previewUrl.value = URL.createObjectURL(file)
    prediction.value = null
  } else {
    alert("File harus berupa gambar (jpg/png).")
  }
}

function triggerFileInput() {
  fileInput.value.click()
}

async function submitImage() {
  if (!image.value) return
  const formData = new FormData()
  formData.append("image", image.value)
  loading.value = true
  prediction.value = null

  try {
    const res = await axios.post("http://127.0.0.1:5000/predict", formData)

    if (res.status === 200 && res.data.label && res.data.confidence !== undefined) {
      prediction.value = res.data
    } else {
      alert("Respons tidak sesuai harapan")
    }
  } catch (err) {
    alert("Gagal mengirim gambar")
    console.error(err)
  } finally {
    loading.value = false
  }
}

function resetForm() {
  image.value = null
  previewUrl.value = null
  prediction.value = null
}
</script>

<style scoped>
/* Layout Umum */
.page {
  min-height: 100vh;
  background-color: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.container {
  background: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  max-width: 900px;
  width: 100%;
}

.title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 1.5rem;
}

/* Upload Area */
.upload-area {
  border: 2px dashed #a0aec0;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 2rem;
}

.upload-area:hover {
  background-color: #f0f4f8;
}

.upload-text {
  color: #555;
  font-size: 16px;
}

/* Result Layout */
.result-wrapper {
  display: flex;
  gap: 1.5rem;
  margin-top: 1.5rem;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
}

/* Card Umum */
.card {
  border: 1px solid #e0e0e0;
  padding: 1rem;
  border-radius: 12px;
  background-color: #fff;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #444;
}

/* Preview */
.preview-card {
  flex: 7;
}

.preview-card .image-box {
  max-width: 70%;
  max-height: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}

/* Prediction */
.prediction-card {
  flex: 3;
}

/* Button */
.form-group {
  text-align: center;
  margin: 1.5rem 0;
}

button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  margin: 0 0.5rem;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #1d4ed8;
}

button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.reset-btn {
  background-color: #ef4444;
}

.reset-btn:hover {
  background-color: #dc2626;
}

/* Loading */
.loading {
  color: #666;
  font-size: 14px;
  margin-top: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .result-wrapper {
    flex-direction: column;
  }

  .preview-card,
  .prediction-card {
    flex: 1 1 100%;
  }
}
</style>
