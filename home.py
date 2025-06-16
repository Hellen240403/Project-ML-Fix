import streamlit as st
import pandas as pd
import requests
from PIL import Image

# ------------------------------------------------------------------ #
#  CONFIG ACCUWEATHER API
# ------------------------------------------------------------------ #
# Pastikan ACCUWEATHER_KEY sudah ditambahkan ke .streamlit/secrets.toml
API_KEY = "xQGm4v0qhpHLusHsjGGA5O2GJPNXAQSO"
LOCATION_KEY = "203449"  # Surabaya

@st.cache_data(ttl=600)
def get_current_weather():
    """Ambil cuaca terkini Surabaya dari Open-Meteo (tanpa API key)"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.2575,      # Koordinat Surabaya
        "longitude": 112.7521,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,uv_index",
        "timezone": "Asia/Jakarta"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()["current"]

    return {
        "temperature": f"{data['temperature_2m']}°C",
        "humidity"   : f"{data['relative_humidity_2m']}%",
        "wind"       : f"{data['wind_speed_10m']} km/h",
        "uv"         : f"UV Index {data['uv_index']}"
    }

# ------------------------------------------------------------------ #
#  CSS
# ------------------------------------------------------------------ #
def set_custom_css():
    st.markdown("""
    <style>
     .stApp { background:white; font-family:'Segoe UI',sans-serif; }
     .weather-card {
        background: rgba(255,255,255,0.6);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,.1);
        width: max-content;
     }
     .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        color: #1e293b;
        font-weight: bold;
        border-radius: 10px;
     }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------ #
#  DATASET LOCAL
# ------------------------------------------------------------------ #
def load_data(path):
    try:
        df = pd.read_csv(path, sep=';')
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        return df
    except Exception as e:
        st.warning(f"Gagal memuat data historikal: {e}")
        return None

# ------------------------------------------------------------------ #
#  MAIN PAGE
# ------------------------------------------------------------------ #
def app():
    set_custom_css()

    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")

    col1, col2 = st.columns([1, 1.3])

    # ---------------- Judul Kotak ---------------- #
    with col1:
        st.markdown("""
        <div style="background:#f0f3fa;padding:20px 30px;border-radius:12px;
                    box-shadow:2px 2px 10px rgba(0,0,0,.1); width:max-content;">
           <h3 style="margin:0;">📍 Cuaca Surabaya Hari Ini</h3>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- Kartu Cuaca ---------------- #
    with col2:
        weather = None
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
    
        try:
            weather = get_current_weather()
        except Exception as e:
            st.error(f"Data cuaca tidak tersedia: {e}")
            
        if weather:
            st.markdown(f"""
            <div class="weather-card" style="margin: 10px 0 10px 10px; padding: 15px 25px;">
              <div style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  flex-wrap: wrap;
                  gap: 20px;
                  font-size: 16px;
                  min-width: 500px;
                  ">
                <div style="min-width: 120px;">🌡️ <b style="color:#d32f2f;">Suhu:</b> {weather['temperature']}</div>
                <div style="min-width: 150px;">💧 <b style="color:#0288d1;">Kelembapan:</b> {weather['humidity']}</div>
                <div style="min-width: 140px;">🌬️ <b style="color:#0277bd;">Angin:</b> {weather['wind']}</div>
                <div style="min-width: 130px;">🌞 <b style="color:#fbc02d;">UV:</b> {weather['uv']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    
            st.caption("📌 Data real-time — AccuWeather API")


    # ------------- Penjelasan & Dataset ---------- #
    with st.expander("📘 Pendahuluan", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📖 Latar Belakang", "🎯 Tujuan", "🎁 Manfaat"])
        with tab1:
            st.info("…ringkasan latar belakang…")
        with tab2:
            st.success("…ringkasan tujuan…")
        with tab3:
            st.warning("…ringkasan manfaat…")

    with st.expander("🧠 Metode"):
        st.markdown("- 🤖 **ANN** - 🔁 **LSTM**")

    df = load_data("data/df_hujan.csv")
    if df is not None:
        st.divider()
        st.subheader("📊 Data Cuaca Surabaya (2023-2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: BMKG")

# ------------------------------------------------------------------ #
if __name__ == "__main__":
    app()
