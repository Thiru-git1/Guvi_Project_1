import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import plotly.express as px

# --- MySQL Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/imdb_2024')

#Page Name change
st.set_page_config(page_title="IMDB 2024 Data Visuals", layout="centered")

# --- Streamlit function ---
st.title("IMDb 2024 Movie Data Visualizations Dashboard")

# 1. Top-Rated Movies: Identify the top 10 movies with the highest ratings and voting counts- Plot by bar chart
st.subheader("1. Top 10 Movies with Rating and Voting counts")
query_top10 = """SELECT * FROM IMDB_Movies_2024 ORDER BY Ratings DESC, Voting_counts DESC LIMIT 10;"""
top10_df = pd.read_sql(query_top10, engine)
st.dataframe(top10_df)
fig_bar = px.bar(top10_df,x='Title',y='Voting_counts',color='Ratings',title='Top 10 Rated movies',
                 hover_data=['Voting_counts'])
st.plotly_chart(fig_bar)

# 2. Genre Analysis: Explore the distribution of genres in the 2024 movie list -Plot by bar chart
st.subheader("2. Genre Analysis")
query_genre = """SELECT Genre, COUNT(*) AS Movie_Count FROM IMDB_Movies_2024 GROUP BY Genre ORDER BY Movie_Count DESC;"""
genre_df = pd.read_sql(query_genre, engine)
fig_genre = px.bar(genre_df,x="Genre",y="Movie_Count",title="Genre Distribution in 2024 Movies",color="Genre", 
            width=1000,height=600)
st.plotly_chart(fig_genre)

# 3. Duration Insights: Analyze the average duration of movies across genres -Plot by bar chart
st.subheader("3.Average Duration by Genre")
query_avg_duration = """SELECT Genre, AVG(Duration) AS Duration FROM IMDB_Movies_2024 GROUP BY Genre ORDER BY Duration DESC;"""
avg_dur_df = pd.read_sql(query_avg_duration, engine)
fig_duration = px.bar(avg_dur_df,x="Duration",y="Genre",title="Average Movie Duration by Genre",
               color="Duration",orientation='h',labels={"Duration": "Avg Duration (mins)"})
st.plotly_chart(fig_duration)

# 4. Voting Patterns: Discover genres with the highest average voting counts- Plot by bar chart
st.subheader("4. Average Voting counts across different genres")
query_votes = """SELECT Genre, AVG(Voting_counts) AS Avg_Votes FROM IMDB_Movies_2024 GROUP BY Genre ORDER BY Avg_Votes DESC;"""
votes_df = pd.read_sql(query_votes, engine)
fig_votes = px.bar(votes_df,x="Avg_Votes",y="Genre",orientation="h",color="Avg_Votes",title="Average Voting Counts by Genre",
            labels={"Avg_Votes": "Average Votes"},height=600,width=1000)
st.plotly_chart(fig_votes)

# 5. Rating Distribution: Analyze the distribution of ratings across all movies -display by histogram
st.subheader("5. Rating Distribution")
query_ratings = """SELECT Ratings FROM IMDB_Movies_2024;"""
ratings_df = pd.read_sql(query_ratings, engine)
fig_hist = px.histogram(ratings_df,x="Ratings",nbins=20,title="Distribution of Movie Ratings",labels={"Ratings": "IMDb Rating"},
           color_discrete_sequence=["teal"],opacity=0.75)
st.plotly_chart(fig_hist)
 
#6.Genre-Based Rating Leaders: Highlight the top-rated movie for each genre- display in a table.
st.subheader("6. Top-Rated Movie in Each Genre")
query = """SELECT Genre, Ratings, Title FROM IMDB_Movies_2024 WHERE Ratings >= 8.0"""
df = pd.read_sql(query, engine)
top_movies_by_genre = df.loc[df.groupby('Genre')['Ratings'].idxmax()] # retrieve top-rated movie per genre using pandas
st.dataframe(top_movies_by_genre[['Genre', 'Title', 'Ratings']], use_container_width=True)

