import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Title
st.title("🎬 Netflix Analytics Dashboard")

# Load data
data = pd.read_csv("netflix_titles.csv")

# Cleaning
data['director'] = data['director'].fillna('Unknown')
data['cast'] = data['cast'].fillna('Unknown')
data['country'] = data['country'].fillna('Unknown')
data['rating'] = data['rating'].fillna('Unknown')

# Fix date
data['date_added'] = data['date_added'].str.strip()
data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')
data['year_added'] = data['date_added'].dt.year

# ================= SIDEBAR FILTERS =================
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=data['type'].unique(),
    default=data['type'].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=data['country'].unique(),
    default=data['country'].unique()[:5]
)

year_filter = st.sidebar.slider(
    "Select Year Range",
    int(data['release_year'].min()),
    int(data['release_year'].max()),
    (2015, 2021)
)

rating_filter = st.sidebar.multiselect(
    "Select Rating",
    options=data['rating'].unique(),
    default=data['rating'].unique()
)

# Apply filters
filtered_data = data[
    (data['type'].isin(type_filter)) &
    (data['country'].isin(country_filter)) &
    (data['release_year'].between(year_filter[0], year_filter[1])) &
    (data['rating'].isin(rating_filter))
]

# ================= KPI =================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Content", len(filtered_data))
col2.metric("Movies", len(filtered_data[filtered_data['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_data[filtered_data['type'] == 'TV Show']))

# ================= CHARTS =================

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    fig, ax = plt.subplots()
    filtered_data['type'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Content Added Over Time")
    fig, ax = plt.subplots()
    filtered_data['year_added'].value_counts().sort_index().plot(ax=ax)
    st.pyplot(fig)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Countries")
    fig, ax = plt.subplots()
    filtered_data['country'].value_counts().head(10).plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col4:
    st.subheader("Top Genres")
    fig, ax = plt.subplots()
    filtered_data['listed_in'].value_counts().head(10).plot(kind='barh', ax=ax)
    st.pyplot(fig)

# Row 3 (NEW CHARTS)
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top Directors")
    fig, ax = plt.subplots()
    filtered_data['director'].value_counts().head(10).plot(kind='barh', ax=ax)
    st.pyplot(fig)

with col6:
    st.subheader("Ratings Distribution")
    fig, ax = plt.subplots()
    filtered_data['rating'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)
