import streamlit as st
import math
import time

def get_weather_prediction(temperature, humidity, wind_speed, cloud_code):
    """
    Fungsi ini mereplikasi logika prediksi berbasis aturan dari notebook.
    Model ANN yang dilatih di notebook tidak digunakan di sini, sesuai dengan implementasi asli.
    """
    
    # 1. Kategori Suhu (hanya untuk display)
    if temperature < 20:
        temp_category = "Dingin"
    elif temperature < 30:
        temp_category = "Sejuk"
    else:
        temp_category = "Panas"

    # 2. Aturan Prediksi Cuaca Awal berdasarkan Kelembapan
    if humidity < 30:
        prediction = "Cerah"
        prob = 0.1
    elif humidity < 60:
        # Notebook memiliki logika `if humidity > 30` di dalam, yang selalu benar di blok ini.
        # Saya sederhanakan menjadi satu kondisi.
        prediction = "Berawan"
        prob = 0.4
    else: # humidity >= 60
        # Notebook memiliki logika `if kel < 25`, yang tidak akan pernah tercapai di blok ini.
        # Saya asumsikan ini kesalahan ketik dan seharusnya `temp < 25`.
        # Namun, untuk setia pada notebook, saya akan mengikuti logika aslinya yang hanya akan jatuh ke 'Hujan Sedang'.
        prediction = "Hujan Sedang"
        prob = 0.9

    # 3. Menyesuaikan Prediksi berdasarkan Kode Awan
    if cloud_code in [1, 2]:  # Cumulus atau Cirrus
        if prediction in ["Gerimis", "Hujan Sedang"]:
            prediction = "Cerah Berawan"
            prob *= 0.5
    elif cloud_code == 3:  # Stratus
        if prediction == "Cerah":
            prediction = "Gerimis"
            prob = max(prob, 0.5)
    elif cloud_code == 4:  # Nimbostratus
        if prediction in ["Cerah", "Berawan", "Gerimis"]:
            prediction = "Hujan Sedang"
            prob = max(prob, 0.7)
    elif cloud_code == 5:  # Cumulonimbus
        if prediction != "Hujan Sedang":
            prediction = "Hujan Lebat"
            prob = max(prob, 0.9)

    # 4. Menghitung Kevalidan
    if prediction == "Cerah":
        tengah, batas_bawah, batas_atas = 0.1, 0.0, 0.25
    elif prediction == "Berawan" or prediction == "Cerah Berawan":
        tengah, batas_bawah, batas_atas = 0.375, 0.26, 0.5
    elif prediction == "Gerimis":
        tengah, batas_bawah, batas_atas = 0.63, 0.51, 0.75
    else: # Hujan Sedang atau Hujan Lebat
        tengah, batas_bawah, batas_atas = 0.88, 0.76, 1.0
    
    maks_jarak = (batas_atas - batas_bawah) / 2
    if maks_jarak == 0:
        validity = 0.0
    else:
        validity = math.exp(-((prob - tengah) ** 2) / (2 * (maks_jarak ** 2))) * 100
    
    validity = round(validity, 2)

    return {
        "prediction": prediction,
        "probability": f"{prob:.2f}",
        "validity": validity,
        "temp_category": temp_category
    }


def app():
    st.title("Prediksi Cuaca Berbasis Aturan 🌦️")
    st.markdown("Masukkan parameter cuaca untuk mendapatkan prediksi berdasarkan sistem berbasis aturan.")
    
    st.divider()

    # --- Input dari Pengguna ---
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.number_input('Masukkan Nilai Temperatur (°C)', min_value=-10.0, max_value=50.0, value=24.0, format="%.1f")
        humidity = st.number_input('Masukkan Nilai Kelembapan (%)', min_value=0.0, max_value=100.0, value=90.0, format="%.1f")
    
    with col2:
        wind_speed = st.number_input('Masukkan Nilai Kecepatan Angin (km/jam)', min_value=0.0, max_value=100.0, value=25.0, format="%.1f")
        
        cloud_options = {
            "Cumulus": 1,
            "Cirrus": 2,
            "Stratus": 3,
            "Nimbostratus": 4,
            "Cumulonimbus": 5
        }
        
        cloud_name = st.selectbox(
            "Pilih Jenis Awan",
            options=cloud_options.keys(),
            index=3  # Default ke Nimbostratus sesuai contoh
        )
        cloud_code = cloud_options[cloud_name]

    # --- Tombol Prediksi ---
if st.button('🚀 Mulai Prediksi Cuaca', use_container_width=True, type="primary"):
    with st.spinner('🔍 Menganalisis cuaca...'):
        time.sleep(1.5)  # Simulasi proses
        results = get_weather_prediction(temperature, humidity, wind_speed, cloud_code)

    prediction = results["prediction"]
    probability = results["probability"]
    validity = results["validity"]
    temp_category = results["temp_category"]

    st.markdown("### 🌤️ Hasil Prediksi Cuaca Hari Ini")

    # --- Tentukan Emoji & Warna Background Dinamis ---
    prediction_lower = prediction.lower()
    emoji = "🌤️"
    bg_color = "#f0f2f6"  # default background

    if "cerah" in prediction_lower:
        emoji = "☀️"
        bg_color = "#FFF7D6"
    elif "berawan" in prediction_lower:
        emoji = "☁️"
        bg_color = "#E0E7FF"
    elif "gerimis" in prediction_lower:
        emoji = "🌦️"
        bg_color = "#D0F0FF"
    elif "hujan sedang" in prediction_lower:
        emoji = "🌧️"
        bg_color = "#B0DAFF"
    elif "hujan lebat" in prediction_lower:
        emoji = "⛈️"
        bg_color = "#A3BFFA"

    # --- Hasil Prediksi dalam Kartu Stylish ---
    st.markdown(f"""
    <div style='
        background-color: {bg_color};
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    '>
        <h1 style='text-align: center; font-size: 3rem;'>{emoji} {prediction}</h1>
        <p style='text-align: center; font-size: 1.1rem;'>Prediksi cuaca berdasarkan input parameter yang Anda masukkan.</p>
        <div style='display: flex; justify-content: space-around; padding-top: 1rem;'>
            <div style='text-align: center;'>
                <h3>📊 Probabilitas</h3>
                <p style='font-size: 1.5rem; font-weight: bold;'>{probability}</p>
            </div>
            <div style='text-align: center;'>
                <h3>✅ Kevalidan</h3>
                <p style='font-size: 1.5rem; font-weight: bold;'>{validity}%</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Detail Parameter Input dengan Emoji ---
    st.markdown("#### 📌 Detail Parameter yang Diberikan:")
    st.markdown(f"""
    - 🌡️ **Temperatur:** `{temperature}°C` ({temp_category})  
    - 💧 **Kelembapan:** `{humidity}%`  
    - 🌬️ **Kecepatan Angin:** `{wind_speed} km/jam`  
    - ☁️ **Jenis Awan:** `{cloud_name}`
    """)

    # --- Tips Tambahan Jika Hujan ---
    if "hujan" in prediction_lower:
        st.info("💡 *Tips*: Jangan lupa bawa payung atau jas hujan ya!")

    st.success("✅ Prediksi berhasil ditampilkan dengan tampilan interaktif!")
