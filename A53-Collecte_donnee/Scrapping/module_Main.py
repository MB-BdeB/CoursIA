import requests
from bs4 import BeautifulSoup


url = "https://www.meteo.gc.ca/fr/location/index.html?coords=45.529,-73.562"

response = requests.get(url).content
#print (response)
scrap = BeautifulSoup(response, "html.parser")
#print(scrap)
# <p data-v-53399591="" class="mrgn-bttm-sm lead mrgn-tp-sm"><span data-v-53399591="">21°</span><abbr data-v-53399591="" title="Celsius">C</abbr></p>
# <span data-v-53399591="">21°</span>
temperature = scrap.find("p", class_="mrgn-bttm-sm lead mrgn-tp-sm").find("span").text
print(f"Temperature: {temperature}")
#   
location = scrap.find("h1", id="wb-cont").text
print(f"Location: {location}")
previson_ce_soir = scrap.find("tr", class_="pdg-tp-0").find_all("td")[1].text
print(f"Prévision ce soir: {previson_ce_soir.strip()}")

