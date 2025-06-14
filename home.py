import streamlit as st
import pandas as pd
from PIL import Image

# Tambahkan CSS untuk tampilan stylish
def set_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom right, #e0f7fa, #e0f2fe);
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
        </style>
    """, unsafe_allow_html=True)

# Fungsi untuk load data
def load_data(file_path, index_col=None):
    try:
        df = pd.read_csv(file_path, index_col=index_col, sep=';')
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        return df
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return None

# Fungsi utama
def app():
    set_custom_css()

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown('<div class="weather-box">', unsafe_allow_html=True)
        st.subheader("📍 Cuaca Surabaya Hari Ini")
        st.image("asset/home.png", use_container_width=True)
        st.write("🌤️ Suhu: 29°C  \n💧 Kelembapan: 78%  \n💨 Angin: 26 km/h  \n🌞 UV: Ekstrem")
        st.caption("Data dari BMKG, diolah kembali oleh sistem prediksi cuaca.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.title("Platform Prediksi Cuaca Surabaya")
        with st.expander("📘 Pendahuluan", expanded=True):
            tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Tujuan", "Manfaat"])
            with tab1:
                st.info("Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer...")
            with tab2:
                st.success("Tujuan dari penelitian ini adalah membangun model prediksi cuaca menggunakan ANN dan LSTM...")
            with tab3:
                st.warning("Penelitian ini bermanfaat untuk meningkatkan akurasi prediksi cuaca dan kesiapsiagaan...")

        with st.expander("🧠 Metode"):
            st.markdown("""
            - **Artificial Neural Network (ANN)**: mengenali pola
            - **Long Short-Term Memory (LSTM)**: memproses data sekuensial cuaca
            """)

    # Load data cuaca historis
    df = load_data("data/df_hujan.csv")
    if df is not None:
        st.divider()
        st.subheader("📊 Data Cuaca Surabaya (2023–2025)")
        st.dataframe(df, use_container_width=True)
        st.caption("📌 Sumber: [BMKG](https://dataonline.bmkg.go.id/home)")

# Jalankan
if __name__ == "__main__":
    app()
