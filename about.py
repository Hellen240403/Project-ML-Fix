import streamlit as st
from PIL import Image

def app():
    # Gaya CSS
    st.markdown("""
        <style>
        .title-style {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #0E6BA8;
            margin-bottom: 20px;
        }
        .subheader-style {
            font-size: 24px;
            color: #0A3D62;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .label-style {
            font-weight: bold;
            color: #333;
        }
        .content-box {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        .motivasi-box {
            background-color: #e1f5fe;
            border-left: 5px solid #0288d1;
            padding: 12px 18px;
            border-radius: 10px;
            margin-top: 10px;
            font-style: italic;
        }
        .linkedin-link {
            text-decoration: none;
            color: #0077b5;
            font-weight: bold;
        }
        .linkedin-link:hover {
            color: #004471;
        }
        </style>
    """, unsafe_allow_html=True)

    # Judul Halaman
    st.markdown("<div class='title-style'>☁️ Tentang Tim SkyWard</div>", unsafe_allow_html=True)

    # Deskripsi Proyek
    st.markdown("""
    <div class='content-box'>
        <p style='font-size:18px; text-align: justify;'>
            <b>SkyWard</b> merupakan sebuah proyek pembelajaran berbasis <b>Machine Learning</b> dari mahasiswa <b>Departemen Statistika Bisnis</b> Universitas Airlangga Angkatan 2022.
            Proyek ini dirancang untuk memprediksi cuaca harian di Kota Surabaya dengan memanfaatkan <b>algoritma LSTM dan ANN</b>.
            Tujuannya adalah memberi solusi analisis data real-time yang bermanfaat dan mudah diakses masyarakat 🌦️.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Profil Anggota
    team = [
        {
            "Nama": "Dwi Ilham Ramadhany",
            "img": "asset/IMG_4105.JPG",
            "Tempat,Tanggal Lahir": "Bangkalan, 7 November 2003",
            "NRP": "2043221054",
            "Status": "Mahasiswa Aktif",
            "Motivasi": "Investasikanlah kesehatanmu selama mungkin.",
            "Email": "dwrmdhany11@gmail.com",
            "Linkedin": "https://linkedin.com/in/dwiilhamramadhany"
        },
        {
            "Nama": "Hellen Aldenia Rovi",
            "img": "asset/IMG_3428_11zon.jpg",
            "Tempat,Tanggal Lahir": "Surabaya, 24 Agustus 2003",
            "NRP": "2043221045",
            "Status": "Mahasiswa Aktif",
            "Motivation": "Mengubah pola kompleks jadi cerita sederhana adalah keajaiban statistika.",
            "Email": "hellenaldenia@gmail.com",
            "Linkedin": "https://linkedin.com/in/hellenaldenia"
        },
        {
            "Nama": "Endita Prastyansyach",
            "img": "asset/IMG_4105.JPG",  # Ganti jika punya foto berbeda
            "Tempat,Tanggal Lahir": "Sidoarjo, 10 Januari 2004",
            "NRP": "2043221145",
            "Status": "Mahasiswa Aktif",
            "Motivation": "Membangun sistem yang tidak hanya memprediksi, tapi menciptakan masa depan lebih baik.",
            "Email": "enditapras@gmail.com",
            "Linkedin": "https://linkedin.com/in/enditapras"
        }
    ]

    for member in team:
        tab = st.container()
        with tab:
            col1, col2 = st.columns([1, 2], gap="large")
            with col1:
                try:
                    img = Image.open(member["img"])
                    if "Dwi Ilham" in member["name"] or "Endita" in member["name"]:
                        img = img.rotate(-90, expand=True)
                    st.image(img, caption=member["name"], use_container_width=True)
                except Exception as e:
                    st.warning(f"Gagal memuat gambar: {e}")
            with col2:
                st.markdown(f"<div class='subheader-style'>{member['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <span class='label-style'>📍 Tempat, Tanggal Lahir:</span> {member['ttl']}  \n
                    <span class='label-style'>🆔 NRP:</span> {member['nrp']}  \n
                    <span class='label-style'>🎓 Status:</span> {member['status']}  \n
                    <span class='label-style'>📧 Email:</span> {member['email']}  \n
                    <span class='label-style'>🔗 LinkedIn:</span> <a href="{member['linkedin']}" target="_blank" class="linkedin-link">{member['linkedin'].split('//')[1]}</a>
                """, unsafe_allow_html=True)
                st.markdown(f"<div class='motivasi-box'>💡 <b>Motivasi:</b> {member['motivation']}</div>", unsafe_allow_html=True)

    # Sumber Data
    st.markdown("## 📚 Sumber Data")
    st.markdown("""
    <div class='content-box'>
        <p style='font-size:17px; text-align: justify;'>
            Data cuaca yang digunakan dalam proyek ini bersumber dari situs resmi <b>Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)</b>,
            dan dapat diakses secara terbuka melalui 
            <a href='https://dataonline.bmkg.go.id/data_harian' target='_blank'>dataonline.bmkg.go.id</a> 🌐.
            Kami mengucapkan terima kasih kepada BMKG atas keterbukaan datanya.
        </p>
    </div>
    """, unsafe_allow_html=True)
