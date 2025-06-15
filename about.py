import streamlit as st
from PIL import Image

def app():
    # --- Gaya Umum ---
    st.markdown("""
        <style>
        .title-style {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #0E6BA8;
            margin-bottom: 10px;
        }
        .subheader-style {
            font-size: 24px;
            color: #4A4A4A;
            font-weight: 600;
        }
        .content-box {
            background-color: rgba(255, 255, 255, 0.6);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .motivasi-box {
            background-color: #E0F7FA;
            border-left: 5px solid #00BCD4;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Judul & Deskripsi ---
    st.markdown("<div class='title-style'>🌤️ Tentang SkyWard Team</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='content-box'>
        <p style='font-size:18px; text-align: justify;'>
            Kami adalah mahasiswa <b>Departemen Statistika Bisnis Angkatan 2022</b> yang sedang mendalami mata kuliah <b>Machine Learning</b>. 
            Dalam mata kuliah ini, kami mempelajari bagaimana <i>Artificial Intelligence (AI)</i> dan algoritma prediksi diterapkan pada data berurutan seperti cuaca.
            Proyek ini, bernama <b>SkyWard</b> ☁️, merupakan hasil penerapan pengetahuan kami untuk membuat sistem prediksi cuaca berbasis <b>LSTM & ANN</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs([
        "👨‍💻 Dwi Ilham Ramadhany", 
        "👩‍💻 Hellen Aldenia Rovi", 
        "👩‍💻 Endita Prastyansyach"
    ])

    # --- Profil DWI ---
    with tab1:
        col1, col2 = st.columns([1, 2], gap="medium")
        with col1:
            try:
                img = Image.open("asset/IMG_4105.JPG")
                img = img.rotate(-90, expand=True)
                st.image(img, caption="Dwi Ilham Ramadhany", use_container_width=True)
            except Exception as e:
                st.warning(f"Gagal memuat gambar: {e}")
        with col2:
            st.markdown("<div class='subheader-style'>Dwi Ilham Ramadhany</div>", unsafe_allow_html=True)
            st.markdown("📍 Bangkalan, 7 November 2003  \n🆔 NRP: 2043221054")
            st.markdown("<div class='motivasi-box'>💡 <i>Investasikanlah kesehatanmu selama mungkin.</i></div>", unsafe_allow_html=True)
            st.markdown("📧 dwrmdhany11@gmail.com")

    # --- Profil HELLEN ---
    with tab2:
        col1, col2 = st.columns([1, 2], gap="medium")
        with col1:
            try:
                img = Image.open("asset/IMG_3428_11zon.jpg")
                st.image(img, caption="Hellen Aldenia Rovi", use_container_width=True)
            except Exception as e:
                st.warning(f"Gagal memuat gambar: {e}")
        with col2:
            st.markdown("<div class='subheader-style'>Hellen Aldenia Rovi</div>", unsafe_allow_html=True)
            st.markdown("📍 Surabaya, 24 Agustus 2003  \n🆔 NRP: 2043221045")
            st.markdown(""<div class='motivasi-box'>📊 <i>Mengubah pola kompleks jadi cerita sederhana adalah keajaiban statistika.</i></div>"", unsafe_allow_html=True)
            st.markdown("📧 hellenaldenia@gmail.com")

    # --- Profil ENDITA ---
    with tab3:
        col1, col2 = st.columns([1, 2], gap="medium")
        with col1:
            try:
                img = Image.open("asset/IMG_4105.JPG")
                img = img.rotate(-90, expand=True)
                st.image(img, caption="Endita Prastyansyach", use_container_width=True)
            except Exception as e:
                st.warning(f"Gagal memuat gambar: {e}")
        with col2:
            st.markdown("<div class='subheader-style'>Endita Prastyansyach</div>", unsafe_allow_html=True)
            st.markdown("📍 Sidoarjo, 10 Januari 2004  \n🆔 NRP: 2043221145")
            st.markdown("<div class='motivasi-box'>🤖 <i>Membangun sistem yang tidak hanya memprediksi, tapi menciptakan masa depan lebih baik.</i></div>", unsafe_allow_html=True)
            st.markdown("📧 enditapras@gmail.com")

    # --- Sumber Data ---
    st.markdown("## 📚 Sumber Data")
    st.markdown("""
    <div class='content-box'>
        <p style='font-size:17px; text-align: justify;'>
            Data cuaca diambil dari situs resmi <b>Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)</b> yang dapat diakses melalui 
            <a href='https://dataonline.bmkg.go.id/data_harian' target='_blank'>dataonline.bmkg.go.id</a> 🌐.  
            Terima kasih kepada BMKG atas data yang terbuka dan mudah diakses.
        </p>
    </div>
    """, unsafe_allow_html=True)
