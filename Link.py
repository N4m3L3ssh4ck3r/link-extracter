import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import validators
import time
import random

# Function to make a request and handle errors
def connector(url):
    result = False
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

    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        result = response.text
    except requests.ConnectionError as e:
        raise ConnectionError("\u001b[31;1mCan not connect to server. Check your internet connection\u001b[0m")
    except requests.Timeout as e:
        raise TimeoutError("\u001b[31;1mOOPS!! Timeout Error\u001b[0m")
    except requests.RequestException as e:
        raise AttributeError("\u001b[31;1mError in HTTP request\u001b[0m")
    except KeyboardInterrupt:
        raise KeyboardInterrupt("\u001b[31;1mInterrupted by user\u001b[0m")
    except Exception as e:
        raise RuntimeError("\u001b[31;1m%s\u001b[0m" % (e))
    finally:
        if not result:
            print("\u001b[31;1mBad Internet Connection :(\u001b[0m")
        return result

# Ask the user for the target website
url = input("Please enter the URL of the website you want to extract links from: ")

# Parse the base URL to extract the domain
base_domain = urlparse(url).netloc

# Create a list of different headers to rotate through
headers = [{'User-Agent': 'Mozilla/5.0'}, {'User-Agent': 'Chrome/70.0.3538.77'}, {'User-Agent': 'Safari/537.36'}, {'User-Agent': 'Internet Explorer/11.0'}]

# Create a set to store all the unique links
links = set()

# Set the number of retries and the delay between retries
max_retries = 3
retry_delay = 3  # seconds

# Function to extract links from a given header
def extract_links(header):
    response_text = connector(url)
    if response_text:
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Find all <a> tags in the response
        for link in soup.find_all('a'):
            # Get the href attribute of the <a> tag
            href = link.get('href')
            
            # Check if the link is valid and not empty
            if href and href != "#":
                # Get the full URL by joining with the base URL
                full_url = urljoin(url, href)
                
                            # Check if the full URL is valid and belongs to the same domain
                if validators.url(full_url) and urlparse(full_url).netloc == base_domain:
                    # Append the valid full URL to the set
                    links.add(full_url)

# Create threads for each header
threads = []
for header in headers:
    thread = threading.Thread(target=extract_links, args=(header,))
    threads.append(thread)
    thread.start()
    time.sleep(1)  # Add a small delay between starting threads

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Print a success message
print("All links from the specified domain have been extracted.")

# Ask the user for the file name to save the links to
file_name = input("Please enter the file name to save the links to (include .txt extension): ")

# Open the file in write mode
with open(file_name, 'w') as f:
    # Write each link to a new line in the file
    for link in links:
        f.write(link + "\n")

# Print a success message
print("All links from the specified domain have been extracted and saved to " + file_name + ".")

