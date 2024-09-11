import requests
from bs4 import BeautifulSoup

base_url = 'https://sjcetpalai.ac.in/'

def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.HTTPError as err:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None

def extract_table(soup, table_id):
    fee_table = soup.find('table', {'id': table_id})
    if fee_table:
        rows = fee_table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            print('\t'.join(row_data))
    else:
        print(f"Table with id {table_id} not found.")

def scrape_fee_structure():
    print("\n### Residential Fee Structure ###")
    fee_url = base_url + 'fee-structure/' 
    soup = scrape_page(fee_url)
    if soup:
        # Replace 'tablepress-1' with the actual ID of the residential fee table if known
        extract_table(soup, 'tablepress-1')  # Example ID, replace with actual one

# Main
def main():
    scrape_fee_structure()
    # Add more scraping functions as needed

if _name_ == '_main_':
    main()