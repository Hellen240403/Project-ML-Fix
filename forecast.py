import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from keras.models import load_model as keras_model
from sklearn.preprocessing import MinMaxScaler

# ──────────────────────────────────────────────────────────────
# 1.  LOAD & PREPARE  DATA
# ──────────────────────────────────────────────────────────────
def load_and_prepare_data(filepath: str) -> pd.DataFrame:
    # pakai delimiter ;  dan force engine python (lebih toleran)
    df = pd.read_csv(filepath, sep=';', engine='python')
    
    # normalisasi kolom → huruf kecil + strip spasi
    df.columns = df.columns.str.strip().str.lower()
    
    # ❤️  tangani kemungkinan karakter aneh (BOM / invisible char)
    for col in df.columns:
        if col.replace('\ufeff', '') == 'tanggal':
            df.rename(columns={col: 'tanggal'}, inplace=True)
            break

    # validasi
    if 'tanggal' not in df.columns:
        st.error(f"Kolom 'tanggal' tidak ditemukan. Kolom yang terbaca: {df.columns.tolist()}")
        st.stop()
    
    # konversi tanggal (DD/MM/YYYY)
    df['tanggal'] = pd.to_datetime(df['tanggal'], format='%d/%m/%Y')
    df.set_index('tanggal', inplace=True)

    return df

# ──────────────────────────────────────────────────────────────
# 2.  TAMPILKAN  TANGGAL
# ──────────────────────────────────────────────────────────────
def tampilkan_tanggal(df: pd.DataFrame) -> None:
    st.subheader("📅 Daftar Tanggal Tersedia")
    # tampilkan sebagai list simpel
    st.write(df.index.strftime('%Y-%m-%d').tolist())

# ──────────────────────────────────────────────────────────────
# 3.  MODEL & UTIL LAINNYA  (tidak diubah)
# ──────────────────────────────────────────────────────────────
def load_pickle_model(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Gagal load model pickle: {e}")

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if isinstance(data, list) else data.shape[1]
    df_sup, names = [], []
    for i in range(n_in, 0, -1):
        df_sup.append(pd.DataFrame(data).shift(i))
        names += [f'var{j+1}(t-{i})' for j in range(n_vars)]
    for i in range(0, n_out):
        df_sup.append(pd.DataFrame(data).shift(-i))
        names += [f'var{j+1}(t+{i})' for j in range(n_vars)]
    agg = pd.concat(df_sup, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def plot_forecast(df, forecast_df):
    for col in df.columns:
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name='Historikal', line=dict(color='cyan')), row=1, col=1)
        fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[col], mode='lines', name='Prakiraan', line=dict(color='magenta')), row=1, col=1)
        if not df.empty and not forecast_df.empty:
            fig.add_trace(go.Scatter(x=[df.index[-1], forecast_df.index[0]],
                                     y=[df[col].iloc[-1], forecast_df[col].iloc[0]],
                                     mode='lines', line=dict(color='magenta'), showlegend=False), row=1, col=1)
        fig.update_layout(title=f'Historikal vs Prakiraan {col}',
                          xaxis_title='Tanggal', yaxis_title=col,
                          xaxis=dict(rangeslider=dict(visible=True), type='date'))
        st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 4.  HALAMAN STREAMLIT
# ──────────────────────────────────────────────────────────────
def app():
    st.title("☁️ Prediksi Cuaca Surabaya")

    df = load_and_prepare_data("data/df_hujan.csv")
    tampilkan_tanggal(df)
    st.dataframe(df, use_container_width=True)

    forecaster = keras_model("model/prediksi_cuaca_lstm_mls6.h5")

    if forecaster:
        n_day = st.number_input("Jumlah hari yang ingin diprediksi", 1, 30, 7)
        if st.button("🔮 Prediksi"):
            with st.spinner("Menghitung..."):
                scaler = MinMaxScaler()
                df_scaled = scaler.fit_transform(df)
                n_back = 3
                n_feat = df.shape[1]
                seq_data = series_to_supervised(df_scaled, n_back, 1).values[:, :n_back*n_feat]

                forecasts = []
                for i in range(n_day):
                    seq = seq_data[i].reshape((1, n_back, n_feat))
                    pred = forecaster.predict(seq, verbose=0)
                    forecasts.append(pred[0])

                fcst = scaler.inverse_transform(np.array(forecasts))
                fcst = np.round(np.abs(fcst), 2)

                idx = pd.date_range(start=df.index[-1], periods=n_day+1)[1:]
                forecast_df = pd.DataFrame(fcst, index=idx, columns=df.columns)

                st.subheader("📊 Hasil Perkiraan Cuaca (LSTM)")
                plot_forecast(df, forecast_df)

# jalankan di mode mandiri
if __name__ == "__main__":
    app()
