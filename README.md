# epaper

## Hardware

### Wiring between Raspberry PI and E-Ink Display

Raspberry Pi                    E Ink Display
3.3V (Pin 1)       ------->     VCC
GND  (Pin 6)       ------->     GND
MOSI (Pin 19)      ------->     DIN (SDA)
SCLK (Pin 23)      ------->     CLK (SCL)
CE0  (Pin 24)      ------->     CS
GPIO (Pin 22)      ------->     DC  (D/C)
GPIO (Pin 11)      ------->     RST (RES)
GPIO (Pin 18)      ------->     BUSY

### Enable Raspberry Pi I2C and SPI

sudo raspi-config

Select the 3 Interface Options option.
Select "I4 SPI" and "I5 I2C"

## Install libs

sudo apt-get update
sudo apt-get install python3-pip, python3-pil, python3-caldav, python3-dotenv

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

## Auto run

To make my-calendar run on each boot automatically, you can use crontab. Do not use sudo for this

crontab -e

then add this (update calendar every 30 mins)

*/30 * * * * python3 $HOME/my-epaper/my-calendar.py

To view schedule list

crontab -l