import streamlit as st
import math
import time

def get_weather_prediction(temperature, humidity, wind_speed, cloud_code):
    if temperature < 20:
        temp_category = "Dingin"
    elif temperature < 30:
        temp_category = "Sejuk"
    else:
        temp_category = "Panas"

    if humidity < 30:
        prediction = "Cerah"
        prob = 0.1
    elif humidity < 60:
        prediction = "Berawan"
        prob = 0.4
    else:
        prediction = "Hujan Sedang"
        prob = 0.9

    if cloud_code in [1, 2]:
        if prediction in ["Gerimis", "Hujan Sedang"]:
            prediction = "Cerah Berawan"
            prob *= 0.5
    elif cloud_code == 3:
        if prediction == "Cerah":
            prediction = "Gerimis"
            prob = max(prob, 0.5)
    elif cloud_code == 4:
        if prediction in ["Cerah", "Berawan", "Gerimis"]:
            prediction = "Hujan Sedang"
            prob = max(prob, 0.7)
    elif cloud_code == 5:
        if prediction != "Hujan Sedang":
            prediction = "Hujan Lebat"
            prob = max(prob, 0.9)

    if prediction == "Cerah":
        tengah, batas_bawah, batas_atas = 0.1, 0.0, 0.25
    elif prediction in ["Berawan", "Cerah Berawan"]:
        tengah, batas_bawah, batas_atas = 0.375, 0.26, 0.5
    elif prediction == "Gerimis":
        tengah, batas_bawah, batas_atas = 0.63, 0.51, 0.75
    else:
        tengah, batas_bawah, batas_atas = 0.88, 0.76, 1.0

    maks_jarak = (batas_atas - batas_bawah) / 2
    validity = math.exp(-((prob - tengah) ** 2) / (2 * (maks_jarak ** 2))) * 100 if maks_jarak else 0.0
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

    cloud_options = {
        "Cumulus": {"code": 1, "img": "asset/cumulus.jpg"},
        "Cirrus": {"code": 2, "img": "asset/cirrus.jpg"},
        "Stratus": {"code": 3, "img": "asset/stratus.jpg"},
        "Nimbostratus": {"code": 4, "img": "asset/nimbostratus.jpg"},
        "Cumulonimbus": {"code": 5, "img": "asset/cumulonimbus.jpg"},
    }

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider('🌡️ Temperatur (°C)', -10.0, 50.0, 24.0, 0.5)
        humidity = st.slider('💧 Kelembapan Udara (%)', 0.0, 100.0, 90.0, 1.0)
    with col2:
        wind_speed = st.slider('🌬️ Kecepatan Angin (km/jam)', 0.0, 100.0, 25.0, 1.0)
        cloud_name = st.radio("☁️ Pilih Jenis Awan:", options=list(cloud_options.keys()), horizontal=True)

    st.image(cloud_options[cloud_name]["img"], caption=f"☁️ Jenis Awan: {cloud_name}", use_container_width=True)
    cloud_code = cloud_options[cloud_name]["code"]

    if st.button('🚀 Mulai Prediksi Cuaca', use_container_width=True, type="primary"):
        with st.spinner('🔍 Menganalisis cuaca...'):
            time.sleep(1.5)
            results = get_weather_prediction(temperature, humidity, wind_speed, cloud_code)

        prediction = results["prediction"]
        probability = results["probability"]
        validity = results["validity"]
        temp_category = results["temp_category"]

        st.markdown("### 🌤️ Hasil Prediksi Cuaca Hari Ini")

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

        if "hujan" in prediction_lower:
            st.info("💡 *Tips*: Jangan lupa bawa payung atau jas hujan ya!")

        st.success("✅ Prediksi berhasil ditampilkan dengan tampilan interaktif!")

# Jalankan aplikasi
if __name__ == "__main__":
    app()
