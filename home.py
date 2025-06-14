import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image

# --- Sidebar Branding ---
st.set_page_config(page_title="Prediksi Cuaca Surabaya", layout="wide")

# --- Header Image ---
col1, col2 = st.columns([1, 3])
with col1:
    try:
        logo = Image.open("asset/home.png")
        st.image(logo, use_container_width=True)
    except:
        st.warning("Logo tidak ditemukan.")
with col2:
    st.markdown("<h1 style='font-size:40px; color:#094067;'>🌤️ Platform Prediksi Cuaca Kota Surabaya</h1>", unsafe_allow_html=True)
    st.caption("Versi interaktif & modern | Tanpa install tambahan")

# --- Expander Informasi ---
with st.expander("ℹ️ Pendahuluan", expanded=False):
    tab1, tab2, tab3 = st.tabs(["📘 Latar Belakang", "🎯 Tujuan", "💡 Manfaat"])
    with tab1:
        st.info("""
        Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan yang dilakukan dengan menganalisis data meteorologi yang ada. Perkembangannya teknologi dan metode yang terus membuat banyak pilihan untuk memprediksi cuaca dengan sangat canggih. Proses ini melibatkan penggunaan berbagai metode statistika dan algoritma pemrograman untuk memodelkan dinamika atmosfer. Berbagai parameter cuaca seperti suhu, kelembapan, tekanan udara, kecepatan angin, dan curah hujan digunakan untuk membuat ramalan cuaca yang dapat memberikan informasi kepada masyarakat untuk kegiatan sehari-hari. Dalam era teknologi yang semakin maju, prediksi menjadi lebih akurat dan dapat diakses dengan mudah melalui berbagai platform digital, memberikan kemudahan bagi masyarakat dalam merencanakan aktivitas mereka.

Kota Surabaya merupakan salah satu kota metropolitan dan kota besar di Indonesia dengan berbagai aktivitas ekonomi, sosial, dan budaya yang sangat tinggi. Aktifitas masyarakat Kota Surabaya sangat padat pada jam tertentu karena kegiatan yang dilakukan secara bersama. Masyarakat dituntut untuk terus waspada terhadap kondisi sekitar lingkungannya agar beraktifitas dengan aman. Cuaca menjadi sangat penting diperhatikan oleh masyarakat karna kondisi yang tidak menentu setiap waktunya. Oleh karena itu, informasi prediksi cuaca yang akurat sangat penting untuk mendukung keberlangsungan aktivitas tersebut. Kondisi tersebut menjadi pemicu untuk melakukan penelitian khusus mengenai prediksi cuaca Kota Surabaya untuk meningkatkan kualitas ramalan cuaca di daerah tersebut. Mengingat tantangan geografis dan dinamika cuaca tropis yang unik, model prediksi cuaca yang lebih tepat dan efisien sangat diperlukan untuk menghadapi ketidakpastian yang terjadi di masa depan.
        "")
    with tab2:
        st.info("""
        Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca yang akurat untuk Kota Surabaya dengan menggunakan metode Artificial Neural Network (ANN) dan Long Short-Term Memory (LSTM) berdasarkan data cuaca terbaru. Adapun tujuan penelitian secara spesifik dijabarkan sebagai berikut. 
        1. Membangun model prediksi cuaca yang dapat memproyeksikan kondisi atmosfer Kota Surabaya dengan menggunakan data meteorologi yang diambil dari BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) pada periode 2023-2025.
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

# --- PILIHAN LAYER CUACA ---
st.markdown("### 🗺️ Peta Cuaca Interaktif Kota Surabaya")
weather_layer = st.selectbox(
    "Pilih jenis data cuaca yang ingin ditampilkan:",
    ["Suhu (Temperature)", "Kelembapan (Humidity)", "Tekanan Udara (Pressure)", "Curah Hujan (Rainfall)"]
)

# --- FUNGSI WARNA TIAP LAYER ---
def get_color_layer(layer):
    if layer == "Suhu (Temperature)":
        return 'YlOrRd'
    elif layer == "Kelembapan (Humidity)":
        return 'PuBuGn'
    elif layer == "Tekanan Udara (Pressure)":
        return 'Blues'
    elif layer == "Curah Hujan (Rainfall)":
        return 'GnBu'
    return 'YlOrBr'

# --- DUMMY DATA (untuk contoh visualisasi peta) ---
data = pd.DataFrame({
    'lat': [-7.2575, -7.2504, -7.2656],
    'lon': [112.7521, 112.7688, 112.7384],
    'value': [31, 28, 33]  # bisa suhu, kelembapan, dll
})

# --- BUAT PETA ---
m = folium.Map(location=[-7.2575, 112.7521], zoom_start=12)

# Tambahkan titik dan gradasi warna berdasarkan nilai
folium.TileLayer("cartodbpositron").add_to(m)
colormap = folium.LinearColormap(
    colors=['#00aaff', '#ffaa00', '#ff0000'],
    index=[25, 30, 35],
    vmin=data['value'].min(),
    vmax=data['value'].max(),
    caption=weather_layer
)
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=10,
        fill=True,
        fill_color=colormap(row['value']),
        fill_opacity=0.7,
        popup=f"{weather_layer}: {row['value']}°C",
        color="black",
        weight=1
    ).add_to(m)

colormap.add_to(m)

# --- TAMPILKAN PETA DI STREAMLIT ---
st_data = st_folium(m, width=900, height=500)

# --- Keterangan Tambahan ---
st.caption("📌 Data ditampilkan berdasarkan simulasi visual dan dapat dikembangkan menjadi real-time dengan integrasi API BMKG atau OpenWeather.")
