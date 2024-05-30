import requests
from bs4 import BeautifulSoup as bs



for i in range (1064, 1077):
    id = str(i)
    # URL de la page F2
    URL = "https://www.fiaformula2.com/Results?raceid="+id

    # Envoyer une requête HTTP au site web
    response = requests.get(URL)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        page_content = response.content
    
        # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
        soup = bs(page_content, 'html.parser')
    
        
        # Extraire les informations des événements
        text_location = soup.find('div', class_='country-circuit')
        if text_location:
            p = text_location.find('p')
            if p:
                location = p.get_text(strip=True)
        print(f'\nLocation : {location}')
        
        # Extraire les informations des événements
        events_container = soup.find_all('div', class_='pin')
        done = 0
        for event in events_container:
            event_details = event.find_all('div')
            if event_details:
                event_name = event_details[0].get_text(strip=True)
                event_day = event_details[1].get_text(strip=True)
                if len(event_details) == 3:
                    event_time = event_details[2].get_text(strip=True)
                    print(f"Event: {event_name}, Day: {event_day}, Time: {event_time}")
                else:
                    done = 1
        
        if done==1:
            print("This race is over.")
    else:
        print(f"Erreur lors de la requête HTTP: {response.status_code}")


