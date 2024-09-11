import requests
from bs4 import BeautifulSoup

def scrape_curriculum(url):
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

    if main_content:
        print("Curriculum Information:")
        print("------------------------")
        
        # Find all headings and their subsequent content
        headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            print(f"\n{heading.text.strip()}")
            
            # Find all siblings until the next heading
            next_element = heading.next_sibling
            while next_element and not next_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if next_element.name in ['p', 'ul', 'ol']:
                    print(next_element.text.strip())
                next_element = next_element.next_sibling

        # Check for any tables in the content
        tables = main_content.find_all('table')
        for table in tables:
            print("\nTable found:")
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                row_data = [cell.text.strip() for cell in cells]
                print('\t'.join(row_data))

    else:
        print("Could not find the main content area. The website structure might have changed.")
        print("Here's the full page content:")
        print(soup.get_text())

    print("\nNote: If the output is not as expected, the website structure may have changed significantly.")

# URL of the webpage to scrape
url = "https://sjcetpalai.ac.in/curriculum/"

# Run the scraping function
scrape_curriculum(url)