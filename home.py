import streamlit as st
import pandas as pd
from PIL import Image

# ===== Styling CSS =====
st.markdown("""
    <style>
    /* Background gradien */
    .stApp {
        background: linear-gradient(135deg, #89f7fe, #66a6ff);
        color: #000000;
    }

    /* Judul besar dengan bayangan */
    .big-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        margin-top: 20px;
        color: #ffffff;
    }

    /* Card box untuk info */
    .info-box {
        background-color: rgba(255,255,255,0.8);
        padding: 20px;
        border-radius: 16px;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ===== Gambar Besar =====
try:
    logomain = Image.open("asset/home.png")
    st.image(logomain, use_container_width=True)
except Exception as e:
    st.warning(f"Gagal memuat gambar: {e}")

# ===== Judul & Deskripsi =====
st.markdown('<div class="big-title">🌤️ Prediksi Cuaca Kota Surabaya</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.write("""
        Selamat datang di platform prediksi cuaca Kota Surabaya!  
        Aplikasi ini menggunakan teknologi Machine Learning (ANN & LSTM) berbasis data dari BMKG 
        untuk memberikan prediksi cuaca yang akurat.  
        🌧️☀️🌬️🌈  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== Load Data Cuaca =====
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/df_hujan.csv", sep=";")
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        return df
    except Exception as e:
        st.error(f"❌ Gagal memuat data cuaca: {e}")
        return None

df = load_data()
if df is not None:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.subheader("📊 Data Cuaca Surabaya 2023–2025")
    st.dataframe(df, use_container_width=True)
    st.caption("📌 Data diperoleh dari BMKG: https://dataonline.bmkg.go.id/home")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.stop()
