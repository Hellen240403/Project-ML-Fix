class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):  # ← pakai self di sini!
        # Sidebar
        with st.sidebar:
            logomain = Image.open("asset/home.png")
            st.image(logomain)        
            app = option_menu(
                menu_title='Dashboard',
                options=['Home','Forecast','Prediction','About'],
                icons=['house','activity','alt','info-circle-fill'],
                menu_icon='bi-cast',
                default_index=0,
                styles={
                        "container": {"padding": "5!important",
                                    "background-color":'#081f5c'},
                        "icon": {"color": "white", "font-size": "23px"}, 
                        "nav-link": {"color":"black",
                                    "font-size": "20px", 
                                    "text-align": "left", 
                                    "margin":"0px", 
                                    "--hover-color": "#f7f2eb"},
                        "nav-link-selected": {"background-color": "#02ab21"},
                })

        if app == "Home":
            home.app()
        elif app == "Forecast":
            forecast.app()    
        elif app == "Prediction":
            prediction.app()        
        elif app == "About":
            about.app()     

# Jalankan MultiApp
app = MultiApp()
app.run()
