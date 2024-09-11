import requests
from bs4 import BeautifulSoup

def scrape_btech_admission(url):
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
        print("B.Tech Admission Information:")
        print("-----------------------------")
        
        # Find the section with admission criteria
        admission_section = main_content.find('h3', string='Admission Criteria for B.Tech Programme')
        
        if admission_section:
            # Extract and print the admission criteria
            criteria_list = admission_section.find_next('ul')
            if criteria_list:
                for item in criteria_list.find_all('li'):
                    print(f"- {item.text.strip()}")
            else:
                print("Admission criteria list not found.")
        else:
            print("Admission criteria section not found.")
        
        # Find and print any additional relevant information
        additional_info = main_content.find_all(['p', 'h3', 'h4'])
        for info in additional_info:
            if any(keyword in info.text.lower() for keyword in ['eligibility', 'qualification', 'admission']):
                print(f"\n{info.name.upper()}: {info.text.strip()}")

    else:
        print("Could not find the main content area. The website structure might have changed.")
        print("Here's the full page content:")
        print(soup.get_text())

    print("\nNote: If the output is not as expected, the website structure may have changed significantly.")

# URL of the webpage to scrape
url = "https://sjcetpalai.ac.in/b-tech-admission/"

# Run the scraping function
scrape_btech_admission(url)