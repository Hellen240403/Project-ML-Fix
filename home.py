import streamlit as st
import pandas as pd
from PIL import Image
import requests

# ---------------------------- API Configuration ----------------------------
API_KEY = "YOUR_ACCUWEATHER_API_KEY"  # Ganti dengan API key Anda
LOCATION_KEY = "203449"  # Location Key untuk Surabaya dari AccuWeather

def get_current_weather():
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{LOCATION_KEY}"
    params = {"apikey": API_KEY, "details": True}
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()[0]
        return {
            "temperature": f"{data['Temperature']['Metric']['Value']}°C",
            "humidity": f"{data['RelativeHumidity']}%",
            "wind": f"{data['Wind']['Speed']['Metric']['Value']} km/h",
            "uv": f"{data['UVIndexText']}",
        }
    except Exception as e:
        st.error(f"❌ Gagal mengambil data cuaca: {e}")
        return None

# ---------------------------- CSS Styling ----------------------------
def set_custom_css():
    st.markdown(\"\"\"
        <style>
        .stApp {
            background-color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .big-logo img {
            width: 90%;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            margin-bottom: 10px;
        }
        .weather-box {
            background-color: #ffffffcc;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f5f9;
            color: #1e293b;
            font-weight: bold;
            border-radius: 10px;
        }
        .metric {
            font-size: 18px !important;
        }
        </style>
    \"\"\", unsafe_allow_html=True)

# ---------------------------- Data Loader ----------------------------
def load_data(file_path, index_col=None):
    try:
        df = pd.read_csv(file_path, index_col=index_col, sep=';')
        df.columns = df.columns.str.strip().str.lower().str.replace('\\ufeff', '')
        return df
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return None

# ---------------------------- Main App ----------------------------
def app():
    set_custom_css()

    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")

    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.markdown(\"\"\"
        <div style="background-color: #f0f3fa; padding: 20px; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style='color: #000000; margin: 0;'>📍 Cuaca Surabaya Hari Ini</h3>
        </div>
        \"\"\", unsafe_allow_html=True)

    with col2:
        weather = get_current_weather()
        if weather:
            st.markdown(f\"\"\"
            <div style="border-radius: 18px; padding: 20px; margin-bottom: 5px; width: fit-content;">
                <ul style="list-style: none; padding-left: 0; margin: 0; font-size: 16px;">
                    <li>🌡️ <span style="font-weight:bold; color:#d32f2f;">Suhu:</span> {weather['temperature']}</li>
                    <li>💧 <span style="font-weight:bold; color:#0288d1;">Kelembapan:</span> {weather['humidity']}</li>
                    <li>🌬️ <span style="font-weight:bold; color:#0277bd;">Angin:</span> {weather['wind']}</li>
                    <li>🌞 <span style="font-weight:bold; color:#fbc02d;">UV:</span> {weather['uv']}</li>
                </ul>
            </div>
            \"\"\", unsafe_allow_html=True)
            st.caption("📌 Data real-time dari AccuWeather")
        else:
            st.warning("Data cuaca tidak tersedia saat ini.")

    with st.expander("📘 Pendahuluan", expanded=True):
        tab1, tab2, tab3 = st.tabs(["📖 Latar Belakang", "🎯 Tujuan", "🎁 Manfaat"])

        with tab1:
            st.info(\"\"\"
            (Isi latar belakang sesuai sebelumnya)
            \"\"\")

        with tab2:
            st.success(\"\"\"
            (Isi tujuan sesuai sebelumnya)
            \"\"\")
        
        with tab3:
            st.warning(\"\"\"
            (Isi manfaat sesuai sebelumnya)
            \"\"\")

    with st.expander("🧠 Metode"): 
        st.markdown(\"\"\"
        - 🤖 **Artificial Neural Network (ANN)**: Mengenali pola data non-linear
        - 🔁 **Long Short-Term Memory (LSTM)**: Menangani data sekuensial cuaca jangka panjang
        \"\"\")

    df = load_data("data/df_hujan.csv")
    if df is not None:
        st.divider()
        st.subheader("📊 Data Cuaca Surabaya (2023–2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: [BMKG](https://dataonline.bmkg.go.id/home)")

# ---------------------------- Run App ----------------------------
if __name__ == "__main__":
    app()
"""

corrected_combined_code[:1500]  # Previewing a portion of the full code due to length
