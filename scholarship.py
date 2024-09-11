import requests
from bs4 import BeautifulSoup
import json

def scrape_scholarships(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content area (trying different possible selectors)
    main_content = soup.find('div', class_='entry-content') or soup.find('main') or soup.find('article')

    scholarships = []

    if main_content:
        print("Scholarship Information:")
        print("------------------------")
        
        # Find all text elements (paragraphs, list items, headings, etc.)
        text_elements = main_content.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for element in text_elements:
            text = element.get_text().strip()
            if text:  # Only print non-empty lines
                print(text)
                scholarships.append(text)  # Add the text to the list of scholarships

    else:
        print("Could not find the main content area. The website structure might have changed.")
        print("Here's the full page content:")
        print(soup.get_text())

    # Save the scraped data to a JSON file
    if scholarships:
        with open('scholarships.json', 'w') as json_file:
            json.dump(scholarships, json_file, indent=4)
        print("\nScholarship data saved to scholarships.json")
    else:
        print("No scholarship data found.")

# URL of the webpage to scrape
url = "https://sjcetpalai.ac.in/sjcet-palai-scholarships/"

# Run the scraping function
scrape_scholarships(url)
