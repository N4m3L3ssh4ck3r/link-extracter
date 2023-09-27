import requests
from bs4 import BeautifulSoup

# ask the user for the target website
url = input("Please enter the URL of the website you want to extract links from: ")

# create a dictionary of different headers to rotate through
headers = [{'User-Agent': 'Mozilla/5.0'}, {'User-Agent': 'Chrome/70.0.3538.77'}, {'User-Agent': 'Safari/537.36'}, {'User-Agent': 'Internet Explorer/11.0'}]

# create a list to store all the links
links = []

# loop through the headers and make a request to the website
for header in headers:
    response = requests.get(url, headers=header)
    
    # parse the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # find all <a> tags in the response
    for link in soup.find_all('a'):
        # get the href attribute of the <a> tag
        href = link.get('href')
        
        # check if the link is valid and not empty
        if href and href != "#":
            # append the link to the list
            links.append(href)

# remove duplicate links from the list
links = list(set(links))

# ask the user for the file name to save the links to
file_name = input("Please enter the file name to save the links to (include .txt extension): ")

# open the file in write mode
with open(file_name, 'w') as f:
    # write each link to a new line in the file
    for link in links:
        f.write(link + "\n")

# print a success message
print("All links have been extracted and saved to " + file_name + ".")
