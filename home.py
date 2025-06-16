import streamlit as st
from utils.weather import get_current_weather

def app():
    st.markdown(
        "<h1 style='text-align: center; color: #000;'>Surabaya</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<h5 style='text-align: center; color: #666;'>Rabu, 1 Januari 2025</h5>", unsafe_allow_html=True
    )

    st.image("asset/bg-cuaca.png", use_column_width=True)  # Gambar awan besar

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col2:
        st.markdown(
            "<h2 style='color:#222;font-weight:bold;'>🌤️ Platform Prediksi Cuaca Surabaya</h2>",
            unsafe_allow_html=True
        )

        st.markdown("")  # Untuk spacing

        if st.button("🔄 Refresh"):
            st.cache_data.clear()

        try:
            weather = get_current_weather()
        except Exception as e:
            st.error(f"Data cuaca tidak tersedia: {e}")
            weather = None

        if weather:
            st.markdown(f"""
            <div class="weather-card" style="margin-top: 10px; padding: 15px 25px;">
              <div style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  flex-wrap: wrap;
                  gap: 20px;
                  font-size: 16px;
                  ">
                <div style="min-width: 120px;">🌡️ <b style="color:#d32f2f;">Suhu:</b> {weather['temperature']}</div>
                <div style="min-width: 150px;">💧 <b style="color:#0288d1;">Kelembapan:</b> {weather['humidity']}</div>
                <div style="min-width: 140px;">🌬️ <b style="color:#0277bd;">Angin:</b> {weather['wind']}</div>
                <div style="min-width: 130px;">🌞 <b style="color:#fbc02d;">UV:</b> {weather['uv']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.caption("📌 Data real-time — AccuWeather API")
