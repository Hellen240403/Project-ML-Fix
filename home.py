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
    st.markdown("""
        <style>
        .weather-box {
            background-color: rgba(255,255,255,0.6);
            border-radius: 15px;
            padding: 10px 20px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .weather-item {
            min-width: 150px;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")

    col1, col2 = st.columns([1, 3])
    
    # Kolom kiri: Judul dan tombol
    with col1:
        st.markdown("### 📍 Cuaca Surabaya Hari Ini")
            if st.button("🔄 Refresh"):
               st.cache_data.clear()
    # Kolom kanan: Kartu cuaca
    with col2:
        try:
            weather = get_current_weather()
            st.markdown(f"""
            <div class="weather-box">
                <div class="weather-item">🌡️ <b style="color:#d32f2f;">Suhu:</b> {weather['temperature']}</div>
                <div class="weather-item">💧 <b style="color:#0288d1;">Kelembapan:</b> {weather['humidity']}</div>
                <div class="weather-item">🌬️ <b style="color:#0277bd;">Angin:</b> {weather['wind']}</div>
                <div class="weather-item">🌞 <b style="color:#fbc02d;">UV:</b> {weather['uv']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("📌 Data real-time — Open-Meteo API")
        except Exception as e:
            st.error(f"Data cuaca tidak tersedia: {e}")

    # Expanders
    with st.expander("📘 Pendahuluan"):
        st.info("Isi penjelasan latar belakang di sini.")

    with st.expander("🧠 Metode"):
        st.markdown("""
        - **ANN**    : Artificial Neural Network (ANN) adalah ...
        - **LSTM**   : Long Short-Term Memory (LSTM) ...
        """)

    # Dataset
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
