import requests
from bs4 import BeautifulSoup
import json
import os
import time

# Google Scholar profile URL (with pagination)
url = "https://scholar.google.com/citations?user=o7u_E8wAAAAJ&cstart={}&pagesize=100"

# User-Agent header to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_publications(url):
    publications = []
    start = 0
    invalid_pages = 0
    max_invalid_pages = 5  # Stop after encountering 5 pages with only invalid data
    
    while True:
        paginated_url = url.format(start)
        response = requests.get(paginated_url, headers=headers)

        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
            continue  # Retry the current page after waiting
        
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        publication_rows = soup.select('.gsc_a_tr')
        
        if not publication_rows:
            print(f"No more publications found. Stopping at page {start // 100 + 1}.")
            break  # No more publications found, exit the loop
        
        print(f"Number of publication rows found on page {start // 100 + 1}: {len(publication_rows)}")
        valid_publications_found = False
        
        for item in publication_rows:
            title_tag = item.select_one('.gsc_a_at')
            title = title_tag.text if title_tag else None
            authors = item.select_one('.gs_gray').text if item.select_one('.gs_gray') else None
            year_tag = item.select_one('.gsc_a_y')
            year = year_tag.text if year_tag else None
            journal = item.select('.gs_gray')[-1].text if len(item.select('.gs_gray')) > 1 else None
            link = "https://scholar.google.com" + title_tag['href'] if title_tag else None

            if not title or not authors or not year or not journal:
                print("Incomplete data found, skipping this entry.")
                continue  # Skip this entry if any essential information is missing

            # Categorize as either conference or journal based on the presence of certain keywords
            category = "conference" if "conference" in journal.lower() or "proceedings" in journal.lower() else "journal"

            # Only include publications from 2015 onwards
            if int(year.strip()) < 2015:
                continue

            publication = {
                'title': title,
                'authors': authors,
                'year': int(year.strip()) if year.strip().isdigit() else 0,
                'journal': journal,
                'link': link,
                'category': category
            }
            print(f"Processed publication: {publication}")
            publications.append(publication)
            valid_publications_found = True

        if not valid_publications_found:
            invalid_pages += 1
            print(f"Invalid data found on page {start // 100 + 1}. Incrementing invalid page counter to {invalid_pages}.")
            if invalid_pages >= max_invalid_pages:
                print("Max invalid pages threshold reached. Stopping further requests.")
                break
        else:
            invalid_pages = 0  # Reset the counter if we find valid data

        # Move to the next page
        start += 100

    # Sort publications by year in descending order (latest first)
    publications.sort(key=lambda x: x['year'], reverse=True)
    
    print(f"Total publications fetched: {len(publications)}")
    
    return publications

# Get the publications data
publications = get_publications(url)

# Ensure the "publication" directory exists
os.makedirs('publication', exist_ok=True)

# Save the publication data to a JSON file in the "publication" directory
with open('publication/publications.json', 'w') as f:
    json.dump(publications, f, indent=4)

print("Data saved to publication/publications.json")