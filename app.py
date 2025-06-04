import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Amazon Prime Titles – Data Exploration App")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("amazon_prime_titles.csv")
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df['duration_clean'] = df['duration'].str.extract('(\d+)').astype(float)
    df['listed_in'] = df['listed_in'].str.split(', ')
    return df.explode('listed_in')

df = load_data()

# Sidebar options
options = [
    "Release Year",
    "Type Distribution",
    "Genres",
    "TV vs Movie Trends",
    "Ratings",
    "Top Directors"
]
choice = st.sidebar.radio("Choose a chart to display:", options)

# 1. Release Year Distribution
if choice == "Release Year":
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df['release_year'], bins=30, ax=ax)
    ax.set_title("Histogram: Release Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# 2. Type Distribution
elif choice == "Type Distribution":
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(data=df, x='type', ax=ax)
    ax.set_title("Bar Chart: Movie vs TV Show")
    st.pyplot(fig)

# 3. Genre Distribution (Top 10)
elif choice == "Genres":
    top_genres = df['listed_in'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_genres.index, y=top_genres.values, ax=ax)
    ax.set_title("Top 10 Genres")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 4. Percent of TV vs Movie Over Time
elif choice == "TV vs Movie Trends":
    df_count = df.groupby(['release_year', 'type']).size().reset_index(name='count')
    df_count['total'] = df_count.groupby('release_year')['count'].transform('sum')
    df_count['percent'] = df_count['count'] / df_count['total'] * 100
    df_count = df_count[df_count['release_year'] >= 1980]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_count, x='release_year', y='percent', hue='type', ax=ax)
    ax.set_title("Percent of Movies and TV Shows by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percent")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 5. Rating Distribution (Messy)
elif choice == "Ratings":
    fig, ax = plt.subplots(figsize=(12, 5))
    rating_order = sorted(df['rating'].dropna().unique())
    sns.countplot(data=df[df['rating'].notna()], x='rating', order=rating_order, ax=ax)
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 6. Top 10 Directors
elif choice == "Top Directors":
    top_directors = df['director'].dropna().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_directors.values, y=top_directors.index, ax=ax)
    ax.set_title("Top 10 Directors")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Director")
    st.pyplot(fig)