# Genre vs. Ratings: Compare the average ratings for each genre -# Plot by bar chart
st.subheader("Genre vs. Ratings")
query_avg_rating = """ SELECT Genre, AVG(Ratings) AS Avg_Rating FROM IMDB_Movies_2024 
GROUP BY Genre 
ORDER BY Avg_Rating DESC;
"""
avg_rating_df = pd.read_sql(query_avg_rating, engine)
fig_genre_rating = px.bar(avg_rating_df,x="Genre",y="Avg_Rating",title="Average Ratings by Genre",color="Genre",
                   labels={"Avg_Rating": "Average IMDb Rating"},height=700,width=1000)
st.plotly_chart(fig_genre_rating)

#7. Most Popular Genres by Voting: Identify genres with the highest total voting counts- plot by pie chart.
st.subheader("7. Most Popular Genres by Voting Counts")
# SQL: Aggregate total votes per genre
query_popular_genres = """SELECT Genre, SUM(Voting_counts) AS Total_Votes FROM IMDB_Movies_2024 
GROUP BY Genre 
ORDER BY Total_Votes DESC;
"""
popular_genres_df = pd.read_sql(query_popular_genres, engine)
fig_genre_votes = px.pie(popular_genres_df,names="Genre",values="Total_Votes",title="Most Popular Genres by Total Voting Counts",
                  color_discrete_sequence=px.colors.sequential.YlGnBu)
st.plotly_chart(fig_genre_votes)

# 8. Duration Extremes: Identify the shortest and longest movies in 2024. -display by table
st.subheader("8. Duration Extremes")
query_duration_short = """SELECT Title, Genre,Duration FROM IMDB_Movies_2024 ORDER BY Duration ASC LIMIT 1;"""
short_movie = pd.read_sql(query_duration_short, engine)
query_duration_long = """SELECT Title, Genre, Duration FROM IMDB_Movies_2024 ORDER BY Duration DESC LIMIT 1;"""
long_movie = pd.read_sql(query_duration_long, engine)
st.write("Shortest Movie:")
st.write(short_movie)
st.write("Longest Movie:")
st.write(long_movie)

#Top-Voted Movies: Find the top 10 movies with the highest voting counts. -display by table
st.subheader("Top 10 Movies with Highest Voted count")
query_top_voted = """SELECT * FROM IMDB_Movies_2024 ORDER BY Voting_counts DESC LIMIT 10;"""
top_voted_df = pd.read_sql(query_top_voted, engine)
st.dataframe(top_voted_df)

#9.Ratings by Genre: Use a heatmap to compare average ratings across genres.
st.subheader("9. Ratings by Genre")
# Query to fetch average ratings by genre
query_ratings_by_genre = """SELECT Genre, AVG(Ratings) AS Avg_Ratings FROM IMDB_Movies_2024
GROUP BY Genre
ORDER BY Avg_Ratings DESC;
"""
ratings_by_genre_df = pd.read_sql(query_ratings_by_genre, engine) # Fetch the data
heatmap_data = ratings_by_genre_df.pivot_table(values='Avg_Ratings', index='Genre', aggfunc='mean')
plt.figure(figsize=(12, 8))  # Adjust figure size for better clarity
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm',cbar_kws={'label': 'Average Ratings'},linewidths=1)
plt.title("Ratings by Genre Heatmap", fontsize=20)
# Display the plot in Streamlit
st.pyplot(plt)

#10.Correlation Analysis: Analyze the relationship between ratings and voting counts using a scatter plot.
st.subheader("10.Correlation Analysis: Ratings vs Voting Counts")
# Query to fetch Ratings and Voting Counts
query_corr = """ SELECT Genre,Ratings, Voting_counts, Title FROM IMDB_Movies_2024
WHERE Ratings IS NOT NULL AND Voting_counts IS NOT NULL
ORDER BY Voting_counts DESC;
"""
corr_df = pd.read_sql(query_corr, engine) # Fetch the data
fig_corr= px.scatter(corr_df,x="Ratings",y="Voting_counts",hover_name="Title", # using plotly scatter chart
    title="Correlation Between Ratings and Voting Counts",
    labels={"Ratings": "IMDB Rating", "Voting_counts": "Number of Votes"},
    color="Genre",  # Color based on Genre
    opacity=0.7,width=2000)
st.plotly_chart(fig_corr) # display the plotly chat in Streamlit

# Close connection to the database
engine.dispose()
