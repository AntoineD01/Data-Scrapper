import requests
from bs4 import BeautifulSoup as bs

# URL de la page F2
URL = "https://www.fiaformula2.com/Results?raceid=1069"

# Envoyer une requête HTTP au site web
response = requests.get(URL)

# Vérifiez si la requête a réussi
if response.status_code == 200:
    page_content = response.content
    
    # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
    soup = bs(page_content, 'html.parser')
    
    # Extraire les informations des événements
    events_container = soup.find_all('div', class_='pin')
    
    for event in events_container:
        event_details = event.find_all('div')
        if event_details:
            event_name = event_details[0].get_text(strip=True)
            event_day = event_details[1].get_text(strip=True)
            event_time = event_details[2].get_text(strip=True)
            print(f"Event: {event_name}, Day: {event_day}, Time: {event_time}")
else:
    print(f"Erreur lors de la requête HTTP: {response.status_code}")
