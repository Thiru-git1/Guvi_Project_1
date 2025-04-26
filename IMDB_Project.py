from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os

# ✅ Initialize the driver
driver = webdriver.Chrome()
# ✅ Dictionary of genre and URL
urls = {
     "fantasy"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=fantasy",
     "Sci-fi"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=sci-fi",
     "history"  :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=history",
     "Animation":"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=animation",
     "family"   :"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=family"
}
# ✅ Folder to save CSVs
output_folder = "D:/imdb_mdb_2024"
os.makedirs(output_folder, exist_ok=True)

def click_load_more():
    try:
        wait = WebDriverWait(driver, 10)
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span')))
        ActionChains(driver).move_to_element(load_more_button).click().perform()
        time.sleep(3)  # Let content load after clicking
        return True
    except Exception as e:
        print("⛔ No more 'Load More' button or error:", {e})
        return False

# ✅ Loop through each genre
for genre_u, url in urls.items():
    driver.get(url)
    time.sleep(5)
    while True:
        if not click_load_more():  # 👈 Keep trying until the button disappears
            print("✅ All movies loaded.")
            break
        else:
             print("➡️ Clicked Load More")
    movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
    print(f"Found {len(movies)}...movies..in {genre_u}....")
    movie_dict = []  # fresh list for every genre

    for idx, movie in enumerate(movies):  
        try:
            title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
            try:
                genre = WebDriverWait(movie, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[1]/div/div/div[2]/button[3]/span"))
                ).text
            except:
                genre = "N/A"            
            try:
                rating = WebDriverWait(movie, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/span/div/span/span[1]"))).text
            except:
                rating = "N/A"
            try:
                voting = WebDriverWait(movie, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/span/div/span/span[2]"))).text
            except:
                voting = "N/A"
            try:
                duration = WebDriverWait(movie, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//div/div/div/div[1]/div[2]/div[2]/span[2]"))).text                
            except:
                duration = "N/A"
                
            title = " ".join(title.split()[1:])
            movie_dict.append([title, genre, rating, voting, duration])
        except Exception as e:
            print(f"❌ Error in movie {idx}: {e}")
            continue
    # ✅ Save to CSV
    mov_col = ['Title', 'Genre', 'Ratings', 'Voting_counts', 'Duration']
    df = pd.DataFrame(movie_dict, columns=mov_col)
    print(df)
   
    file_path = f"{output_folder}/{genre_u}.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Saved {len(df)} movies to {file_path}\n")
#✅ Close driver
driver.quit()