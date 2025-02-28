import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# attaches to existing chrome
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Scrapes twitter of content date and views
def scrape_twitter(query, max_scrolls=5):
    driver.get(f"https://twitter.com/search?q={query}&f=live")
    time.sleep(5)  # Wait for page to load

    tweets = []  # List to store all tweets


    for _ in range(max_scrolls):
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
                    views = views_element.get_attribute("aria-label").split()[0]  # Extract number only
                except:
                    views = "N/A" 

    
            
                # Stores tweet in list
                tweets.append({"Content": content, "Date": date, "views": views})

            except Exception as e:
                print(f"Error extracting tweet: {e}")  # Catch extraction errors

        # Scrolls down to load tweets
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Wait for new tweets to load
        except Exception as e:
            print(f"Error while scrolling: {e}")  # Handle scrolling errors

    # Convert tweets to Data Frame
    df = pd.DataFrame(tweets)
    

    # Saves to CSV
    df.to_csv("twitter_search_results.csv", index=False)
    print("✅ Scraping complete. Data saved to 'twitter_search_results.csv'.")

    return tweets  # Return list of tweets

# Runs scraper
tweets = scrape_twitter("query")

# Prints first 3 tweets for verification of accuracy of output
print(" First 3 tweets")
for tweet in tweets[:3]:
    print(tweet)
