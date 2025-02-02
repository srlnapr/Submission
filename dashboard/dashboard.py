import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import plotly.express as px

# Membaca data
@st.cache_data
def load_data():
    file_path = os.path.join('dashboard', 'all_data.csv')  # Path relatif
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"File CSV tidak ditemukan di lokasi yang diharapkan: {file_path}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika file tidak ditemukan

df = load_data()

# Pastikan kolom tanggal ada dan diubah menjadi datetime
if 'order_purchase_timestamp' in df.columns:
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
else:
    st.warning("Kolom 'order_purchase_timestamp' tidak ditemukan dalam dataset.")

# 1. Persiapkan data untuk analisis RFM
def calculate_rfm(df):
    current_date = df['order_purchase_timestamp'].max()
    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (current_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'payment_value': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    return rfm

# 2. Hitung RFM scores
def calculate_rfm_scores(rfm):
    rfm['recency'] = rfm['recency'].replace(0, 1)
    rfm['monetary'] = rfm['monetary'].replace(0, 1)
    rfm['R'] = pd.qcut(rfm['recency'].rank(method='first'), q=5, labels=[5, 4, 3, 2, 1])
    rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
    rfm['M'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
    return rfm

# 3. Tentukan segmen customer
def segment_customers(rfm):
    def get_segment(row):
        if row['R'] >= 4 and row['F'] >= 4:
            return 'Champions'
        elif row['F'] >= 4:
            return 'Loyal Customers'
        elif row['R'] >= 4:
            return 'Recent Customers'
        elif row['F'] >= 3 and row['M'] >= 3:
            return 'Regular Customers'
        elif row['R'] >= 2:
            return 'At Risk'
        else:
            return 'Lost Customers'
    
    rfm['Segment'] = rfm.apply(get_segment, axis=1)
    return rfm

# 4. Visualisasi hasil segmen
def plot_segment_distribution(rfm):
    segment_counts = rfm['Segment'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe']
    ax.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', 
           colors=colors, startangle=90)
    ax.set_title('Distribusi Segmen Customer')
    ax.axis('equal')
    st.pyplot(fig)

# 5. Menampilkan RFM di Streamlit
def display_rfm_data(rfm_segmented):
    st.subheader("Hasil Analisis RFM")
    st.dataframe(rfm_segmented)

# Main execution
def main():
    # Menghitung RFM metrics
    rfm_df = calculate_rfm(df)
    
    # Menghitung RFM scores
    rfm_scored = calculate_rfm_scores(rfm_df)
    
    # Segmentasi pelanggan
    rfm_segmented = segment_customers(rfm_scored)
    
    # Menampilkan hasil RFM
    display_rfm_data(rfm_segmented)
    
    # Menampilkan visualisasi distribusi segmen pelanggan
    plot_segment_distribution(rfm_segmented)

    # Menyimpan hasil
    rfm_segmented.to_csv('rfm_results.csv', index=False)

    return rfm_segmented

# Streamlit Sidebar
st.sidebar.header("Filter Berdasarkan Segmen")

# Menambahkan filter berdasarkan segmen
segment_filter = st.sidebar.selectbox("Pilih Segmen", ['All', 'Champions', 'Loyal Customers', 'Recent Customers', 'Regular Customers', 'At Risk', 'Lost Customers'])

# Menjalankan analisis dan menampilkan hasil
rfm_results = main()

# Memfilter berdasarkan segmen yang dipilih
if segment_filter != 'All':
    rfm_filtered = rfm_results[rfm_results['Segment'] == segment_filter]
    st.subheader(f"Data untuk Segmen: {segment_filter}")
    st.dataframe(rfm_filtered)
else:
    st.subheader("Data untuk Semua Segmen")
    st.dataframe(rfm_results)
