import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("amazon_prime_titles.csv")

# Sidebar filters
st.sidebar.title("Filters")
type_filter = st.sidebar.multiselect("Choose type:", options=df['type'].dropna().unique(), default=df['type'].dropna().unique())

year_min, year_max = int(df['release_year'].min()), int(df['release_year'].max())
year_range = st.sidebar.slider("Select year range:", min_value=year_min, max_value=year_max, value=(2000, 2020))

selected_genres = st.sidebar.multiselect("Choose genres:", options=df['listed_in'].dropna().unique(), default=[])
show_trendline = st.sidebar.checkbox("Add trendline to yearly count")

# Filter data
filtered_df = df[df['type'].isin(type_filter) &
                 df['release_year'].between(year_range[0], year_range[1])]
if selected_genres:
    filtered_df = filtered_df[filtered_df['listed_in'].isin(selected_genres)]

st.title("Amazon Prime Data Analysis")

# 1. Histogram - release_year with optional trendline
st.subheader("Titles by Release Year")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=filtered_df, x='release_year', bins=30, ax=ax)
if show_trendline:
    yearly_counts = filtered_df.groupby('release_year').size()
    sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, color='red', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

# 2. Top genres
st.subheader("Top Genres")
top_genres = filtered_df['listed_in'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)
ax.set_xlabel("Count")
ax.set_ylabel("Genre")
st.pyplot(fig)

# 3. Rating distribution
st.subheader("Rating Distribution")
rating_order = sorted(df['rating'].dropna().unique())
fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(data=filtered_df[filtered_df['rating'].notna()], x='rating', order=rating_order, ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
plt.xticks(rotation=45)
st.pyplot(fig)
