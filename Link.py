import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import validators  # Import the validators module to check URL validity

# Ask the user for the target website
url = input("Please enter the URL of the website you want to extract links from: ")

# Create a dictionary of different headers to rotate through
headers = [{'User-Agent': 'Mozilla/5.0'}, {'User-Agent': 'Chrome/70.0.3538.77'}, {'User-Agent': 'Safari/537.36'}, {'User-Agent': 'Internet Explorer/11.0'}]

# Create a set to store all the unique links
links = set()

# Loop through the headers and make a request to the website
for header in headers:
    response = requests.get(url, headers=header)
    
    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags in the response
    for link in soup.find_all('a'):
        # Get the href attribute of the <a> tag
        href = link.get('href')
        
        # Check if the link is valid and not empty
        if href and href != "#":
            # Get the full URL by joining with the base URL
            full_url = urljoin(url, href)
            
            # Check if the full URL is valid
            if validators.url(full_url):
                # Append the valid full URL to the set
                links.add(full_url)

# Ask the user for the file name to save the links to
file_name = input("Please enter the file name to save the links to (include .txt extension): ")

# Open the file in write mode
with open(file_name, 'w') as f:
    # Write each link to a new line in the file
    for link in links:
        f.write(link + "\n")

# Print a success message
print("All links have been extracted and saved to " + file_name + ".")
