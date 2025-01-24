import pandas as pd
from upsetplot import from_memberships, UpSet
import matplotlib.pyplot as plt
import streamlit as st

st.title('Upset Plot Visualisasi Sumber Lead')

def process_and_plot(df):
    # remove coma di data
    df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)

    # kolom pertama diabaikan
    categories = df.columns[1:]
    
    # combinations
    df_combinations = pd.DataFrame({
        "Combination": categories,
        "Count": df.iloc[0, 1:].values
    })
    
    # comb kolom
    df_combinations["Combination"] = df_combinations["Combination"].astype(str)
    
    # convert
    upset_data = from_memberships(
        memberships=[comb.split(", ") for comb in df_combinations["Combination"]],
        data=df_combinations["Count"]
    )
    
    # upset plot
    upset_plot = UpSet(upset_data, show_counts=True)
    upset_plot.plot()
    
    # plot
    st.pyplot(plt)

# upload file CSV
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    st.write("Data yang diupload:")
    st.write(df)
    
    process_and_plot(df)
