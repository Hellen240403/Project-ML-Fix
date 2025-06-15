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

@st.cache_data(ttl=600)  # cache 10 menit
def get_current_weather():
    """Ambil cuaca Surabaya terkini dari AccuWeather API"""
    url    = f"https://dataservice.accuweather.com/currentconditions/v1/{LOCATION_KEY}"
    params = {"apikey": API_KEY, "details": True, "language": "id-id"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()[0]
    return {
        "temperature": f"{data['Temperature']['Metric']['Value']}°C",
        "humidity"   : f"{data['RelativeHumidity']}%",
        "wind"       : f"{data['Wind']['Speed']['Metric']['Value']} km/h",
        "uv"         : data["UVIndexText"]
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
        try:
            weather = get_current_weather()
        except Exception as e:
            st.error(f"Data cuaca tidak tersedia: {e}")
            
        if weather:
            st.markdown(f"""
            <div class="weather-card" style="margin-left:10px;">
              <ul style="
                  list-style:none;
                  margin:0;
                  padding:0;
                  font-size:16px;
                  display:flex;
                  gap:30px;
                  flex-wrap:wrap;
                  align-items:center;">
                <li>🌡️ <b style="color:#d32f2f;">Suhu:</b> {weather['temperature']}</li>
                <li>💧 <b style="color:#0288d1;">Kelembapan:</b> {weather['humidity']}</li>
                <li>🌬️ <b style="color:#0277bd;">Angin:</b> {weather['wind']}</li>
                <li>🌞 <b style="color:#fbc02d;">UV:</b> {weather['uv']}</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)
            st.caption("📌 Data real-time — AccuWeather API")
        st.markdown("</div>", unsafe_allow_html=True)

            weather = None
        if st.button("🔄 Refresh"):
            st.cache_data.clear()

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
