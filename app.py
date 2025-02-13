import pandas as pd
from upsetplot import from_memberships, UpSet
import matplotlib.pyplot as plt
import streamlit as st
import re

st.title('Upset Plot Visualisasi Sumber Lead')

# Mapping untuk normalisasi nama kategori
KATEGORI_MAP = {
    'Google': 'Google Ads',
    'Meta': 'Meta Ads',
    'SEO': 'SEO',
    'Sosmed': 'Sosmed'
}

KATEGORI_ORDER = ['Google Ads', 'Meta Ads', 'SEO', 'Sosmed']

def parse_kombinasi(nama_kombinasi):
    nama_kombinasi = nama_kombinasi.strip()
    
    if nama_kombinasi == 'All Four':
        return KATEGORI_ORDER
    
    if nama_kombinasi.endswith(' Only'):
        kategori = nama_kombinasi.replace(' Only', '')
        return [KATEGORI_MAP.get(kategori, kategori)]
    
    # Split kombinasi dengan berbagai delimiter
    parts = re.split(r', | & ', nama_kombinasi)
    
    # Normalisasi dan filter kategori
    kategori_terdaftar = []
    for part in parts:
        kategori = KATEGORI_MAP.get(part, part)
        if kategori in KATEGORI_ORDER:
            kategori_terdaftar.append(kategori)
    
    return sorted(list(set(kategori_terdaftar)))

def proses_dan_plot(df):
    # Bersihkan data numerik
    df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)
    df.iloc[:, 5:] = df.iloc[:, 5:].astype(int)

    # Ekstrak kombinasi dan hitungan
    kombinasi = df.columns[5:]
    df_kombinasi = pd.DataFrame({
        'Kombinasi': kombinasi,
        'Jumlah': df.iloc[0, 5:].values
    })

    # Parse semua kombinasi
    df_kombinasi['Membership'] = df_kombinasi['Kombinasi'].apply(parse_kombinasi)
    
    # Buat data upset
    data_upset = from_memberships(
        df_kombinasi['Membership'].tolist(),
        data=df_kombinasi['Jumlah']
    )
    
    # Buat plot dengan urutan kategori yang ditentukan
    upset = UpSet(
        data_upset,
        show_counts=True,
        sort_by='cardinality',
        category_order=KATEGORI_ORDER
    )
    
    fig, ax = plt.subplots()
    upset.plot(fig=fig)
    st.pyplot(fig)

# Upload file
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data yang diupload:")
    st.write(df)
    proses_dan_plot(df)