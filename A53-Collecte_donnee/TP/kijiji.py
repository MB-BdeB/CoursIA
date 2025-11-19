from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
from pymongo import MongoClient

# Function to remove emojis
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "\U00002B00-\U00002BFF"  # arrows
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Function to extract the year from the title
def extract_year(title):
    match = re.search(r"\b(19|20)\d{2}\b", title)  # Matches years like 1990-2099
    return match.group(0) if match else "Unknown"

# Function to write data to CSV with semicolon separator
def write_to_csv(data, output_file):
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Year", "Title", "Price"])  # Header row
        writer.writerows(data)

# Initialisation
options = Options()
options.add_argument("--headless")
service = Service("C:/Users/bouma12/VSCode_WorkSpace/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://www.kijiji.ca/b-autos-et-camions/ville-de-montreal"
page_urls = []
for i in range(1, 25):
    page_urls.append(f"{base_url}/page-{i}/c174l1700281")  # ~1000 lignes

data = []

for idx, url in enumerate(page_urls):
    print(f"\n Page {idx + 1} : {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="listing-card"]'))
        )
    except:
        print(" Annonces non détectées sur cette page.")
        continue

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    annonces = soup.select('[data-testid="listing-card"]')

    print(f" {len(annonces)} annonces trouvées sur cette page.")

    for annonce in annonces:
        titre_tag = annonce.find("h3")
        prix_tag = annonce.find("p")

        titre = titre_tag.get_text(strip=True) if titre_tag else "N/A"
        prix = prix_tag.get_text(strip=True) if prix_tag else "N/A"

        # Suppression des emojis
        titre = remove_emojis(titre)
        prix = remove_emojis(prix)

        year = extract_year(titre)
        data.append([year, titre, prix])

driver.quit()

# Enregistrement dans un fichier CSV
output_file = "kijiji_voitures_final.csv"
write_to_csv(data, output_file)

print(f"\n  {len(data)} annonces enregistrées dans {output_file}")

# File paths for cleaning
input_file = "kijiji_voitures_final.csv"
output_file_cleaned = "kijiji_voitures_final_cleaned.csv"

# Function to remove the year from the title
def remove_year_from_title(title):
    # Matches years like 1990-2099 at the beginning of the title
    return re.sub(r"^\b(19|20)\d{2}\b\s*", "", title)

# Process the file to clean titles
with open(input_file, "r", encoding="utf-8") as infile, open(output_file_cleaned, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Split the line into fields using semicolon separator
        parts = line.strip().split(";")
        if len(parts) == 3:  # Ensure the line has Year, Title, and Price
            year, title, price = parts
            # Remove the year from the title
            title = remove_year_from_title(title)
            # Write the cleaned line to the output file
            outfile.write(f"{year};{title};{price}\n")

# MongoDB Atlas connection string
connection_string = "mongodb+srv://MB:mb@cluster0.luxsp4o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)
db = client["kijiji_database"]  # Replace with your database name
collection = db["kijiji_voitures"]  # Replace with your collection name

# Read the CSV file
csv_file = "kijiji_voitures_final_cleaned.csv"
df = pd.read_csv(csv_file, delimiter=";")

# Convert DataFrame to a list of dictionaries
data = df.to_dict(orient="records")

# Insert data into MongoDB
collection.insert_many(data)

print("Data successfully inserted into MongoDB Atlas!")
