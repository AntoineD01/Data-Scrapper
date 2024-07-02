# Formula 2 Event Scraper and Google Calendar Integration

This project is a Python script that scrapes Formula 2 race event details from the FIA Formula 2 website and adds them to a Google Calendar. The script checks for existing events to avoid duplication and is designed to run automatically on a weekly schedule.

## Features

- Scrapes event details from the FIA Formula 2 website
- Checks if events already exist in the Google Calendar
- Adds new events to the Google Calendar
- Can be scheduled to run automatically on a weekly basis

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `google-auth` library
- `google-auth-oauthlib` library
- `google-auth-httplib2` library
- `google-api-python-client` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/formula2-calendar.git
    cd formula2-calendar
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google Calendar API:

    - Go to the [Google Developers Console](https://console.developers.google.com/).
    - Create a new project.
    - Enable the Google Calendar API for the project.
    - Create OAuth 2.0 credentials and download the `credentials.json` file.
    - Place the `credentials.json` file in the project directory.

## Usage

1. Run the script manually:

    ```bash
    python main.py
    ```

2. To schedule the script to run automatically on a weekly basis:

    - On Windows, use the Task Scheduler:

        - Open Task Scheduler and create a new task.
        - Set the trigger to run weekly.
        - Set the action to start a program and browse to your Python interpreter (e.g., `C:\Users\Antoine Dupont\AppData\Local\Microsoft\WindowsApps\python3.exe`).
        - Add the script path as an argument (e.g., `C:\path\to\your\script\main.py`).

    - On Linux, use cron:

        - Open the crontab editor:

            ```bash
            crontab -e
            ```

        - Add a line to run the script weekly (adjust the path to your Python interpreter and script):

            ```bash
            0 0 * * 0 /usr/bin/python3 /path/to/your/script/main.py
            ```

## Script Details

- The script scrapes the event details from the FIA Formula 2 website using `requests` and `beautifulsoup4`.
- It checks for existing events in the Google Calendar to avoid duplicates using the Google Calendar API.
- New events are added to the Google Calendar if they do not already exist.

## Troubleshooting

- If you encounter an `invalid_grant: Bad Request` error, delete the `token.json` file and run the script again to reauthorize access.
- Ensure your `credentials.json` file is correctly configured and located in the project directory.
- Check the `script.log` file for detailed error messages and logs.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Google Calendar API](https://developers.google.com/calendar)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/)

