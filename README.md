Skills      - Selenium, Python, Pandas, Streamlit, SQL, Data Cleaning, Data Analysis, Visualization, and Interactive Filter Applications.
Domain Name - Entertainment / Data Analytics

Problem Statement:
-----------------
This project focuses on extracting and analyzing movie data from IMDb for the year 2024. The task involves scraping data such as movie names, genres, ratings, voting counts, and durations from IMDb's 2024 movie list using Selenium. The data will then be organized genre-wise, saved as individual CSV files, and combined into a single dataset stored in an SQL database. Finally, the project will provide interactive visualizations and filtering functionality using Streamlit to answer key questions and allow users to customize their exploration of the dataset.

Business Use Cases:
------------------
1.	Top-Rated Movies: Identify the top 10 movies with the highest ratings and voting counts.
2.	Genre Analysis: Explore the distribution of genres in the 2024 movie list.
3.	Duration Insights: Analyze the average duration of movies across genres.
4.	Voting Patterns: Discover genres with the highest average voting counts.
5.	Popular Genres: Identify the genres that dominate IMDb's 2024 list based on movie count.
6.	Rating Distribution: Analyze the distribution of ratings across all movies.
7.	Genre vs. Ratings: Compare the average ratings for each genre.
8.	Duration Extremes: Identify the shortest and longest movies in 2024.
9.	Top-Voted Movies: Find the top 10 movies with the highest voting counts.
10.	Interactive Filtering: Allow users to filter movies by ratings, duration, votes, and genre and view the results in a tabular DataFrame format.

Business Use Cases:
-------------------
1.	Top-Rated Movies: Identify the top 10 movies with the highest ratings and voting counts.
2.	Genre Analysis: Explore the distribution of genres in the 2024 movie list.
3.	Duration Insights: Analyze the average duration of movies across genres.
4.	Voting Patterns: Discover genres with the highest average voting counts.
5.	Popular Genres: Identify the genres that dominate IMDb's 2024 list based on movie count.
6.	Rating Distribution: Analyze the distribution of ratings across all movies.
7.	Genre vs. Ratings: Compare the average ratings for each genre.
8.	Duration Extremes: Identify the shortest and longest movies in 2024.
9.	Top-Voted Movies: Find the top 10 movies with the highest voting counts.
10.	Interactive Filtering: Allow users to filter movies by ratings, duration, votes, and genre and view the results in a tabular DataFrame format.

Approach:
--------
1. Data Scraping and Storage
●	Data Source: IMDb 2024 Movies page (link).
●	Scraping Method: Use Selenium to extract the following fields:
○	Movie Name
○	Genre
○	Ratings
○	Voting Counts
○	Duration
●	Genre-wise Storage: Save extracted data as individual CSV files for each genre.
●	Combine Data: Merge all genre-wise CSVs into a single DataFrame.
●	SQL Storage: Store the merged dataset into an SQL database for querying and future analysis.

Data Analysis, Visualization, and Filtration
----------------------------------------------
Interactive Visualizations
Using Python and Streamlit, create dynamic visualizations for:
1.	Top 10 Movies by Rating and Voting Counts: Identify movies with the highest ratings and significant voting engagement.
2.	Genre Distribution: Plot the count of movies for each genre in a bar chart.
3.	Average Duration by Genre: Show the average movie duration per genre in a horizontal bar chart.
4.	Voting Trends by Genre: Visualize average voting counts across different genres.
5.	Rating Distribution: Display a histogram or boxplot of movie ratings.
6.	Genre-Based Rating Leaders: Highlight the top-rated movie for each genre in a table.
7.	Most Popular Genres by Voting: Identify genres with the highest total voting counts in a pie chart.
8.	Duration Extremes: Use a table or card display to show the shortest and longest movies.
9.	Ratings by Genre: Use a heatmap to compare average ratings across genres.
10.	Correlation Analysis: Analyze the relationship between ratings and voting counts using a scatter plot.

Interactive Filtering Functionality
●	Allow users to filter the dataset based on the following criteria:
○	Duration (Hrs): Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs).
○	Ratings: Filter movies based on IMDb ratings (e.g., > 8.0).
○	Voting Counts: Filter based on the number of votes received (e.g., > 10,000 votes).
○	Genre: Filter movies within specific genres (e.g., Action, Drama).
●	Display the filtered results in a dynamic DataFrame within the Streamlit app.
●	Combine filtering options so users can apply multiple filters simultaneously for customized insights.

