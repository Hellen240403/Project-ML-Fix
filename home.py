import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=600)
def get_current_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.2575,
        "longitude": 112.7521,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,uv_index",
        "timezone": "Asia/Jakarta"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()["current"]
    return {
        "temperature": f"{data['temperature_2m']}°C",
        "humidity": f"{data['relative_humidity_2m']}%",
        "wind": f"{data['wind_speed_10m']} km/h",
        "uv": f"UV Index {data['uv_index']}"
    }

def app():
    # CSS Custom Style
    st.markdown("""
        <style>
        .weather-row {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        .weather-item {
            background-color: rgba(255,255,255,0.6);
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton > button {
            height: 38px;
            padding: 6px 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Gambar dan Judul
    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")
    st.markdown("### 📍 Cuaca Surabaya Hari Ini")

    # Layout sejajar horizontal (refresh + cuaca)
    weather = None
    try:
        weather = get_current_weather()
    except Exception as e:
        st.error(f"Data cuaca tidak tersedia: {e}")

    st.markdown("<div class='weather-row'>", unsafe_allow_html=True)

    # Tombol Refresh di kiri
    with st.form(key="refresh_form", clear_on_submit=False):
        submit_button = st.form_submit_button(label="🔄 Refresh")
        if submit_button:
            st.cache_data.clear()

    st.markdown("</div>", unsafe_allow_html=True)

    # Info cuaca di kanan
    if weather:
        st.markdown(f"""
            <div class='weather-row'>
                <div class='weather-item'>🌡️ <b style='color:#d32f2f;'>Suhu:</b> {weather['temperature']}</div>
                <div class='weather-item'>💧 <b style='color:#0288d1;'>Kelembapan:</b> {weather['humidity']}</div>
                <div class='weather-item'>🌬️ <b style='color:#0277bd;'>Angin:</b> {weather['wind']}</div>
                <div class='weather-item'>🌞 <b style='color:#fbc02d;'>UV:</b> {weather['uv']}</div>
            </div>
            <div style='margin-top:-5px'>
                <small>📌 Data real-time — Open-Meteo API</small>
            </div>
        """, unsafe_allow_html=True)

    # Expanders
    with st.expander("📘 Pendahuluan"):
        st.info("Isi penjelasan latar belakang di sini.")

    with st.expander("🧠 Metode"):
        st.markdown("""
        - **ANN**    : Artificial Neural Network (ANN) adalah ...
        - **LSTM**   : Long Short-Term Memory (LSTM) ...
        """)

    # Dataset Historikal
    try:
        df = pd.read_csv("data/df_hujan.csv", sep=";")
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        st.subheader("📊 Data Cuaca Surabaya (2023–2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: BMKG")
    except Exception as e:
        st.warning(f"Gagal memuat data historikal: {e}")

if __name__ == "__main__":
    app()
