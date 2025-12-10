import streamlit as st
import pandas as pd

st.set_page_config(page_title="Medical Dataset Explorer", layout="wide")

st.title("🩺 Medical Dataset Explorer")
st.write("Search and explore curated medical datasets for Machine Learning and Research.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/datasets.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

modality = st.sidebar.selectbox(
    "Select Modality",
    options=["All"] + sorted(df["modality"].dropna().unique().tolist())
)

task = st.sidebar.selectbox(
    "Select Task",
    options=["All"] + sorted(df["task"].dropna().unique().tolist())
)

disease = st.sidebar.text_input("Search Disease (keyword)")

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Apply filters
filtered_df = df.copy()

if modality != "All":
    filtered_df = filtered_df[filtered_df["modality"] == modality]

if task != "All":
    filtered_df = filtered_df[filtered_df["task"] == task]

if disease:
    filtered_df = filtered_df[
        filtered_df["disease"].str.contains(disease, case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df["year"] >= year_range[0]) & (filtered_df["year"] <= year_range[1])
]

# Display results
st.subheader(f"✅ Found {len(filtered_df)} dataset(s)")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download option
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download filtered datasets as CSV",
    data=csv,
    file_name="filtered_medical_datasets.csv",
    mime="text/csv"
)
