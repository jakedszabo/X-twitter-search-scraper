# twitterssearchscraper
This X (formerly known as Twitter) search scraper uses Selenium to extract the content, dates, and views of an X search.

Users require the latest version of Python, a code editor such as Visual Code Studio, and a Windows system. 

To Run:

1. Open a powershell window by holding shift and left-clicking on the desktop.
2. Click "Open PowerShell window here."
3. Install all dependencies by typing pip install in the PowerShell Window followed by the dependency name.
4. Wait for the dependency to install before repeating.
Dependencies:
Selenium
Pandas
Webdriver-manager
5. Open twittersearchscraper.py in a code editor.
6. Replace the term query within the quotes in line 72 with your search query.
7. Change the number of scrolls (times the code will scroll down the X search window to produce more results) to the desired amount by changing the value in line 20 of the code of max_scrolls=5 to the desired value.
8. Save changes
9. Open a Chrome browser window and log in to X.
10. Type python twittersearchscraper.py into the PowerShell window.
11. The code will return the first 3 results in the PowerShell window and save the results to twitter_search_results.csv in whatever folder that twittersearchscraper.py is in.
12. The list will contain many duplicates. Use the remove duplicates function in Excel by typing remove duplicates into the search bar.
13. Save your results to another file before running the code again as it will replace the file each time.
