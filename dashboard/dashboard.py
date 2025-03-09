import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_rent_weekday(df):
    sum_rent_weekday = day_df.groupby("weekday")["cnt"].sum().sort_values(ascending=False).reset_index()

    return sum_rent_weekday

def create_monthly_rent_df(df):
    df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    
    monthly_rent_df["dteday_str"] = monthly_rent_df["dteday"].dt.strftime('%Y-%m')  # Buat kolom string
    
    return monthly_rent_df

def create_sum_rent_users(df):
    sum_rent_users = day_df[["casual", "registered"]].sum()
    return sum_rent_users


def create_seasonal_rent_df(df):
    seasonal_rent_df = day_df.groupby("season")[["casual", "registered", "cnt"]].sum().reset_index()
    return seasonal_rent_df

day_df = pd.read_csv("dashboard/day_df_clean.csv")
hour_df = pd.read_csv("dashboard/hour_df_clean.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])



min_date_day = day_df["dteday"].min()
max_date_day = day_df["dteday"].max()

min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    st.image("tasha-kostyuk-_IKNpNUnKhg-unsplash.png")
    st.markdown(
        'Illustration by [Tasha Kostyuk](https://unsplash.com/@tashakostyuk?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) '
        'on [Unsplash](https://unsplash.com/illustrations/a-person-riding-a-bike-with-a-helmet-on-_IKNpNUnKhg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)',
        unsafe_allow_html=True
    )

    start_date, end_date = st.sidebar.date_input(
        "Rentang Waktu",
        [day_df["dteday"].min(), day_df["dteday"].max()],
        min_value=day_df["dteday"].min(),
        max_value=day_df["dteday"].max()
    )

main_day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) &
                         (day_df["dteday"] <= pd.to_datetime(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) &
                         (hour_df["dteday"] <= pd.to_datetime(end_date))]

sum_rent_weekday = create_sum_rent_weekday(main_day_df)
monthly_rent_df = create_monthly_rent_df(main_day_df)
sum_rent_users = create_sum_rent_users(main_day_df)
seasonal_rent_df = create_seasonal_rent_df(main_day_df)

st.header("Bike Sharing Dashboard 🚴")

# Penyewaan Sepeda Paling Banyak dan Paling Sedikit
st.subheader("Total Penyewaan Sepeda Harian")

fig, ax = plt.subplots(figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="weekday", data=sum_rent_weekday, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("Jumlah Penyewaan", fontsize=20)
ax.set_title("Hari dengan Sewa Sepeda Paling Banyak dan Paling Sedikit", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=20)

plt.tight_layout()
st.pyplot(fig)

# Tren sewa sepeda beberapa bulan terakhir
st.subheader("Tren Sewa Sepeda dalam Beberapa Bulan Terakhir")

fig, ax = plt.subplots(figsize=(20, 4))
ax.plot(monthly_rent_df["dteday"], monthly_rent_df["cnt"], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Tren Sewa Sepeda dalam Beberapa Bulan Terakhir", loc="center", fontsize=20)
ax.tick_params(axis='x', labelsize=10, rotation=45)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Perbandingan Pengguna Casual dan Registered
st.subheader("Pengguna Casual dan Registered")

colors = ["#D3D3D3", "#72BCD4"]
users = ["Casual", "Registered"]
explode = (0.1, 0)

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    x=sum_rent_users,
    labels=users,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode
)

ax.set_title("Perbandingan Jumlah Penyewa Sepeda: Casual vs. Registered", fontsize=10)
st.pyplot(fig)

st.write("### Seasonal Rentals")
seasonal_rent_df = main_day_df.groupby("season")[["casual", "registered", "cnt"]].sum().reset_index()
st.dataframe(seasonal_rent_df)


st.caption("© 2025 Bike Sharing Analysis")
