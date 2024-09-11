import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://sjcetpalai.ac.in/'

def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
        
    except requests.exceptions.HTTPError as err:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None

def scrape_fee_structure():
    print("\n### Fee Structure ###")
    fee_url = base_url + 'fee-structure/' 
    soup = scrape_page(fee_url)
    
    fee_data = []  # To store the fee structure data
    
    if soup:
        fee_table = soup.find('table')
        if fee_table:
            rows = fee_table.find_all('tr')
            headers = [th.text.strip() for th in rows[0].find_all('th')]  # Extract headers from the first row
            
            # Extract rows data
            for row in rows[1:]:  # Skipping the header row
                cells = row.find_all('td')
                row_data = {headers[i]: cell.text.strip() for i, cell in enumerate(cells)}
                fee_data.append(row_data)
        else:
            print("Fee structure table not found.")
    else:
        print("Failed to retrieve the fee structure page.")
    
    return fee_data

# Save the scraped data to a JSON file
def save_to_json(data, filename='fee_structure.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been saved to {filename}")

# Main
def main():
    fee_data = scrape_fee_structure()
    if fee_data:
        save_to_json(fee_data)  # Save the fee structure data to a JSON file

if __name__ == "__main__":
    main()
