import streamlit as st
import pandas as pd
from PIL import Image

# ---------------------------- CSS Styling ----------------------------
def set_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom right, #e0f7fa, #e0f2fe);
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
        <div class='weather-box' style="
            background-color: rgba(255, 255, 255, 0.6);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        ">
            <ul style="list-style: none; padding-left: 0; margin: 0; font-size: 16px;">
                <li>🌡️ <b>Suhu:</b> 29°C</li>
                <li>💧 <b>Kelembapan:</b> 78%</li>
                <li>🌬️ <b>Angin:</b> 26 km/h</li>
                <li>🌞 <b>UV:</b> Ekstrem</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.caption("📌 Data dari BMKG, diolah kembali oleh sistem prediksi cuaca.")

    with st.expander("📘 Pendahuluan", expanded=True):
        tab1, tab2, tab3 = st.tabs(["📖 Latar Belakang", "🎯 Tujuan", "🎁 Manfaat"])

        with tab1:
            st.info("""
            Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan yang dilakukan dengan menganalisis data meteorologi yang ada. Perkembangannya teknologi dan metode yang terus membuat banyak pilihan untuk memprediksi cuaca dengan sangat canggih. Proses ini melibatkan penggunaan berbagai metode statistika dan algoritma pemrograman untuk memodelkan dinamika atmosfer. Berbagai parameter cuaca seperti suhu, kelembapan, tekanan udara, kecepatan angin, dan curah hujan digunakan untuk membuat ramalan cuaca yang dapat memberikan informasi kepada masyarakat untuk kegiatan sehari-hari. Dalam era teknologi yang semakin maju, prediksi menjadi lebih akurat dan dapat diakses dengan mudah melalui berbagai platform digital, memberikan kemudahan bagi masyarakat dalam merencanakan aktivitas mereka.
            Kota Surabaya merupakan salah satu kota metropolitan dan kota besar di Indonesia dengan berbagai aktivitas ekonomi, sosial, dan budaya yang sangat tinggi. Aktifitas masyarakat Kota Surabaya sangat padat pada jam tertentu karena kegiatan yang dilakukan secara bersama. Masyarakat dituntut untuk terus waspada terhadap kondisi sekitar lingkungannya agar beraktifitas dengan aman. Cuaca menjadi sangat penting diperhatikan oleh masyarakat karna kondisi yang tidak menentu setiap waktunya. Oleh karena itu, informasi prediksi cuaca yang akurat sangat penting untuk mendukung keberlangsungan aktivitas tersebut. Kondisi tersebut menjadi pemicu untuk melakukan penelitian khusus mengenai prediksi cuaca Kota Surabaya untuk meningkatkan kualitas ramalan cuaca di daerah tersebut. Mengingat tantangan geografis dan dinamika cuaca tropis yang unik, model prediksi cuaca yang lebih tepat dan efisien sangat diperlukan untuk menghadapi ketidakpastian yang terjadi di masa depan.
            """)

        with tab2:
            st.success("""
            Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca yang akurat untuk Kota Surabaya dengan menggunakan metode Artificial Neural Network (ANN) dan Long Short-Term Memory (LSTM) berdasarkan data cuaca terbaru. Adapun tujuan penelitian secara spesifik dijabarkan sebagai berikut. 
            1. Membangun model prediksi cuaca yang dapat memproyeksikan kondisi atmosfer Kota Surabaya dengan menggunakan data meteorologi yang diambil dari BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) pada periode 2023-2025.
            2. Mengoptimalkan performa prediksi cuaca dengan memanfaatkan metode ANN dan LSTM untuk mengidentifikasi pola cuaca yang lebih kompleks, terutama yang berhubungan dengan ketergantungan jangka panjang dalam data cuaca.
            3. Menilai akurasi model prediksi yang dibangun dengan membandingkan hasil prediksi dari ANN dan LSTM untuk memastikan metode yang paling sesuai digunakan untuk prediksi cuaca Kota Surabaya.                
            4. Memberikan kontribusi dalam pengembangan model prediksi cuaca berbasis teknologi kecerdasan buatan di Indonesia, khususnya untuk meningkatkan kualitas peramalan cuaca di wilayah perkotaan yang dinamis.
            """)
        
        with tab3:
            st.warning("""
            Penelitian ini memberikan berbagai manfaat yang dapat diterapkan dalam bidang meteorologi dan kehidupan sehari-hari, antara lain:
            1. Meningkatkan akurasi prediksi cuaca Kota Surabaya dengan menggunakan model ANN dan LSTM, penelitian ini dapat memberikan prediksi cuaca yang lebih akurat dan relevan untuk wilayah Kota Surabaya, membantu masyarakat dalam merencanakan kegiatan mereka dengan lebih tepat.
            2. Mendukung pengambilan keputusan hasil prediksi cuaca yang lebih akurat dapat membantu pemerintah daerah, sektor transportasi, pertanian, dan sektor lainnya dalam merencanakan kebijakan atau aktivitas yang lebih efisien, terutama yang bergantung pada kondisi cuaca.
            3. Meningkatkan kesiapsiagaan terhadap bencana cuaca ekstrem dengan model prediksi cuaca yang lebih canggih, dapat dilakukan deteksi lebih awal terhadap potensi cuaca ekstrem, seperti hujan lebat atau angin kencang, yang dapat mengurangi risiko bencana dan kerugian bagi masyarakat.
            4. Kontribusi terhadap penelitian meteorologi berbasis kecerdasan buatan penelitian ini juga memberikan kontribusi dalam pengembangan model-model prediksi cuaca berbasis kecerdasan buatan (AI), memperkenalkan pendekatan ANN dan LSTM sebagai alat yang efektif dalam analisis data cuaca yang dinamis.
            5. Peningkatan pemahaman tentang pola cuaca tropis penelitian ini dapat membantu memetakan pola cuaca di daerah tropis, khususnya di Surabaya, yang memiliki tantangan cuaca dan iklim yang spesifik, memberikan wawasan lebih dalam tentang bagaimana cuaca berkembang di kawasan tersebut.
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
