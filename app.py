import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Tracker Keuangan Mahasiswa")

#Form Input Transaksi
nama = st.text_input("Nama kamu")
tanggal = st.date_input("Tanggal")

jenis = st.selectbox(
    "Jenis",
    ["Pemasukan", "Pengeluaran"]
)

kategori = st.text_input("Kategori")

nominal = st.number_input(
    "Nominal",
    min_value=0
)

#Simpan Data Transaksi
if st.button("💾 Simpan"):
    transaksi = pd.DataFrame({
        "nama": [nama],
        "tanggal": [tanggal],
        "jenis": [jenis],
        "kategori": [kategori],
        "nominal": [nominal]
    })

# Simpan data ke file CSV
    transaksi.to_csv(
        "transaksi.csv",
        mode="a",
        header=False,
        index=False
    )
    st.success("✅ Data berhasil disimpan!")
   
#Preview Data   
st.write("Preview Data:")
st.write({
    "nama": nama,
    "tanggal": tanggal,
    "jenis": jenis,
    "kategori": kategori,
    "nominal": nominal
})

#Riwayat Transaksi
st.subheader("📋 Riwayat Transaksi")

data = pd.read_csv("transaksi.csv")
data["tanggal"] = pd.to_datetime(data["tanggal"])

bulan = st.selectbox(
"Pilih Bulan",
data["tanggal"].dt.to_period("M").astype(str).unique()
)

data = data[
    data["tanggal"].dt.to_period("M").astype(str)==bulan
    ]

st.dataframe(data)
st.download_button(
   label = "Tekan untuk Download Data",
   data = data.to_csv(index=False),
   file_name = "transaksi.csv",
   mime = "text/csv"
)

#Tampilkan Ringkasan Keuangan
st.subheader("📊 Ringkasan Keuangan")
pemasukan = data[data["jenis"] == "Pemasukan"]
pengeluaran = data[data["jenis"] == "Pengeluaran"]

total_pemasukan = pemasukan["nominal"].sum()
total_pengeluaran = pengeluaran["nominal"].sum()

saldo = total_pemasukan - total_pengeluaran

st.metric(label = "Total Pemasukan",
          value = f"Rp {total_pemasukan:,}"
         )

st.metric(label = "Total Pengeluaran",
          value = f"Rp {total_pengeluaran:,}"
          )

st.metric(label = "Saldo",
          value = f"Rp {saldo:,}"
          )

st.write(data)

#Grafik Keuangan Pemasukan
st.subheader("📈 Grafik Keuangan Pemasukan")
pemasukan_kategori = (
    pemasukan.groupby("kategori")["nominal"].sum()
)
st.dataframe(pemasukan_kategori)

if not pemasukan_kategori.empty:
    fig, ax = plt.subplots()

    pemasukan_kategori.plot(
        kind="bar",
        ax=ax
    )
    st.pyplot(fig)
else: 
    st.info("Belum ada data pemasukan untuk ditampilkan.")

#Grafik Keuangan Pengeluaran
st.subheader("📈 Grafik Keuangan Pengeluaran")
pengeluaran_kategori = (
    pengeluaran.groupby("kategori")["nominal"].sum()
    )
st.dataframe(pengeluaran_kategori)

if not pengeluaran_kategori.empty:
    fig, ax = plt.subplots()

    pengeluaran_kategori.plot(
        kind="bar",
        ax=ax
    )
    st.pyplot(fig)
else:
    st.info("Belum ada data pengeluaran untuk ditampilkan.")

#pie chart pemasukan
st.subheader("📊 Pie Chart Pemasukan")
fig, ax = plt.subplots()
ax.pie(
    pemasukan_kategori,
    labels = pemasukan_kategori.index,
    autopct = "%1.1f%%",
    startangle = 90
)
ax.set_title("Persentase Pemasukan")
st.pyplot(fig)


#pie chart pengeluaran
st.subheader("📊 Pie Chart Pengeluaran")
fig, ax = plt.subplots()
ax.pie(
    pengeluaran_kategori,
    labels = pengeluaran_kategori.index,
    autopct = "%1.1f%%",
    startangle = 90
)
ax.set_title("Persentase Pengeluaran")
st.pyplot(fig)
