# epaper

## Install libs

sudo apt install python3-caldav
sudo apt install python3-dotenv

## Keys

### Creating openweathermap api key

Go to https://openweathermap.org/api and sign in.
Go to https://home.openweathermap.org/api_keys, input API key name click and click Generate
Use Key as your WEATHER_API_KEY.

### Creating an Apple App-Specific Password:

Go to https://appleid.apple.com/ and sign in.
In the Security section, click "Generate Password" under App-Specific Passwords.
Follow the steps to create a password and use this as your APPLE_PASSWORD.

### Get calendar name

Go to Calendar app on your iPhone
Click on Calendars button at the bottom of the app
Use calendar name in iCloud section as your APPLE_CALENDAR_NAME

### Update information

Update above values to .env file

APPLE_ID='your_apple_id@icloud.com'
APPLE_PASSWORD='your_app_specific_password'
APPLE_CALENDAR_NAME = 'your_calendar_name'
WEATHER_API_KEY='your_api_key'
SPECIAL_DAYS='[["Payday", "25"], ["Birthday", "20/02"], ["Travel", "26/1"], ["New Year", "1/1"]]'