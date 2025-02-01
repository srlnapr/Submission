import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os

# Memuat data (pastikan file CSV Anda ada di lokasi yang benar)
@st.cache_data
def load_data():
    file_path = os.path.join('dashboard', 'all_data.csv')  # Path relatif
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"File CSV tidak ditemukan di lokasi yang diharapkan: {file_path}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika file tidak ditemukan

df = load_data()

# Periksa apakah data berhasil dimuat
if df.empty:
    st.stop()  # Jika data tidak ada, hentikan aplikasi

# Analisis: Produk yang paling banyak dijual
sum_order_items_df = df.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False).head(10)  # Top 10 kategori produk

# Streamlit Title
st.title("📊 Analisis Produk yang Paling Banyak Dijual")

# Tampilkan DataFrame
st.subheader("Top 10 Produk Paling Banyak Dijual")
st.dataframe(sum_order_items_df)

# Membuat horizontal bar chart dengan Altair
chart = alt.Chart(sum_order_items_df).mark_bar().encode(
    x=alt.X('products', title='Jumlah Produk'),
    y=alt.Y('product_category_name_english', sort='-x', title='Kategori Produk'),
    color=alt.Color('product_category_name_english', legend=None),
    tooltip=['product_category_name_english', 'products']
).properties(
    title='Kategori Produk Paling Banyak Dijual',
    width=700,
    height=400
)

# Menampilkan chart di Streamlit
st.altair_chart(chart, use_container_width=True)

# Mendapatkan jumlah review score
if 'review_score' in df.columns:
    review_scores = df['review_score'].value_counts()

    # Membuat visualisasi distribusi rating pembeli menggunakan Plotly
    fig = px.pie(
        names=review_scores.index,
        values=review_scores.values,
        title="Distribusi Rating Pembeli",
        color=review_scores.index,
        color_discrete_sequence=px.colors.sequential.Blues,
        labels={'value': 'Jumlah', 'review_score': 'Rating Pembeli'},
    )

    # Menampilkan chart di Streamlit
    st.plotly_chart(fig)

    # Tampilkan skor rating yang paling umum
    most_common_score = review_scores.idxmax()
    st.write(f"Rating paling umum adalah: **{most_common_score}**")
else:
    st.warning("Kolom 'review_score' tidak ditemukan dalam dataset.")
