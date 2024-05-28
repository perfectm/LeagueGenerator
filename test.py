from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Load the page
driver.get("https://www.mlb.com/players")

# Wait for dynamic content to load (adjust sleep time as needed)
time.sleep(5)

# Get the page source after content is loaded
html_content = driver.page_source

# Close the driver
driver.quit()

# Now you can use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')
# Add your parsing logic here based on the loaded HTML
print(soup)
# Example: Print the page title
#print("Page Title:", soup.title.text.strip())
