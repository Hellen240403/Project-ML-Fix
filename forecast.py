import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from keras.models import load_model as keras_model
from sklearn.preprocessing import MinMaxScaler

# =========================
# Fungsi Load Dataset
# =========================
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, delimiter=';')
        df.columns = df.columns.str.strip().str.lower()
        if 'tanggal' not in df.columns:
            st.error("Kolom 'tanggal' tidak ditemukan dalam file CSV.")
            return None
        df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True, errors='coerce')
        df.dropna(subset=['tanggal'], inplace=True)
        df.set_index('tanggal', inplace=True)
        return df
    except Exception as e:
        st.error(f"Gagal membaca file data: {e}")
        return None

# =========================
# Fungsi Load Model .pkl (Jika ada)
# =========================
def load_model(file_path):
    try:
        with open(file_path, 'rb') as model_in:
            model = pickle.load(model_in)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

# =========================
# Fungsi Series to Supervised
# =========================
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if isinstance(data, list) else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [(f'var{j+1}(t-{i})') for j in range(n_vars)]
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [(f'var{j+1}(t)') for j in range(n_vars)]
        else:
            names += [(f'var{j+1}(t+{i})') for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# =========================
# Fungsi Plot
# =========================
def plot_forecast(df, forecast_df):
    for column in df.columns:
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name='Historikal', line=dict(color='cyan')), row=1, col=1)
        fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[column], mode='lines', name='Prakiraan', 
                                 line=dict(color='magenta')), row=1, col=1)

        if not df.empty and not forecast_df.empty:
            fig.add_trace(go.Scatter(x=[df.index[-1], forecast_df.index[0]],
                                     y=[df[column].iloc[-1], forecast_df[column].iloc[0]],
                                     mode='lines', line=dict(color='magenta'), showlegend=False), row=1, col=1)

        fig.update_layout(
            title=f'Historikal vs Prakiraan {column}',
            xaxis_title='Tanggal',
            yaxis_title=column,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================
# Fungsi Aplikasi Streamlit
# =========================
def app():
    st.title('⛅ Prediksi Cuaca Kota Surabaya Menggunakan LSTM')
    st.write("""Prediksi cuaca Kota Surabaya menggunakan algoritma Long Short-Term Memory (LSTM) berdasarkan data histori cuaca tahun 2023.""")

    # Load data
    filepath = 'data/df_hujan.csv'
    df = load_data(filepath)
    if df is None:
        return

    st.subheader("Data Historis Cuaca")
    st.dataframe(df, use_container_width=True)

    # Load model
    try:
        forecaster = keras_model('model/prediksi_cuaca_lstm_mls6.h5')
    except Exception as e:
        st.error(f"Gagal memuat model LSTM: {e}")
        return

    # Input jumlah hari prediksi
    n_forecast_days = st.number_input('Silakan isi jumlah hari yang ingin Anda prediksi:', min_value=1, max_value=30, value=7)

    if st.button('Mulai Prediksi'):
        with st.spinner('Mohon tunggu... sedang memproses prediksi...'):
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df)
            n_days = 3
            n_features = df.shape[1]

            test_data_supervised = series_to_supervised(df_scaled, n_days, 1)
            test_data_sequences = test_data_supervised.values[:, :n_days * n_features]

            forecast = []
            last_seq = test_data_sequences[-1].reshape((1, n_days, n_features))

            for _ in range(n_forecast_days):
                pred = forecaster.predict(last_seq, verbose=0)
                forecast.append(pred[0])
                last_seq = np.append(last_seq[:, 1:, :], [[pred[0]]], axis=1)

            forecast_array = np.array(forecast)
            forecast_inverse = scaler.inverse_transform(forecast_array)
            forecast_inverse = np.abs(forecast_inverse)
            forecast_inverse = np.round(forecast_inverse, 2)

            date_range = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=n_forecast_days)
            forecast_df = pd.DataFrame(forecast_inverse, index=date_range, columns=df.columns)

            st.subheader("Hasil Perkiraan Cuaca")
            st.dataframe(forecast_df)
            plot_forecast(df, forecast_df)
