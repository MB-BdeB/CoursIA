import requests

url ='https://degenio.com/html5/contacts.json'

reponse = requests.get(url)
data = reponse.json()
# print(data['contacts'])
# print(reponse.status_code)
for item in data['contacts']:
    # print(item)
    for k,v in item.items():
        print(f"{k}: {v}")
    print('-------------------')