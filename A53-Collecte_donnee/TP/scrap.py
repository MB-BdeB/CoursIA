from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

url = "https://www.leboncoin.fr/voitures/offres/"

# Set up Selenium WebDriver
driver = webdriver.Firefox()  # Ensure you have ChromeDriver installed
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Get the page source
html_content = driver.page_source
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Example: Find all 'div' elements containing car listings (adjust based on actual HTML structure)
annonces = soup.find_all('div', class_=lambda c: c and 'styles__item' in c)

# Debug: Print the number of annonces found
print(f"Found {len(annonces)} annonces.")
print(annonces)

data = []
for annonce in annonces:
    # Extract title
    titre_tag = annonce.find('h2', class_=lambda c: c and 'styles__title' in c)
    titre = titre_tag.text.strip() if titre_tag else "N/A"

    # Extract price
    prix_tag = annonce.find('span', class_=lambda c: c and 'styles__price' in c)
    prix = prix_tag.text.strip() if prix_tag else "N/A"

    # Extract year, mileage, fuel type, and transmission
    details_tag = annonce.find_all('span', class_=lambda c: c and 'styles__detail' in c)
    details = [detail.text.strip() for detail in details_tag] if details_tag else ["N/A"] * 4

    # Append extracted data
    data.append([titre, prix] + details)

# Print the extracted data
print(f"Extracted {len(data)} annonces.")
for row in data:
    print(row)

# Save to CSV
with open("extracted_data.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Year", "Mileage", "Fuel Type", "Transmission"])
    writer.writerows(data)

print(f"{len(data)} annonces sauvegardées dans 'extracted_data.csv'")