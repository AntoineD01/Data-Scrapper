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
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    for i in range(1069, 1070):
        id = str(i)
        # URL of the F2 page
        URL = "https://www.fiaformula2.com/Results?raceid=" + id

        # Send an HTTP request to the website
        response = requests.get(URL)
        all_messages = []
        # Verify if it's successful
        if response.status_code == 200:
            page_content = response.content

            # Use bs to analyse the page
            soup = bs(page_content, 'html.parser')

            # Extract the location
            text_location = soup.find('div', class_='country-circuit')
            if text_location:
                p = text_location.find('p')
                if p:
                    location = p.get_text(strip=True)
            print(f'\nLocation : {location}')
            messages = {'location': location}
            # Extract the date
            text_date= soup.find('div', class_='schedule')
            if text_date:
                spans = text_date.find_all('span')
                
                if spans:
                    second_span = spans[1]
                    date = second_span.get_text(strip=True)
            print(f'Date : {date}')
            
            
            # Extract the info of the event
            events_container = soup.find_all('div', class_='pin')
            done = 0
            for event in events_container:
                event_details = event.find_all('div')
                if event_details:
                    event_name = event_details[0].get_text(strip=True)
                    messages['name'] = event_name
                    event_day = event_details[1].get_text(strip=True)
                    messages['day'] = event_day
                    if len(event_details) == 3:
                        event_time = event_details[2].get_text(strip=True)
                        messages['time'] = event_time
                        event_date = reformat_date(date, event_day)
                        messages['date'] = event_date
                        print(f"Event: {event_name}, Day: {event_day}, Time: {event_time}, Date: {event_date}")
                        all_messages.append(messages.copy())
                    else:
                        done = 1
                
            # If the race has already taken place
            if done == 1:
                print("This race is over.")
        else:
            print(f"Erreur lors de la requête HTTP: {response.status_code}")

        event_info = {}
        for event in all_messages:
            event_info[event['name']] = adapt_text(event)

        #print(event_info)
        for event in all_messages:
            create_event(event, event_info)
        
def reformat_date(date_range_str, day_name):
    # Split the date range string to extract the start and end dates
    start_date_part, end_date_part = date_range_str.split('-')
    start_date_part = start_date_part.strip()
    end_date_part = end_date_part.split()[0].strip()
    
    # Extract the month and year from the string
    month_year_part = date_range_str.split()[-2] + " " + date_range_str.split()[-1]
    
    # Combine the start date part with the month and year
    full_start_date_str = f"{start_date_part} {month_year_part}"
    full_end_date_str = f"{end_date_part} {month_year_part}"
    
    # Parse the combined date strings
    parsed_start_date = datetime.datetime.strptime(full_start_date_str, '%d %B %Y')
    parsed_end_date = datetime.datetime.strptime(full_end_date_str, '%d %B %Y')
    
    # Determine the correct date based on the day_name parameter
    if day_name.lower() == 'friday':
        target_date = parsed_start_date
    elif day_name.lower() == 'saturday':
        target_date = parsed_start_date + datetime.timedelta(days=1)
    elif day_name.lower() == 'sunday':
        target_date = parsed_end_date
    else:
        raise ValueError("day_name must be 'Friday', 'Saturday', or 'Sunday'")
    
    # Format the target date into the desired output format
    formatted_date = target_date.strftime('%Y-%m-%d')
    
    return formatted_date

def adapt_text(event):
    start, end = split_time_range(event['time'])
    event_start = event['date']+ 'T' + start + ':00+02:00'
    event_end = event['date']+ 'T' + end + ':00+02:00'
    return event_start, event_end

def split_time_range(time_range):
    start_time, end_time = time_range.split('-')
    return start_time, end_time

def check_event_existence(service, event_data):
    try:
        # Define the time range to search for events
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        

        # Call the Calendar API to retrieve events within the time range
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        #print(f'Event result : {events_result}\n')

        # Get the list of events
        events = events_result.get('items', [])
        #print(f'Event : {events}\n')
        # Iterate through each event and check if it matches the event_data
        for existing_event in events:
            #print(f'Existing event : {existing_event}\n')
            # Compare event summary, start time, and end time
            if (existing_event.get('summary') == event_data['summary']
                    and existing_event.get('start').get('dateTime') == event_data['start'].get('dateTime')
                    and existing_event.get('end').get('dateTime') == event_data['end'].get('dateTime')):
                # Similar event found
                return True

        # No similar event found
        return False

    except Exception as e:
        print(f"An error occurred while checking event existence: {e}")
        return False

def create_event(event, event_info):
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)
        # Create the event object
        event_data = {
            'summary': event['name'],
            'location': event['location'],
            'start': {
                'dateTime': event_info[event['name']][0],
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': event_info[event['name']][1],
                'timeZone': 'Europe/Paris',
            },
        }

        
        if check_event_existence(service, event_data):
            print(f'This event already exist.')
        else:
            # Insert the event into the calendar
            """event = service.events().insert(calendarId='primary', body=event_data).execute()
            print(f"Event created: {event.get('htmlLink')}")"""
            print("We enter the data !")
    
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()