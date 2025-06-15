import streamlit as st
import pandas as pd
from PIL import Image

# ---------------------------- CSS Styling ----------------------------
def set_custom_css():
    st.markdown("""
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
            background-color: rgba(255, 255, 255, 0.6);
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
    """, unsafe_allow_html=True)

# ---------------------------- Data Loader ----------------------------
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

# ---------------------------- Main App ----------------------------
def app():
    set_custom_css()

    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")

    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.markdown("""
        <div style="background-color: #f0f3fa; padding: 20px; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style='color: #000000; margin: 0;'>📍 Cuaca Surabaya Hari Ini</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='weather-box'>
            <ul style="list-style: none; padding-left: 0; margin: 0; font-size: 16px;">
                <li>🌡️ <span style="font-weight:bold; color:#d32f2f;">Suhu:</span> 29°C</li>
                <li>💧 <span style="font-weight:bold; color:#0288d1;">Kelembapan:</span> 78%</li>
                <li>🌬️ <span style="font-weight:bold; color:#0277bd;">Angin:</span> 26 km/h</li>
                <li>🌞 <span style="font-weight:bold; color:#fbc02d;">UV:</span> Ekstrem</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.caption("📌 Data dari BMKG, diolah kembali oleh sistem prediksi cuaca.")

    with st.expander("📘 Pendahuluan", expanded=True):
        tab1, tab2, tab3 = st.tabs(["📖 Latar Belakang", "🎯 Tujuan", "🎁 Manfaat"])

        with tab1:
            st.info("""
            Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan dengan menganalisis data meteorologi. Kota Surabaya sebagai kota metropolitan sangat membutuhkan informasi cuaca yang akurat. Dengan demikian, penelitian ini bertujuan untuk membangun model prediksi cuaca yang akurat demi mendukung aktivitas masyarakat.
            """)

        with tab2:
            st.success("""
            1. Membangun model prediksi cuaca Surabaya dengan ANN dan LSTM.
            2. Mengoptimalkan akurasi prediksi menggunakan data BMKG 2023–2025.
            3. Menilai performa ANN vs LSTM.
            4. Memberikan kontribusi AI dalam prediksi cuaca lokal.
            """)

        with tab3:
            st.warning("""
            1. Masyarakat dapat merencanakan aktivitas lebih baik.
            2. Pemerintah & sektor penting bisa mengambil keputusan lebih tepat.
            3. Deteksi dini potensi cuaca ekstrem.
            4. Kontribusi terhadap pengembangan AI untuk prediksi cuaca.
            5. Peningkatan pemahaman cuaca tropis di Surabaya.
            """)

    with st.expander("🧠 Metode"): 
        st.markdown("""
        - 🤖 **Artificial Neural Network (ANN)**: Mengenali pola data non-linear  
        - 🔁 **Long Short-Term Memory (LSTM)**: Menangani data sekuensial cuaca jangka panjang
        """)

    df = load_data("data/df_hujan.csv")
    if df is not None:
        st.divider()
        st.subheader("📊 Data Cuaca Surabaya (2023–2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: [BMKG](https://dataonline.bmkg.go.id/home)")

# ---------------------------- Run App ----------------------------
if __name__ == "__main__":
    app()
