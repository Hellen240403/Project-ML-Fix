import streamlit as st
import pandas as pd
import requests
from PIL import Image

# ------------------------------------------------------------------ #
#  CONFIG ACCUWEATHER API
# ------------------------------------------------------------------ #
@st.cache_data(ttl=600)
def get_current_weather():
    """Ambil cuaca terkini Surabaya dari Open-Meteo (tanpa API key)"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.2575,      # Koordinat Surabaya
        "longitude": 112.7521,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,uv_index",
        "timezone": "Asia/Jakarta"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()["current"]

    return {
        "temperature": f"{data['temperature_2m']}°C",
        "humidity"   : f"{data['relative_humidity_2m']}%",
        "wind"       : f"{data['wind_speed_10m']} km/h",
        "uv"         : f"UV Index {data['uv_index']}"
    }

# ------------------------------------------------------------------ #
#  CSS
# ------------------------------------------------------------------ #
def set_custom_css():
    st.markdown("""
    <style>
     .stApp { background:white; font-family:'Segoe UI',sans-serif; }
     .weather-card {
        background: rgba(255,255,255,0.6);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,.1);
        width: max-content;
     }
     .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        color: #1e293b;
        font-weight: bold;
        border-radius: 10px;
     }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------ #
#  DATASET LOCAL
# ------------------------------------------------------------------ #
def load_data(path):
    try:
        df = pd.read_csv(path, sep=';')
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        return df
    except Exception as e:
        st.warning(f"Gagal memuat data historikal: {e}")
        return None

# ------------------------------------------------------------------ #
#  MAIN PAGE
# ------------------------------------------------------------------ #
def app():
    set_custom_css()

    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")

    col1, col2 = st.columns([1, 1.3])

    # ---------------- Judul Kotak ---------------- #
    with col1:
        st.markdown("""
        <div style="background:#f0f3fa;padding:20px 30px;border-radius:12px;
                    box-shadow:2px 2px 10px rgba(0,0,0,.1); width:max-content;">
           <h3 style="margin:0;">📍 Cuaca Surabaya Hari Ini</h3>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- Kartu Cuaca ---------------- #
    with col2:
        weather = None
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
    
        try:
            weather = get_current_weather()
        except Exception as e:
            st.error(f"Data cuaca tidak tersedia: {e}")
            
        if weather:
            st.markdown(f"""
            <div class="weather-card" style="margin: 10px 0 10px 10px; padding: 15px 25px;">
              <div style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  flex-wrap: wrap;
                  gap: 20px;
                  font-size: 16px;
                  min-width: 500px;
                  ">
                <div style="min-width: 120px;">🌡️ <b style="color:#d32f2f;">Suhu:</b> {weather['temperature']}</div>
                <div style="min-width: 150px;">💧 <b style="color:#0288d1;">Kelembapan:</b> {weather['humidity']}</div>
                <div style="min-width: 140px;">🌬️ <b style="color:#0277bd;">Angin:</b> {weather['wind']}</div>
                <div style="min-width: 130px;">🌞 <b style="color:#fbc02d;">UV:</b> {weather['uv']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    
            st.caption("📌 Data real-time — AccuWeather API")


    # ------------- Penjelasan & Dataset ---------- #
    with st.expander("📘 Pendahuluan", expanded=False):
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
        st.markdown("
        - **ANN**    :Artificial Neural Network (ANN) adalah model komputasi yang meniru cara kerja otak manusia dalam memproses informasi. ANN efektif digunakan untuk berbagai masalah kompleks, termasuk prediksi cuaca. Model ini terdiri dari neuron-neuron sederhana yang saling terhubung dan belajar mengenali pola dari data.
        - **LSTM**   :Long Short-Term Memory (LSTM) merupakan pengembangan dari Recurrent Neural Network (RNN) yang dirancang untuk mengatasi masalah vanishing gradient saat mengolah data berurutan. LSTM memiliki kemampuan untuk mengingat informasi historis dalam jangka panjang, sehingga cocok untuk memodelkan data cuaca yang bersifat temporal. 
                    ")

    df = load_data("data/df_hujan.csv")
    if df is not None:
        st.divider()
        st.subheader("📊 Data Cuaca Surabaya (2023-2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: BMKG")

# ------------------------------------------------------------------ #
if __name__ == "__main__":
    app()
