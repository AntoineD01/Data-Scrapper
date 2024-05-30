import requests
from bs4 import BeautifulSoup as bs
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError





# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  for i in range (1064, 1077):
    id = str(i)
    # URL of the F2 page
    URL = "https://www.fiaformula2.com/Results?raceid="+id

    # Send an HTTP request to the website 
    response = requests.get(URL)

    # Verify if it's successful
    if response.status_code == 200:
        page_content = response.content
    
        # Use bs to analyse the page
        soup = bs(page_content, 'html.parser')
    
        
        # Extract the info of the location
        text_location = soup.find('div', class_='country-circuit')
        if text_location:
            p = text_location.find('p')
            if p:
                location = p.get_text(strip=True)
        print(f'\nLocation : {location}')
        
        # Extract the info of the event
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
        #If the race has already taken place
        if done==1:
            print("This race is over.")

    else:
        print(f"Erreur lors de la requête HTTP: {response.status_code}")

  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    
  except HttpError as error:
    print(f"An error occurred: {error}")
"""

if __name__ == "__main__":
  main()