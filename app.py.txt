import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Amazon Prime Dataset Analysis")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("amazon_prime_titles.csv")
    return df

df = load_data()

st.markdown("""
### What is this app?
This is a simple Streamlit app to explore the Amazon Prime Movies and TV Shows dataset.
You can scroll and see different visualizations we made during the project.
""")

# Dataset preview
st.subheader("Preview of Dataset")
st.dataframe(df.head())

# Chart 1: Release Year Histogram
st.subheader("1. Release Year - Histogram")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(data=df, x='release_year', bins=30, ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# Chart 2: Top 10 Genres
st.subheader("2. Top 10 Genres")
df_genres = df.copy()
df_genres['listed_in'] = df_genres['listed_in'].str.split(', ')
df_genres = df_genres.explode('listed_in')
top_genres = df_genres['listed_in'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10, 4))
top_genres.plot(kind='bar', ax=ax2)
ax2.set_xlabel("Genre")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# Chart 3: Ratings (messy)
st.subheader("3. Rating - All Types")
fig3, ax3 = plt.subplots(figsize=(10, 4))
ratings_sorted = sorted(df['rating'].dropna().unique())
sns.countplot(data=df[df['rating'].notna()], x='rating', order=ratings_sorted, ax=ax3)
ax3.set_xlabel("Rating")
ax3.set_ylabel("Count")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Chart 4: TV vs Movie Percent per Year
st.subheader("4. Percent of Movies and TV Shows per Year")
year_type_counts = df.groupby(['release_year', 'type']).size().reset_index(name='count')
year_type_counts['total'] = year_type_counts.groupby('release_year')['count'].transform('sum')
year_type_counts['percent'] = year_type_counts['count'] / year_type_counts['total'] * 100
year_type_counts = year_type_counts[year_type_counts['release_year'] >= 1980]

fig4, ax4 = plt.subplots(figsize=(12, 4))
sns.barplot(data=year_type_counts, x='release_year', y='percent', hue='type', ax=ax4)
ax4.set_xlabel("Release Year")
ax4.set_ylabel("Percent")
plt.xticks(rotation=45)
st.pyplot(fig4)

# Footer
st.markdown("""
---
**Created by Student for Midterm Project**  
Based on dataset: amazon_prime_titles.csv
""")
