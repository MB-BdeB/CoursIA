import requests

uri = 'https://www.degenio.com/html5/contacts.json'
reponse = requests.get(uri)
data = reponse.json()
contacts = data['contacts']
counter = 1
for tmp in contacts:
    print(f'Contact:{counter}')
    for k,v in tmp.items():
        if k == 'phone':
            print('Téléphone')
            print('-'*10)
            for m,n in v.items():
                print(m,':',n)
        else:
            print(k,':',v)
    print('=' * 50)
    counter += 1