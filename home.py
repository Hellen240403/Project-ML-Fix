import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fungsi load data
def load_data(file_path, index_col=None):
    try:
        df = pd.read_csv(file_path, index_col=index_col)
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return None

    # Bersihkan nama kolom
    df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
    return df

def app():
    st.title("Platform Prediksi Cuaca Kota Surabaya :thunder_cloud_and_rain:")

    with st.expander("Pendahuluan"):
        tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Tujuan", "Manfaat"])

        with tab1:
            st.info("""
            Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan yang dilakukan dengan menganalisis data meteorologi yang ada. Perkembangannya teknologi dan metode yang terus membuat banyak pilihan untuk memprediksi cuaca dengan sangat canggih. Proses ini melibatkan penggunaan berbagai metode statistika dan algoritma pemrograman untuk memodelkan dinamika atmosfer. Berbagai parameter cuaca seperti suhu, kelembapan, tekanan udara, kecepatan angin, dan curah hujan digunakan untuk membuat ramalan cuaca yang dapat memberikan informasi kepada masyarakat untuk kegiatan sehari-hari. Dalam era teknologi yang semakin maju, prediksi menjadi lebih akurat dan dapat diakses dengan mudah melalui berbagai platform digital, memberikan kemudahan bagi masyarakat dalam merencanakan aktivitas mereka. Kota Surabaya merupakan salah satu kota metropolitan dan kota besar di Indonesia dengan berbagai aktivitas ekonomi, sosial, dan budaya yang sangat tinggi. Aktifitas masyarakat Kota Surabaya sangat padat pada jam tertentu karena kegiatan yang dilakukan secara bersama. Masyarakat dituntut untuk terus waspada terhadap kondisi sekitar lingkungannya agar beraktifitas dengan aman. Cuaca menjadi sangat penting diperhatikan oleh masyarakat karna kondisi yang tidak menentu setiap waktunya. Oleh karena itu, informasi prediksi cuaca yang akurat sangat penting untuk mendukung keberlangsungan aktivitas tersebut. Kondisi tersebut menjadi pemicu untuk melakukan penelitian khusus mengenai prediksi cuaca Kota Surabaya untuk meningkatkan kualitas ramalan cuaca di daerah tersebut. Mengingat tantangan geografis dan dinamika cuaca tropis yang unik, model prediksi cuaca yang lebih tepat dan efisien sangat diperlukan untuk menghadapi ketidakpastian yang terjadi di masa depan.
            """)
        with tab2:
            st.info("Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca 
            ")
        with tab3:
            st.info("Penelitian ini memberikan berbagai manfaat 
            ")

    with st.expander("Metode"):
        st.write("Neural Network (NN) adalah model komputasi yang terinspirasi oleh cara kerja otak ...")

    # Load data
    df = load_data("data/df_hujan.csv")
    if df is None:
        st.stop()

    # Validasi kolom tanggal
    if 'tanggal' not in df.columns:
        st.error(f"❌ Kolom 'tanggal' tidak ditemukan! Kolom tersedia: {df.columns.tolist()}")
        st.stop()

    # Format tanggal: DD/MM/YYYY
    try:
        df['tanggal'] = pd.to_datetime(df['tanggal'], format='%d/%m/%Y', errors='coerce')
        if df['tanggal'].isna().all():
            st.error("⚠️ Semua nilai 'tanggal' gagal dikonversi. Cek format tanggalnya (harus DD/MM/YYYY).")
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Gagal mengonversi tanggal: {e}")
        st.stop()

    df.set_index('tanggal', inplace=True)

    # Tampilkan data
    st.divider()
    st.subheader("📊 Data Cuaca Tahun 2023-2025")
    st.dataframe(df, use_container_width=True)

    st.caption("📌 Data cuaca Kota Surabaya diperoleh dari BMKG (https://dataonline.bmkg.go.id/home)")
