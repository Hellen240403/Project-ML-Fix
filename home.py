import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Fungsi untuk load data
def load_data(file_path, index_col=None):
    try:
        df = pd.read_csv(file_path, index_col=index_col, sep=';')  # delimiter ;
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return None

    df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
    return df

# Fungsi utama
def app():
    # Tampilan logo
    try:
        logomain = Image.open("asset/home.png")
        st.image(logomain, width=200)
    except Exception as e:
        st.warning(f"Gagal memuat logo: {e}")

    st.title("🌦️ Platform Prediksi Cuaca Kota Surabaya")
    st.markdown(
        "<style>div.block-container{padding-top:2rem; padding-bottom:2rem;} .stTabs [data-baseweb='tab']{background:#f0f2f6;border-radius:10px;padding:10px}</style>",
        unsafe_allow_html=True,
    )

    # Tab Pendahuluan
    with st.expander("📘 Pendahuluan", expanded=True):
        tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Tujuan", "Manfaat"])

        with tab1:
            st.info("""Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan yang dilakukan dengan menganalisis data meteorologi yang ada. Perkembangannya teknologi dan metode yang terus membuat banyak pilihan untuk memprediksi cuaca dengan sangat canggih. Proses ini melibatkan penggunaan berbagai metode statistika dan algoritma pemrograman untuk memodelkan dinamika atmosfer. Berbagai parameter cuaca seperti suhu, kelembapan, tekanan udara, kecepatan angin, dan curah hujan digunakan untuk membuat ramalan cuaca yang dapat memberikan informasi kepada masyarakat untuk kegiatan sehari-hari. Dalam era teknologi yang semakin maju, prediksi menjadi lebih akurat dan dapat diakses dengan mudah melalui berbagai platform digital, memberikan kemudahan bagi masyarakat dalam merencanakan aktivitas mereka. Kota Surabaya merupakan salah satu kota metropolitan dan kota besar di Indonesia dengan berbagai aktivitas ekonomi, sosial, dan budaya yang sangat tinggi. Aktifitas masyarakat Kota Surabaya sangat padat pada jam tertentu karena kegiatan yang dilakukan secara bersama. Masyarakat dituntut untuk terus waspada terhadap kondisi sekitar lingkungannya agar beraktifitas dengan aman. Cuaca menjadi sangat penting diperhatikan oleh masyarakat karna kondisi yang tidak menentu setiap waktunya. Oleh karena itu, informasi prediksi cuaca yang akurat sangat penting untuk mendukung keberlangsungan aktivitas tersebut. Kondisi tersebut menjadi pemicu untuk melakukan penelitian khusus mengenai prediksi cuaca Kota Surabaya untuk meningkatkan kualitas ramalan cuaca di daerah tersebut. Mengingat tantangan geografis dan dinamika cuaca tropis yang unik, model prediksi cuaca yang lebih tepat dan efisien sangat diperlukan untuk menghadapi ketidakpastian yang terjadi di masa depan.""")
        with tab2:
            st.info("""
            Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca yang akurat untuk Kota Surabaya dengan menggunakan metode Artificial Neural Network (ANN) dan Long Short-Term Memory (LSTM) berdasarkan data cuaca terbaru. Adapun tujuan penelitian secara spesifik dijabarkan sebagai berikut. 
            1. Membangun model prediksi cuaca yang dapat memproyeksikan kondisi atmosfer Kota Surabaya dengan menggunakan data meteorologi yang diambil dari BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) pada periode 2023-2025
            2. Mengoptimalkan performa prediksi cuaca dengan memanfaatkan metode ANN dan LSTM untuk mengidentifikasi pola cuaca yang lebih kompleks, terutama yang berhubungan dengan ketergantungan jangka panjang dalam data cuaca.
            3. Menilai akurasi model prediksi yang dibangun dengan membandingkan hasil prediksi dari ANN dan LSTM untuk memastikan metode yang paling sesuai digunakan untuk prediksi cuaca Kota Surabaya.
            4. Memberikan kontribusi dalam pengembangan model prediksi cuaca berbasis teknologi kecerdasan buatan di Indonesia, khususnya untuk meningkatkan kualitas peramalan cuaca di wilayah perkotaan yang dinamis.
            """)
        with tab3:
            st.info("""
            Penelitian ini memberikan berbagai manfaat yang dapat diterapkan dalam bidang meteorologi dan kehidupan sehari-hari, antara lain:
            1. Meningkatkan akurasi prediksi cuaca Kota Surabaya dengan menggunakan model ANN dan LSTM, penelitian ini dapat memberikan prediksi cuaca yang lebih akurat dan relevan untuk wilayah Kota Surabaya, membantu masyarakat dalam merencanakan kegiatan mereka dengan lebih tepat.
            2. Mendukung pengambilan keputusan hasil prediksi cuaca yang lebih akurat dapat membantu pemerintah daerah, sektor transportasi, pertanian, dan sektor lainnya dalam merencanakan kebijakan atau aktivitas yang lebih efisien, terutama yang bergantung pada kondisi cuaca.
            3. Meningkatkan kesiapsiagaan terhadap bencana cuaca ekstrem dengan model prediksi cuaca yang lebih canggih, dapat dilakukan deteksi lebih awal terhadap potensi cuaca ekstrem, seperti hujan lebat atau angin kencang, yang dapat mengurangi risiko bencana dan kerugian bagi masyarakat.
            4. Kontribusi terhadap penelitian meteorologi berbasis kecerdasan buatan penelitian ini juga memberikan kontribusi dalam pengembangan model-model prediksi cuaca berbasis kecerdasan buatan (AI), memperkenalkan pendekatan ANN dan LSTM sebagai alat yang efektif dalam analisis data cuaca yang dinamis.
            5. Peningkatan pemahaman tentang pola cuaca tropis penelitian ini dapat membantu memetakan pola cuaca di daerah tropis, khususnya di Surabaya, yang memiliki tantangan cuaca dan iklim yang spesifik, memberikan wawasan lebih dalam tentang bagaimana cuaca berkembang di kawasan tersebut.
            """)
    # Metode
    with st.expander("🧠 Metode"):
        st.markdown("""
            - **ANN** (Artificial Neural Network): Menggunakan jaringan syaraf tiruan untuk mengenali pola cuaca.
            - **LSTM** (Long Short-Term Memory): Mampu mengingat tren jangka panjang dan sangat cocok untuk prediksi waktu.
        """)

    # Load dan tampilkan data
    df = load_data("data/df_hujan.csv")
    if df is None:
        return

    st.divider()
    st.subheader("📊 Data Cuaca Tahun 2023-2025")
    st.dataframe(df, use_container_width=True)

    st.caption("📌 Sumber: [BMKG](https://dataonline.bmkg.go.id/home)")

# Panggil fungsi saat file dijalankan
if __name__ == "__main__":
    app()
