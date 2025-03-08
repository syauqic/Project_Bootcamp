import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    df_orders = pd.read_csv("data/olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    df_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
    return df_orders, df_reviews

df_orders, df_reviews = load_data()

# Sidebar Navigation
st.sidebar.title("E-Commerce Analysis")
page = st.sidebar.radio("Pilih Analisis:", ["Tren Jumlah Pesanan", "Distribusi Rating Pelanggan"])

if page == "Tren Jumlah Pesanan":
    st.title("📈 Tren Jumlah Pesanan dari Waktu ke Waktu")
    
    # Resample jumlah pesanan per bulan
    monthly_orders = df_orders.set_index("order_purchase_timestamp").resample("M").size()
    
    # Visualisasi Line Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_orders, marker='o', linestyle='-', color='b')
    ax.set_title("Tren Jumlah Pesanan dari Waktu ke Waktu")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pesanan")
    ax.grid(True)
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    st.markdown("Dari grafik line chart, terlihat bahwa jumlah pesanan mengalami peningkatan signifikan dari waktu ke waktu, terutama mulai awal 2017 hingga akhir 2018. Tren ini menunjukkan bahwa platform e-commerce mengalami pertumbuhan dalam jumlah transaksi, dengan lonjakan yang tajam di beberapa periode tertentu. Setelah mencapai puncaknya, jumlah pesanan cenderung stabil dengan sedikit fluktuasi.")

elif page == "Distribusi Rating Pelanggan":
    st.title("⭐ Distribusi Nilai Rating Pelanggan")
    
    # Histogram Distribusi Rating
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_reviews['review_score'], bins=5, kde=True, color='skyblue', ax=ax)
    ax.set_title("Distribusi Nilai Rating Pelanggan")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Ulasan")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig)
    
    # Boxplot untuk Outlier
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=df_reviews['review_score'], color='orange', ax=ax)
    ax.set_title("Boxplot Nilai Rating Pelanggan")
    ax.set_xlabel("Rating")
    
    st.pyplot(fig)
    st.markdown("Dari histogram, mayoritas pelanggan memberikan rating tinggi, terutama rating 5, yang mendominasi jumlah ulasan. Sebagian kecil pelanggan memberikan rating rendah (1 dan 2), tetapi jumlahnya jauh lebih sedikit dibandingkan rating tinggi. Boxplot menunjukkan adanya outlier pada rating 1 dan 2, yang menandakan ada sejumlah kecil pelanggan yang sangat tidak puas dengan layanan atau produk. Secara keseluruhan, rating pelanggan lebih condong ke positif, menunjukkan bahwa sebagian besar pelanggan puas dengan pengalaman mereka.")