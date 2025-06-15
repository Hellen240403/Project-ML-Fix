import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import home
import forecast
import prediction
import about

# ✅ Panggil hanya sekali, dan di paling atas
st.set_page_config(
    page_title="Prediksi Cuaca Surabaya ☀️🌧️",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Struktur MultiApp
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Sidebar
        with st.sidebar:
            try:
                logomain = Image.open("asset/sidebar.png")
                st.image(logomain)
            except Exception as e:
                st.warning(f"Gagal memuat logo: {e}")
            
            app = option_menu(
                menu_title='Dashboard',
                options=['🏠 Home', '🌦️ Forecast', '📊 Prediction', 'ℹ️ About'],
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": '#081f5c'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {
                        "color": "white", 
                        "font-size": "20px", 
                        "text-align": "left", 
                        "margin": "0px", 
                        "--hover-color": "#a7ebf2"
                    },
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Routing
        try:
            if app == "🏠 Home":
                home.app()
            elif app == "🌦️ Forecast":
                forecast.app()
            elif app == "📊 Prediction":
                prediction.app()
            elif app == "ℹ️ About":
                about.app()
        except KeyError as ke:
            st.error(f"Kolom hilang dalam data: {ke}. Periksa apakah file CSV memiliki kolom tersebut.")
        except FileNotFoundError as fnf:
            st.error(f"File tidak ditemukan: {fnf}. Pastikan path dan nama file benar.")
        except Exception as e:
            st.error(f"Terjadi error: {e}")

# ✅ Jalankan aplikasi
app = MultiApp()
app.run()
