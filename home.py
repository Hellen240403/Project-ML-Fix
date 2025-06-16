import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=600)
def get_current_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.2575,
        "longitude": 112.7521,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,uv_index",
        "timezone": "Asia/Jakarta"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()["current"]
    return {
        "temperature": f"{data['temperature_2m']}°C",
        "humidity": f"{data['relative_humidity_2m']}%",
        "wind": f"{data['wind_speed_10m']} km/h",
        "uv": f"UV Index {data['uv_index']}"
    }

def app():
    # CSS Custom Style
    st.markdown("""
        <style>
        .weather-row {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        .weather-item {
            background-color: rgba(255,255,255,0.6);
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton > button {
            height: 38px;
            padding: 6px 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Gambar dan Judul
    st.image("asset/home.png", use_container_width=True)
    st.title("🌦️ Platform Prediksi Cuaca Surabaya")
    st.markdown("### 📍 Cuaca Surabaya Hari Ini")

    # Layout sejajar horizontal (refresh + cuaca)
    weather = None
    try:
        weather = get_current_weather()
    except Exception as e:
        st.error(f"Data cuaca tidak tersedia: {e}")

    st.markdown("<div class='weather-row'>", unsafe_allow_html=True)

    # Tombol Refresh di kiri
    with st.form(key="refresh_form", clear_on_submit=False):
        submit_button = st.form_submit_button(label="🔄 Refresh")
        if submit_button:
            st.cache_data.clear()

    st.markdown("</div>", unsafe_allow_html=True)

    # Info cuaca di kanan
    if weather:
        st.markdown(f"""
            <div class='weather-row'>
                <div class='weather-item'>🌡️ <b style='color:#d32f2f;'>Suhu:</b> {weather['temperature']}</div>
                <div class='weather-item'>💧 <b style='color:#0288d1;'>Kelembapan:</b> {weather['humidity']}</div>
                <div class='weather-item'>🌬️ <b style='color:#0277bd;'>Angin:</b> {weather['wind']}</div>
                <div class='weather-item'>🌞 <b style='color:#fbc02d;'>UV:</b> {weather['uv']}</div>
            </div>
            <div style='margin-top:-5px'>
                <small>📌 Data real-time — Open-Meteo API</small>
            </div>
        """, unsafe_allow_html=True)

    # Expanders
    tab1, tab2, tab3 = st.tabs(["📘 Pendahuluan", "🎯 Tujuan", "💡 Manfaat"])
    
    with st.expander : 
    with tab1 :
        st.info("""
        Prediksi cuaca adalah proses untuk memprediksi kondisi atmosfer pada waktu tertentu di masa depan yang dilakukan dengan menganalisis data meteorologi yang ada. Perkembangannya teknologi dan metode yang terus membuat banyak pilihan untuk memprediksi cuaca dengan sangat canggih. Proses ini melibatkan penggunaan berbagai metode statistika dan algoritma pemrograman untuk memodelkan dinamika atmosfer. Berbagai parameter cuaca seperti suhu, kelembapan, tekanan udara, kecepatan angin, dan curah hujan digunakan untuk membuat ramalan cuaca yang dapat memberikan informasi kepada masyarakat untuk kegiatan sehari-hari. Dalam era teknologi yang semakin maju, prediksi menjadi lebih akurat dan dapat diakses dengan mudah melalui berbagai platform digital, memberikan kemudahan bagi masyarakat dalam merencanakan aktivitas mereka.
        Kota Surabaya merupakan salah satu kota metropolitan dan kota besar di Indonesia dengan berbagai aktivitas ekonomi, sosial, dan budaya yang sangat tinggi. Aktifitas masyarakat Kota Surabaya sangat padat pada jam tertentu karena kegiatan yang dilakukan secara bersama. Masyarakat dituntut untuk terus waspada terhadap kondisi sekitar lingkungannya agar beraktifitas dengan aman. Cuaca menjadi sangat penting diperhatikan oleh masyarakat karna kondisi yang tidak menentu setiap waktunya. Oleh karena itu, informasi prediksi cuaca yang akurat sangat penting untuk mendukung keberlangsungan aktivitas tersebut. Kondisi tersebut menjadi pemicu untuk melakukan penelitian khusus mengenai prediksi cuaca Kota Surabaya untuk meningkatkan kualitas ramalan cuaca di daerah tersebut. Mengingat tantangan geografis dan dinamika cuaca tropis yang unik, model prediksi cuaca yang lebih tepat dan efisien sangat diperlukan untuk menghadapi ketidakpastian yang terjadi di masa depan.
        """)
    
    with st.expander :
    with tab2 :
        st.markdown("""
        Tujuan dari penelitian ini adalah untuk mengembangkan model prediksi cuaca yang akurat untuk Kota Surabaya dengan menggunakan metode Artificial Neural Network (ANN) dan Long Short-Term Memory (LSTM) berdasarkan data cuaca terbaru. Adapun tujuan penelitian secara spesifik dijabarkan sebagai berikut. 
        - Memberikan informasi cuaca terkini secara real-time.
        - Memprediksi kondisi cuaca beberapa hari ke depan di Surabaya.
        - Menyediakan visualisasi data historis cuaca untuk analisis lanjutan.
        """)
    
    with st.expander :
    with tab3 :
        st.markdown("""
        Penelitian ini memberikan berbagai manfaat yang dapat diterapkan dalam bidang meteorologi dan kehidupan sehari-hari, antara lain:
        - Membantu masyarakat merencanakan aktivitas sehari-hari.
        - Mendukung pengambilan keputusan di sektor transportasi, pertanian, dan pariwisata.
        - Menjadi sarana edukasi tentang pentingnya data cuaca.
        """)

    with st.expander("🧠 Metode"):
        st.markdown("""
        - **ANN**    : Artificial Neural Network (ANN) model komputasi yang meniru cara kerja otak manusia dalam memproses informasi. ANN efektif digunakan untuk berbagai masalah kompleks, termasuk prediksi cuaca. Model ini terdiri dari neuron-neuron sederhana yang saling terhubung dan belajar mengenali pola dari data. 
        - **LSTM**   : Long Short-Term Memory (LSTM) adalah pengembangan dari Recurrent Neural Network (RNN) yang dirancang untuk mengatasi masalah vanishing gradient saat mengolah data berurutan. LSTM memiliki kemampuan untuk mengingat informasi historis dalam jangka panjang, sehingga cocok untuk memodelkan data cuaca yang bersifat temporal.
        """)

    # Dataset Historikal
    try:
        df = pd.read_csv("data/df_hujan.csv", sep=";")
        df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')
        st.subheader("📊 Data Cuaca Surabaya (2023–2025)")
        st.dataframe(df, use_container_width=True, height=350)
        st.caption("📌 Sumber: BMKG")
    except Exception as e:
        st.warning(f"Gagal memuat data historikal: {e}")

if __name__ == "__main__":
    app()
