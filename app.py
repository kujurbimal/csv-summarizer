import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="CSV Summarizer", layout="wide")

st.title("📊 CSV Summarizer")
st.markdown("Upload a CSV file to get instant insights into your data.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Basic Summary")
        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

        st.subheader("🧮 Column Statistics")
        summary = df.describe(include='all').transpose()
        summary['Missing Values'] = df.isnull().sum()
        st.dataframe(summary)

        st.subheader("🔢 Data Types")
        st.dataframe(df.dtypes.rename("Data Type"))

        st.subheader("🚨 Missing Data Heatmap")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(df.isnull(), cbar=False, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.subheader("📊 Numeric Column Distributions")
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in num_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
            st.pyplot(fig)

        st.subheader("🔠 Top Categories in Categorical Columns")
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            st.markdown(f"**{col}**")
            st.write(df[col].value_counts().head(5))

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
