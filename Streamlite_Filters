import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --- SQLAlchemy Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/imdb_2024')
# --- Streamlit App ---

#1. Filter movies based on run-time
#--------------------------------------
st.title("IMDb 2024 Movie Analysis Dashboard with Filters")

#1: Filters based on movie run-time
#------------------------------------
st.sidebar.header("1. Filters based on Duration")
dur_side_filter = st.sidebar.selectbox("Select Duration Filter:", options=["< 2 hrs", "2 - 3 hrs", "> 3 hrs"])
# if condition for duration_time------
if dur_side_filter == "< 2 hrs":
    dur_mins = "Duration < 120"
elif dur_side_filter == "2 - 3 hrs":
    dur_mins = "Duration BETWEEN 120 AND 180"
else:
    dur_mins = "Duration > 180"
# Final SQL Query----------------------------------------
query = f"""SELECT * FROM IMDB_Movies_2024
WHERE {dur_mins}
ORDER BY Duration asc;"""
#-----------------------xxx---------------------------------
st.subheader("1. Display Movies based on Movie Run-time")
# Fetch Data and display in main page
duration_df = pd.read_sql(query, engine)
st.dataframe(duration_df)

#2: Filter movies based on IMDb ratings-----------------
#-------------------------------------------------------
st.sidebar.header("2. Filter based on IMDB Ratings")
ratings_side_filter = st.sidebar.slider("Select IMDB Ratings:", min_value=0.0, max_value=10.0, step=0.1, value=8.0)
# SQL Query--------------------------------------------------
query = f"""SELECT * FROM IMDB_Movies_2024
WHERE Ratings <={ratings_side_filter}
ORDER BY Ratings DESC;"""
st.subheader(f"2. Display movie based on IMDB Ratings >= {ratings_side_filter}")
# Display Movie list in main page based on the SQL query-----
ratings_df = pd.read_sql(query,engine)
st.dataframe(ratings_df)

#3.Filter movies based on Voting counts-----------------
#-------------------------------------------------------
st.sidebar.header("3.Filter based on Voting counts")
voting_side_filter = st.sidebar.slider("Select Voting count:", min_value=1, max_value=100000, step=1)
# SQL Query---------------------------------------------
query = f"""SELECT * FROM IMDB_Movies_2024
WHERE Voting_counts >={voting_side_filter}
ORDER BY Voting_counts asc;"""
st.subheader(f"2.Display movie based on Voting counts>= {voting_side_filter}")
# Display Movie list in main page based on the SQL query----
voting_count_df=pd.read_sql(query,engine)
st.dataframe(voting_count_df)

#4. Genre: Filter movies within specific genres (e.g., Action, Drama).
#--------------------------------------------------------------------
# Sidebar Header
st.sidebar.header("4. Filter Movies Based on Genre")
# Fetch all genres
genre_query = """SELECT DISTINCT Genre FROM IMDB_Movies_2024""" #Get the unique Genre from SQL DB
genre_df = pd.read_sql(genre_query, engine) # read and store the data from SQL and move into Panda dataframe.
# Split and clean genres
all_genres = set(g.strip() for genre in genre_df['Genre'] for g in genre.split(","))
# Sorted list for UI
genres_df = sorted(list(all_genres))
fil_genre = st.sidebar.multiselect("Select Genre:",options=genres_df,default=[])
# If genres are selected
if fil_genre:
    # Prepare the genre conditions
    genre_conditions = " OR ".join([f"Genre LIKE '%{g}%'" for g in fil_genre])
    # Final Query
    gen_cond_query = f"""SELECT * FROM IMDB_Movies_2024 
    WHERE {genre_conditions}
    ORDER BY Genre asc;
    """
    # Fetch and display
    genre_fil_df = pd.read_sql(gen_cond_query, engine)
    st.subheader("4. Movies Based on Selected Genre")
    st.dataframe(genre_fil_df)
else:
    st.warning("Please select at least one genre to see the results.")

#5. Combine filtering options so users can apply multiple filters simultaneously for customized insights.

st.sidebar.header("5. Combined Filters ")
# Fetch all genres (splitting them like before)
genre_query = """SELECT DISTINCT Genre FROM IMDB_Movies_2024"""
genre_df = pd.read_sql(genre_query, engine)
# Split and clean genres
all_genres = set(g.strip() for genre in genre_df['Genre'] for g in genre.split(","))
# Sorted list for UI
genres_list = sorted(list(all_genres))
# Sidebar filters
selected_genres = st.sidebar.multiselect("Select Genre(s):", options=genres_list, default=[],key="genre_multiselect" )
min_rating = st.sidebar.slider("Minimum Rating:", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
duration_range = st.sidebar.slider("Duration Range (minutes):", min_value=0, max_value=300, value=(120, 180))
min_votes = st.sidebar.number_input("Minimum Votes:", min_value=0, value=50000, step=1000)
# Building the SQL Query dynamically
filters = []
# Genre filter
if selected_genres:
    genre_condition = " OR ".join([f"Genre LIKE '%{g}%'" for g in selected_genres])
    filters.append(f"({genre_condition})")
# Rating filter
filters.append(f"Ratings >= {min_rating}")
# Duration filter
filters.append(f"Duration BETWEEN {duration_range[0]} AND {duration_range[1]}")
# Votes filter
filters.append(f"Voting_counts >= {min_votes}")
# Combine all filters with AND
where_clause = " AND ".join(filters)

# Valid sort columns that match the columns with SQL DB
sort_columns = ["Title", "Genre", "Ratings", "Voting counts", "Duration"]
select_sort_column = st.sidebar.selectbox("Sort By:", sort_columns, index=2)  # Example: Ratings
sort_order = st.sidebar.radio("Sort Order:", ["Descending", "Ascending"])
order_sql = "DESC" if sort_order == "Descending" else "ASC"

# Final SQL Query
query_comb = f"""SELECT *FROM IMDB_Movies_2024  
WHERE {where_clause}
ORDER BY {select_sort_column} {order_sql};
"""

display_movies = pd.read_sql(query_comb, engine) # Fetch and display
# Display Table
st.subheader("5. Display filtered Movies")
st.dataframe(display_movies)

# --- Close SQL Connection ---
engine.dispose()
