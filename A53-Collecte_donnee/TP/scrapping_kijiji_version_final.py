from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import re

#  Fonction pour supprimer les emojis
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

#  Initialisation
options = Options()
options.add_argument("--headless")
service = Service("C:/Users/bouma12/VSCode_WorkSpace/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://www.kijiji.ca/b-autos-et-camions/ville-de-montreal"
page_urls = [f"{base_url}/page-{i}/c174l1700281" for i in range(1, 3)]  # ~1000 lignes

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

        #  Suppression des emojis
        titre = remove_emojis(titre)
        prix = remove_emojis(prix)

        data.append([titre, prix])

driver.quit()

#  Enregistrement dans un fichier CSV
with open("kijiji_voitures.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Titre", "Prix"])
    writer.writerows(data)

print(f"\n  {len(data)} annonces enregistrées dans kijiji_voitures.csv")
