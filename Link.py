import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import validators
import time
import random

# User agents list
user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        # Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]

# Function to initialize the WebDriver and visit the URL with a random user agent
def initialize_driver(url):
    options = Options()
    options.add_argument("--headless")  # Run headless for performance
    options.add_argument(f"user-agent={random.choice(user_agent_list)}")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

# Function to make a request and handle errors using Selenium WebDriver
def connector_selenium(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        response = driver.page_source
        return response
    except Exception as e:
        raise RuntimeError("\u001b[31;1m%s\u001b[0m" % (e))

# Function to extract links from the page using Selenium
def extract_links_selenium(url, driver, visible_links, hidden_links):
    response_text = connector_selenium(url, driver)
    if response_text:
        soup = BeautifulSoup(response_text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href != "#":
                full_url = urljoin(url, href)
                if validators.url(full_url) and urlparse(full_url).netloc == base_domain:
                    visible_links.add(full_url)
                else:
                    hidden_links.add(full_url)

# Ask the user for the target website
url = input("Please enter the URL of the website you want to extract links from: ")

# Parse the base URL to extract the domain
base_domain = urlparse(url).netloc

# Create sets to store all links, visible links, and hidden links
all_links = set()
visible_links = set()
hidden_links = set()

# Initialize the WebDriver
driver = initialize_driver(url)

# Create threads for link extraction
threads = []
for _ in range(5):  # You can adjust the number of threads as needed
    thread = threading.Thread(target=extract_links_selenium, args=(url, driver, visible_links, hidden_links))
    threads.append(thread)
    thread.start()
    time.sleep(1)  # Add a small delay between starting threads

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Combine all links into one set
all_links.update(visible_links)
all_links.update(hidden_links)

# Print the summary
print(f"Total links: {len(all_links)}")
print(f"Visible links: {len(visible_links)}")
print(f"Hidden links: {len(hidden_links)}")

# Print a success message
print("All links from the specified domain have been extracted.")

# Ask the user for the file name to save the links to
file_name = input("Please enter the file name to save the links to (include .txt extension): ")

# Open the file in write mode
with open(file_name, 'w') as f:
    # Write each link to a new line in the file
    for link in all_links:
        f.write(link + "\n")

# Close the WebDriver
driver.quit()

# Print a success message
print(f"All links from the specified domain have been extracted and saved to {file_name}.")
