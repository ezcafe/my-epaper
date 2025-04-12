# epaper

## Install libs

sudo apt install python3-caldav

## Keys

### Creating an App-Specific Password:

Go to https://appleid.apple.com/ and sign in.
In the Security section, click "Generate Password" under App-Specific Passwords.
Follow the steps to create a password and use this as your APPLE_PASSWORD.

### Update Password

Add these lines to ~/.bashrc

export APPLE_ID='your_apple_id@icloud.com'
export APPLE_PASSWORD='your_app_specific_password'