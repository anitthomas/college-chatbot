import requests
from bs4 import BeautifulSoup

def scrape_placement_opportunities(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content area
    main_content = soup.find('div', class_='entry-content')

    if main_content:
        print("SJCET Palai Placement Opportunities:")
        print("------------------------------------")
        
        # Extract and print headings and their content
        headings = main_content.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            print(f"\n{heading.text.strip()}")
            next_element = heading.next_sibling
            while next_element and next_element.name not in ['h2', 'h3', 'h4']:
                if next_element.name in ['p', 'ul', 'ol']:
                    print(next_element.text.strip())
                next_element = next_element.next_sibling

        # Look for any tables (often used for statistics)
        tables = main_content.find_all('table')
        for table in tables:
            print("\nTable Information:")
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                print(' | '.join(cell.text.strip() for cell in cells))

        # Look for lists of companies
        company_lists = main_content.find_all(['ul', 'ol'])
        for list_item in company_lists:
            if any('compan' in li.text.lower() for li in list_item.find_all('li')):
                print("\nCompanies mentioned:")
                for li in list_item.find_all('li'):
                    print(f"- {li.text.strip()}")

    else:
        print("Could not find the main content area. The website structure might have changed.")
        print("Here's a summary of the page content:")
        print(soup.get_text())

    print("\nNote: If the output is not as expected, the website structure may have changed significantly.")

# URL of the webpage to scrape
url = "https://sjcetpalai.ac.in/sjcet-palai-placement/"

# Run the scraping function
scrape_placement_opportunities(url)