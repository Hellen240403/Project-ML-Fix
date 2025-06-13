import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from keras.models import load_model as keras_model
from sklearn.preprocessing import MinMaxScaler

# ──────────────────────────────────────────────────────────────
# 1. LOAD & CLEAN DATA
# ──────────────────────────────────────────────────────────────
def load_and_prepare_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep=';', engine='python')

    # Normalisasi kolom
    df.columns = df.columns.str.strip().str.lower().str.replace('\ufeff', '')

    # Validasi dan ganti nama kolom tanggal
    if 'tanggal' not in df.columns:
        st.error(f"❌ Kolom 'tanggal' tidak ditemukan! Kolom yang terbaca: {df.columns.tolist()}")
        st.stop()

    # Konversi tanggal (format DD/MM/YYYY)
    try:
        df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True)
    except Exception as e:
        st.error(f"⚠️ Format tanggal tidak valid. Error: {e}")
        st.stop()

    df.set_index('tanggal', inplace=True)

    # Ganti koma jadi titik (jika ada nilai string desimal)
    df = df.apply(lambda x: x.astype(str).str.replace(',', '.'), axis=0)

    # Hanya gunakan kolom numerik
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except:
            st.warning(f"⚠️ Kolom '{col}' dihapus karena bukan numerik.")
            df.drop(columns=[col], inplace=True)

    if df.empty:
        st.error("❌ Tidak ada kolom numerik yang tersedia untuk prediksi.")
        st.stop()

    return df

# ──────────────────────────────────────────────────────────────
# 2. SERIES TO SUPERVISED
# ──────────────────────────────────────────────────────────────
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    df = pd.DataFrame(data)
    cols, names = [], []
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [f'var{j+1}(t-{i})' for j in range(df.shape[1])]
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        names += [f'var{j+1}(t+{i})' for j in range(df.shape[1])]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# ──────────────────────────────────────────────────────────────
# 3. PLOTTING
# ──────────────────────────────────────────────────────────────
def plot_forecast(df, forecast_df):
    for col in df.columns:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name='Historikal', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[col], name='Prakiraan', line=dict(color='orange')))
        fig.update_layout(title=f"Historikal & Forecast: {col}",
                          xaxis_title="Tanggal",
                          yaxis_title=col,
                          xaxis=dict(rangeslider=dict(visible=True), type="date"))
        st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 4. STREAMLIT APP
# ──────────────────────────────────────────────────────────────
def app():
    st.title("⛅ Prediksi Cuaca Kota Surabaya")

    df = load_and_prepare_data("data/df_hujan.csv")
    st.subheader("📊 Data Historikal Cuaca")
    st.dataframe(df)

    try:
        model = keras_model("model/prediksi_cuaca_lstm_mls6.h5")
    except Exception as e:
        st.error(f"❌ Gagal memuat model: {e}")
        return

    n_day = st.number_input("Masukkan Jumlah Hari Untuk Prediksi", min_value=1, max_value=30, value=7)

    if st.button("🔮 Prediksi"):
        with st.spinner("Sedang memproses prediksi..."):
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df)

            n_back = 3
            n_feat = df.shape[1]
            supervised = series_to_supervised(df_scaled, n_back, 1)
            input_data = supervised.values[:, :n_back * n_feat]

            forecasts = []
            for i in range(n_day):
                seq = input_data[-1].reshape((1, n_back, n_feat))
                pred = model.predict(seq, verbose=0)
                forecasts.append(pred[0])

                next_input = np.append(input_data[-1][n_feat:], pred[0])
                input_data = np.vstack([input_data, next_input])

            fcst_array = scaler.inverse_transform(np.array(forecasts))
            fcst_df = pd.DataFrame(fcst_array,
                                   index=pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=n_day),
                                   columns=df.columns)

            st.subheader("📈 Grafik Perkiraan Cuaca")
            plot_forecast(df, fcst_df)

# Jalankan langsung jika dieksekusi
if __name__ == "__main__":
    app()
