from selenium.webdriver.support.ui import WebDriverWait   #wait fot the elements to appear to become clickable before interacting with dynamic webpage like IMDB
from selenium.webdriver.support import expected_conditions as EC  #same to wait 
from selenium import webdriver               #Open the browser                     
from selenium.webdriver.common.by import By  # By is used to find the specific elements like CSS, XPATH, etc.. 
from selenium.webdriver.common.action_chains import ActionChains # To do actions like Hoving and dynamically clicking
import time  # time used to add delayes using sleep
import pandas as pd  # pandas to create datatables (df) and save in CSV format
import os  # used to manage folder and file path

# Initialize the driver
driver = webdriver.Chrome()  
#Dictionary of genre and URL - Keys are Genre and Values are url..
urls = {
     "fantasy"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=fantasy",
     "Sci-fi"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=sci-fi",
     "history"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=history",
     "Animation":"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=animation",
     "family"   :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=family"
    }
#Folder to save CSVs
output_folder = "D:/imdb_mdb_2024" # Folder path to save all CSVs in the folder
os.makedirs(output_folder, exist_ok=True)  #checks if the folder already exists, avoids if any error.

def click_load_more(): # Click_load_more function is defined to click load more button if its need to load more pages.
    try:
        wait = WebDriverWait(driver, 10) 
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span')))
        ActionChains(driver).move_to_element(load_more_button).click().perform()
        time.sleep(3)  # Let content load after clicking
        return True
    except Exception as e:
        print("No more 'Load More' button or 'error':", {e})
        return False

#Loop through each genre
for genre_u, url in urls.items():           # loop thorugh Key and Values in Url items
    driver.get(url)                         # opens the IMDB broswer to loop thorugh the items in url
    time.sleep(5)                           # wait 5 secs to load the page completely
    while True:                             # returns true when all the movies loaded in the page - until break it runs
        if not click_load_more():           # if no button, stop looping
            print("All movies loaded.")     # and print all movies are loaded
            break                           # exit loop once all movies are loaded
        else:                               # if button is clicked, continue to loop
             print("Click to Load More")    # and print still more to click
# after the exit from False from the loop..
    movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item") # declare movie variable to loop through each container
    print(f"Found {len(movies)}...movies..in {genre_u}....") # message to say movie count in the page and under Genre
    movie_dict = []     #create a list to store the movie details
# create a for loop to loop through the items in the container
    for idx, movie in enumerate(movies):  # idx - index, movie is a variable , enumerate is in-built for loop function gives index and value while looping
        try: 
            title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text #Extract the Movie Title 
            try:
                genre = WebDriverWait(movie, 2).until( # Extract the Genre details 
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[1]/div/div/div[2]/button[3]/span"))
                ).text 
            except:
                genre = None            
            try:
                rating = WebDriverWait(movie, 3).until( # Extract the rating details 
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/span/div/span/span[1]"))).text
            except:
                rating = None
            try:
                voting = WebDriverWait(movie, 3).until( #Extract the Voting details
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/span/div/span/span[2]"))).text
            except:
                voting = None
            try:
                duration = WebDriverWait(movie, 3).until( # Extract the duration details
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/div[2]/span[2]"))).text                
            except:
                duration = None
                
            title = " ".join(title.split()[1:])  # split only the movie title
            movie_dict.append([title, genre, rating, voting, duration]) # add the extracted movie details to the list
        except Exception as e: # if any of the during movie scraping, that catches the exception
            print(f"Error in movie {idx}: {e}") 
            continue
    #Save to CSV
    mov_col = ['Title', 'Genre', 'Ratings', 'Voting_counts', 'Duration'] # column name matches with list appended
    df = pd.DataFrame(movie_dict, columns=mov_col) # create df from movie_dict
    print(df)                                      # print the scraped movie data 
    file_path = f"{output_folder}/{genre_u}.csv"   # output_folder- folder where need to create particular genre.csv
    df.to_csv(file_path, index=False)              # csv() - saves df into CSV format
    print(f"Saved {len(df)} movies to {file_path}\n") # message to print total no.of movies saved in that particular csv
#Close driver
driver.quit()
