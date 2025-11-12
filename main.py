from Apriori import Apriori 
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def visualize():
    for level, data in ap.freq_sets.items():
        df = pd.DataFrame({
            "itemset": [str(d.items) for d in data],
            "sup": [d.sup for d in data]
        })

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df['itemset'], df['sup'])
        ax.set_xlabel("Itemset")
        ax.set_ylabel("Support")
        ax.set_title(f"Frequent Itemsets ({level})")
        plt.xticks(rotation=45)

        st.pyplot(fig)

    for level, data in ap.itemsets.items():
        df = pd.DataFrame({
            "itemset": [str(d.items) for d in data],
            "sup": [d.sup for d in data]
        })

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df['itemset'], df['sup'])
        ax.set_xlabel("Itemset")
        ax.set_ylabel("Support")
        ax.set_title(f"Itemsets ({level})")
        plt.xticks(rotation=45)

        st.pyplot(fig)

st.title("Frequent Patterns Mining Using Apriori Algortihm")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv", "xlsx"])
min_sup = st.slider("Select minimum support", min_value=1, max_value=10, step=1, value=2)

if uploaded_file is not None:
    if uploaded_file.name.endswith("xlsx"):
        df=pd.read_excel(uploaded_file)
    else:
        df =pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("Run Apriori Algorithm"):
        ap = Apriori(uploaded_file.name, min_sup)
        ap.run()
        visualize()
        st.balloons()
else:
    st.info("Please upload a CSV or XLSX file.")

# ap.visualize()