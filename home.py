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
            st.info("Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer ...")
        with tab2:
            st.info("Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca ...")
        with tab3:
            st.info("Penelitian ini memberikan berbagai manfaat ...")

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
