import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = "https://sjcetpalai.ac.in/residential-facilities/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the main content area (trying different possible selectors)
main_content = soup.find('div', class_='entry-content') or soup.find('main') or soup.find('article')

# Dictionary to store the scraped data
residential_facilities_data = {}

if main_content:
    print("Residential Facilities Information:")
    print("-----------------------------------")

    # Initialize a list to store the text elements
    content_list = []

    # Find all text elements (paragraphs, list items, headings, etc.)
    text_elements = main_content.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for element in text_elements:
        text = element.get_text().strip()
        if text:  # Only store non-empty lines
            content_list.append(text)

    # Store the list of text elements in the dictionary
    residential_facilities_data["residential_facilities"] = content_list

else:
    print("Could not find the main content area. The website structure might have changed.")
    residential_facilities_data["error"] = "Main content area not found."

# Save the scraped data to a JSON file
json_filename = 'residential_facilities.json'
with open(json_filename, 'w') as json_file:
    json.dump(residential_facilities_data, json_file, indent=4)

print(f"\nData saved to {json_filename}")
