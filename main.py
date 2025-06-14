import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import home 
import forecast
import prediction
import about

st.set_page_config(
    page_title="Dashboard"
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):  # ✅ Perbaikan: harus pakai 'self'
        # Sidebar
        with st.sidebar:
            try:
                logomain = Image.open("asset/sidebar.png")
                st.image(logomain)
            except Exception as e:
                st.warning(f"Gagal memuat logo: {e}")
            
            app = option_menu(
                menu_title='Dashboard',
                options=['Home', 'Forecast', 'Prediction', 'About'],
                icons=['house', 'activity', 'alt', 'info-circle-fill'],
                menu_icon='bi-cast',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": '#081f5c'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#a7ebf2"},
                    "nav-link-selected": {"background-color": "black"},
                }
            )

        # Menu routing
        try:
            if app == "Home":
                home.app()
            elif app == "Forecast":
                forecast.app()
            elif app == "Prediction":
                prediction.app()
            elif app == "About":
                about.app()
        except KeyError as ke:
            st.error(f"Kolom hilang dalam data: {ke}. Periksa apakah file CSV memiliki kolom tersebut.")
        except FileNotFoundError as fnf:
            st.error(f"File tidak ditemukan: {fnf}. Pastikan path dan nama file benar.")
        except Exception as e:
            st.error(f"Terjadi error: {e}")

# Jalankan aplikasi
app = MultiApp()
app.run()
