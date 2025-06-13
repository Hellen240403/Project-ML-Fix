import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fungsi load data dengan pembersihan kolom
def load_data(file_path, index_col=None):
    df = pd.read_csv(file_path, index_col=index_col)

    # Normalisasi nama kolom
    df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')

    return df

def app():
    st.title("Platform Prediksi Cuaca Kota Surabaya :thunder_cloud_and_rain:")

    with st.expander("Pendahuluan"):
        tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Tujuan", "Manfaat"])

    with tab1:
        st.info("""
            Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer ...
            (konten disingkat, sama seperti sebelumnya)
        """)

    with tab2:
        st.info("""
            Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca ...
            (konten disingkat)
        """)

    with tab3:
        st.info("""
            Penelitian ini memberikan berbagai manfaat yang dapat diterapkan ...
            (konten disingkat)
        """)

    with st.expander("Metode"):
        st.write("""
            Neural Network (NN) adalah model komputasi yang terinspirasi oleh cara kerja otak ...
            (konten disingkat)
        """)

    # Load Dataset
    df = load_data("data/df_hujan.csv")

    # Normalisasi ulang kolom (jaga-jaga jika load_data dipakai ulang)
    df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')

    # Validasi keberadaan kolom tanggal
    if 'tanggal' not in df.columns:
        st.error(f"❌ Kolom 'tanggal' tidak ditemukan! Kolom tersedia: {df.columns.tolist()}")
        st.stop()

    # Konversi tanggal
    try:
        df['tanggal'] = pd.to_datetime(df['tanggal'], format='%Y-%m-%d')
    except Exception as e:
        st.error(f"⚠️ Format tanggal tidak bisa dikonversi. Error: {e}")
        st.stop()

    df.set_index('tanggal', inplace=True)

    # Tampilkan data
    st.divider()
    st.subheader("📊 Data Cuaca Tahun 2023-2025")
    st.dataframe(df, use_container_width=True)

    # Sumber
    url1 = "https://dataonline.bmkg.go.id/home"
    st.caption("Data cuaca Kota Surabaya diperoleh dari BMKG (%s)" % url1)
