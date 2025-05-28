import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# attaches to open chrome
chrome_options = Options()
path = r"C:\Users\USER\AppData\Local\Google\Chrome\User Data"
chrome_options.add_argument(f"--user-data-dir={path}")
chrome_options.add_argument(r'--profile-directory=Default')
chromedriver_path = r"C:\Users\USER\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = webdriver.ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)






# Scrapes twitter of content date and views
def scrape_twitter(query, max_scrolls=2000):
    driver.get(f"https://twitter.com/search?q={query}&f=live")
    time.sleep(5)  # Wait for page to load

    tweets = []  # List to store all tweets

    try:
        for _ in range(max_scrolls):
            time.sleep(1)
            tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article")  # Select tweet articles

            for tweet in tweet_elements:
                try:
                    # Tweet content
                    content = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
                    
                    # Tweet date
                    date = tweet.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")

                    try:
                        views_element = WebDriverWait(tweet, 1).until(
                        EC.presence_of_element_located((By.XPATH, ".//a[contains(@aria-label, 'views')]"))
                        )
                        views_text = views_element.get_attribute("aria-label")  # Example: "1,234 views"
                        views = views_text.split()[0]  # Extract only the number
                    except:
                        views = "N/A"
                    try:
                        # Find the likes element
                        likes_element = WebDriverWait(tweet, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label][contains(@aria-label, 'like')]"))
                        )
                        likes_text = likes_element.get_attribute("aria-label")
                        
                        # Extract the number from "X Likes"
                        likes_count = int(likes_text.split()[0].replace(",", ""))
                    except :
                        likes_count = "N/A"
                    try:
                        username = tweet.find_element(By.CSS_SELECTOR, "a[href*='/']").get_attribute("href")
                        username = username.split("/")[-1]  # Extract username from URL
                    except:
                        username = "N/A"
 

        
                
                    # Stores tweet in list
                    tweets.append({"Content": content, "Date": date, "views": views, "usernames": username})

                except Exception as e:
                    print(f"Error extracting tweet: {e}")  # Catch extraction errors

            # Scrolls down to load tweets
            try:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                time.sleep(2)  # Wait for new tweets to load
            except Exception as e:
                print(f"Error while scrolling: {e}")  # Handle scrolling errors
    except Exception as e:
                print(f"Browser closed prematurely: {e}")  # Handle scrolling errors
    finally:

        # Convert tweets to Data Frame
        df = pd.DataFrame(tweets)
    

        # Saves to CSV
        df.to_csv("twitter_search_results.csv", index=False)
        print("Scraping complete. Data saved to 'twitter_search_results.csv'.")

        return tweets  # Return list of tweets

# Runs scraper
tweets = scrape_twitter("search terms")

# Prints first 3 tweets for verification of accuracy of output
print(" First 3 tweets")
for tweet in tweets[:3]:
    print(tweet)
