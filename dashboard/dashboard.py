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
st.sidebar.title("📊 E-Commerce Dashboard")
# st.sidebar.markdown("## 📊 E-Commerce Dashboard")
menu = st.sidebar.selectbox(
    "📁 Pilih Menu Analisis",
    options=["Tren Jumlah Pesanan", "Distribusi Rating Pelanggan"],
    index=0
)

# Halaman 1
if menu == "Tren Jumlah Pesanan":
    st.title("Tren Jumlah Pesanan dari Waktu ke Waktu")

    df_orders['year'] = df_orders['order_purchase_timestamp'].dt.year
    tahun_tersedia = sorted(df_orders['year'].unique())
    tahun_dipilih = st.selectbox("Pilih Tahun", tahun_tersedia)

    # Filter berdasarkan tahun
    df_filtered = df_orders[df_orders['year'] == tahun_dipilih]
    monthly_orders = df_filtered.set_index("order_purchase_timestamp").resample("M").size()
    df_monthly = monthly_orders.reset_index()
    df_monthly.columns = ['Bulan', 'Jumlah Pesanan']

    st.subheader(f"📅 Jumlah Pesanan per Bulan di Tahun {tahun_dipilih}")
    st.dataframe(df_monthly)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_monthly['Bulan'], df_monthly['Jumlah Pesanan'], marker='o', linestyle='-', color='b')
    ax.set_title(f"Tren Pesanan Tahun {tahun_dipilih}")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown(f"""
    **Insight:**
    Pada tahun **{tahun_dipilih}**, terlihat fluktuasi pesanan setiap bulan. Hal ini bisa mencerminkan tren belanja musiman, promosi, atau hari besar.
    """)

# Halaman 2
elif menu == "Distribusi Rating Pelanggan":
    st.title("Distribusi Nilai Rating Pelanggan")

    rating_unique = sorted(df_reviews['review_score'].unique())
    rating_pilihan = st.multiselect("Pilih Rating untuk Ditampilkan", rating_unique, default=rating_unique)

    df_filtered = df_reviews[df_reviews['review_score'].isin(rating_pilihan)]

    # Tampilkan tabel distribusi rating
    rating_counts = df_filtered['review_score'].value_counts().sort_index().reset_index()
    rating_counts.columns = ['Rating', 'Jumlah Ulasan']

    st.subheader("📊 Distribusi Rating (Berdasarkan Pilihan)")
    st.dataframe(rating_counts)

    # Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_filtered['review_score'], bins=5, kde=True, color='skyblue', ax=ax)
    ax.set_title("Histogram Rating Pelanggan")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Ulasan")
    st.pyplot(fig)

    # Checkbox: tampilkan tabel ulasan detail
    if st.checkbox("Tampilkan Detail Ulasan?"):
        st.write(df_filtered[['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message']].dropna().head(20))

    st.markdown(f"""
    **Insight:**
    Rating yang dipilih menunjukkan distribusi tertentu. Kamu bisa eksplorasi lebih lanjut untuk mencari tahu mengapa rating tertentu lebih dominan atau jarang muncul.
    """)
