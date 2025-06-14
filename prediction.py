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
    st.markdown("## ☁️ Masukkan Parameter Cuaca")
    st.markdown("Lengkapi data berikut untuk memprediksi cuaca berdasarkan parameter atmosfer dan jenis awan yang dipilih:")

# --- Pilihan Jenis Awan + Gambar ---
    cloud_options = {
        "Cumulus": {"code": 1, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/CumulusCloud.jpg/320px-CumulusCloud.jpg"},
        "Cirrus": {"code": 2, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Cirrus_clouds2.jpg/320px-Cirrus_clouds2.jpg"},
        "Stratus": {"code": 3, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Stratus_clouds_over_Beacon_Hill.jpg/320px-Stratus_clouds_over_Beacon_Hill.jpg"},
        "Nimbostratus": {"code": 4, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Nimbostratus_Clouds.jpg/320px-Nimbostratus_Clouds.jpg"},
        "Cumulonimbus": {"code": 5, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cumulonimbus_over_Lake_Victoria.jpg/320px-Cumulonimbus_over_Lake_Victoria.jpg"},
    }
    
    # --- Input Pengguna ---
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.slider(
            '🌡️ Temperatur (°C)',
            min_value=-10.0,
            max_value=50.0,
            value=24.0,
            step=0.5,
            help="Geser untuk mengatur suhu udara"
        )
        humidity = st.slider(
            '💧 Kelembapan Udara (%)',
            min_value=0.0,
            max_value=100.0,
            value=90.0,
            step=1.0,
            help="Kelembapan relatif di udara"
        )
    
    with col2:
        wind_speed = st.slider(
            '🌬️ Kecepatan Angin (km/jam)',
            min_value=0.0,
            max_value=100.0,
            value=25.0,
            step=1.0,
            help="Kecepatan angin di permukaan"
        )
    
        st.markdown("### 🖼️ Pilih Jenis Awan")
        cloud_name = st.radio(
            "📸 Klik salah satu gambar awan berikut untuk memilih:",
            options=list(cloud_options.keys()),
            format_func=lambda x: f"🌥️ {x}",
            horizontal=True
        )
    
    # --- Gambar Awan yang Dipilih ---
    st.image(
        cloud_options[cloud_name]["img"],
        caption=f"☁️ Jenis Awan: {cloud_name}",
        use_container_width=True
    )
    
    cloud_code = cloud_options[cloud_name]["code"]
    
    # --- Tombol Prediksi Cuaca ---
    if st.button('🚀 Mulai Prediksi Cuaca', use_container_width=True, type="primary"):
        with st.spinner('🔍 Menganalisis cuaca...'):
            time.sleep(1.5)  # Simulasi
    
            # Ganti dengan model prediksi milik Anda
            results = get_weather_prediction(temperature, humidity, wind_speed, cloud_code)
    
        prediction = results["prediction"]
        probability = results["probability"]
        validity = results["validity"]
        temp_category = results["temp_category"]
    
        st.markdown("### 🌤️ Hasil Prediksi Cuaca Hari Ini")
    
        # Tambahkan emoji sesuai hasil prediksi
        emoji = "🌤️"
        prediction_lower = prediction.lower()
        if "cerah" in prediction_lower:
            emoji = "☀️"
        elif "berawan" in prediction_lower:
            emoji = "☁️"
        elif "gerimis" in prediction_lower:
            emoji = "🌦️"
        elif "hujan sedang" in prediction_lower:
            emoji = "🌧️"
        elif "hujan lebat" in prediction_lower:
            emoji = "⛈️"
    
        col_res1, col_res2, col_res3 = st.columns(3)
    
        with col_res1:
            if "hujan" in prediction_lower or "gerimis" in prediction_lower:
                st.error(f"**{emoji} {prediction}**")
            elif "berawan" in prediction_lower:
                st.warning(f"**{emoji} {prediction}**")
            else:
                st.success(f"**{emoji} {prediction}**")
    
        with col_res2:
            st.metric("📊 Probabilitas", value=probability)
    
        with col_res3:
            st.metric("✅ Kevalidan", value=f"{validity}%")
    
        st.caption(f"""
        📌 **Detail input**:  
        🌡️ Temperatur: **{temperature}°C** ({temp_category})  
        💧 Kelembapan: **{humidity}%**  
        🌬️ Kecepatan Angin: **{wind_speed} km/jam**  
        ☁️ Awan: **{cloud_name}**
        """)

    # --- Tips Tambahan Jika Hujan ---
    if "hujan" in prediction_lower:
        st.info("💡 *Tips*: Jangan lupa bawa payung atau jas hujan ya!")
    
    st.success("✅ Prediksi berhasil ditampilkan dengan tampilan interaktif!")
