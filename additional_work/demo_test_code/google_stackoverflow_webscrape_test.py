

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

import requests
from bs4 import BeautifulSoup

# to search
query = "Pytorch CNN Model Issue"
 
for url in search(query, tld="com", num=10, stop=10, pause=2):
    if url.startswith("https://stackoverflow.com/questions/"):
        print(url)
        response = requests.get(url)
        # Check for successful download
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract specific information:
            question_header = soup.find(id="question-header")

            # Getting URL title 
            # There can be multiple elements within the question header, so find the first h1 tag
            title_element = question_header.find('h1')

            # If the h1 tag exists, extract its text content
            if title_element:
                title_text = title_element.text.strip()
                print(title_text)
            else:
                print("H1 title not found")

            # Getting question body now:  s-prose js-post-body
            question_header = soup.find(id="s-prose js-post-body")
            
            # This will find the header for the question body 
        else:
            print(f"Error downloading the webpage: {response.status_code}")

   