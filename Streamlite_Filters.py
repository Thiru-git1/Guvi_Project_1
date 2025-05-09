import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --- SQLAlchemy Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/imdb_2024')
# --- Streamlit App ---

#Page Name change
st.set_page_config(page_title="IMDB 2024 Streamlit Filters", layout="wide")
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
query = f"""SELECT * FROM IMDB_Movies_2024 WHERE {dur_mins} ORDER BY Duration asc;"""
st.subheader("1. Display Movies based on Movie Run-time")
duration_df = pd.read_sql(query, engine) # Fetch Data from SQL and returns as a DF
st.dataframe(duration_df) #display that Dataframe as an interactive table 

#2: Filter movies based on IMDb ratings-----------------
st.sidebar.header("2. Filter based on IMDB Ratings")
ratings_side_filter = st.sidebar.slider("Select IMDB Ratings:", min_value=0.0, max_value=10.0, step=0.1, value=8.0)
query = f"""SELECT * FROM IMDB_Movies_2024 WHERE Ratings >={ratings_side_filter}
ORDER BY Ratings DESC;"""
st.subheader(f"2. Display movie based on IMDB Ratings >= {ratings_side_filter}")
ratings_df = pd.read_sql(query,engine)
st.dataframe(ratings_df)

#3.Filter movies based on Voting counts-----------------
st.sidebar.header("3.Filter based on Voting counts")
voting_side_filter = st.sidebar.slider("Select Voting count:", min_value=1, max_value=100000, step=1)
query = f"""SELECT * FROM IMDB_Movies_2024
WHERE Voting_counts >={voting_side_filter}
ORDER BY Voting_counts asc;"""
st.subheader(f"3.Display movie based on Voting counts>= {voting_side_filter}")
voting_count_df=pd.read_sql(query,engine)
st.dataframe(voting_count_df)

#4. Genre: Filter movies within specific genres (e.g., Action, Drama).
st.sidebar.header("4. Filter Movies Based on Genre")
genre_query = """SELECT DISTINCT Genre FROM IMDB_Movies_2024""" #Get the unique Genre from SQL DB
genre_df = pd.read_sql(genre_query, engine) # read and store the data from SQL and move into Panda dataframe.
all_genres = set(g.strip() for genre in genre_df['Genre'] for g in genre.split(","))  # Split and clean genres
genres_df = sorted(list(all_genres)) # Sorted list for UI
fil_genre = st.sidebar.multiselect("Select Genre:",options=genres_df,default=[])
if fil_genre: # If genres are selected
    genre_conditions = " OR ".join([f"Genre LIKE '%{g}%'" for g in fil_genre]) # Prepare the genre conditions to make to one genre
    gen_cond_query = f"""SELECT * FROM IMDB_Movies_2024 WHERE {genre_conditions} ORDER BY Genre asc;"""
    genre_fil_df = pd.read_sql(gen_cond_query, engine)     # Fetch from SQL and store as a dataframe and display
    st.subheader("4. Movies Based on Selected Genre")
    st.dataframe(genre_fil_df)
else:
    st.warning("Please select at least one genre to see the results.")

#5. Combine filtering options so users can apply multiple filters simultaneously for customized insights.
st.sidebar.header("5. Combined Filters ")
genre_query = """SELECT DISTINCT Genre FROM IMDB_Movies_2024""" # select the unique Genre and load into dataframe
genre_df = pd.read_sql(genre_query, engine)
all_genres = set(g.strip() for genre in genre_df['Genre'] for g in genre.split(","))# Split and clean genres
genres_list = sorted(list(all_genres)) # Sorted list in streamlit
# Sidebar Interactive filters 
genres_select = st.sidebar.multiselect("Select Genre:", options=genres_list, default=[],key="genre_multiselect" )
rating_cond = st.sidebar.slider("Select Rating:", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
duration_cond = st.sidebar.slider("Select Duration (mins):", min_value=0, max_value=300, value=(60, 120))
voting_cond = st.sidebar.slider("Select Voting count:", min_value=1, max_value=100000, value=400, step=100)
# Building the SQL Query dynamically
filters = [] #create a list for Filter to append the conditions 
if genres_select:
    genre_unique = " OR ".join([f"Genre LIKE '%{g}%'" for g in genres_select])
    filters.append(f"({genre_unique})")
filters.append(f"Ratings >= {rating_cond}")
filters.append(f"Duration BETWEEN {duration_cond[0]} AND {duration_cond[1]}")# Duration filter
filters.append(f"Voting_counts >= {voting_cond}") # Votes filter
where_filter = " AND ".join(filters) # Combine all filters with AND
query_comb = f"""SELECT *FROM IMDB_Movies_2024  
WHERE {where_filter}
"""
display_movies = pd.read_sql(query_comb, engine) # Fetch and display
st.subheader("5. Combined filtered display")
st.dataframe(display_movies) # Display dataframe Table using Interactive display

# --- Close SQL Connection ---
engine.dispose()
