# Google Drive Lib

This is a library to write simple Google Drive management/backup tools using Python.

## Usage

After quickly setting up the environment you can run the google drive commander like this:

```bash
# List files in the root directory
bin/gdrive ls /

# Download a file
bin/gdrive scp drive:/test.pdf ~/test.pdf

# Upload a file
bin/gdrive scp ~/test.pdf drive:/test.pdf
```

## Setup

You need to only do two small things to be able to access the Google Drive API. You need to set up the python environment with the relevant libraries and set up permissions in the Drive itself. Below is information on how to do both of these things.

### Setting up the Python Environment
You'll need to run the following commands to setup the virtual environment and download the packages:

```bash
python3 -m venv .google-drive-venv
source .google-drive-venv/bin/activate
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client mypy pylint
```

### Setting up the Google Drive API permissions

To use the Google Drive API you need to do step 1 and step 2 as outlined in these docs (this needs to be done only once): 
https://developers.google.com/drive/api/v3/quickstart/python

You can see your live projects here: https://console.cloud.google.com/

Then you'll need to move the `credentials.json` and `token.json` files either to where you are running the gdrive binary from or pass the location in using the arguments `gdrive --token ~/token.json --creds ~/creds.json`.

## Documentation

Drive API Docs
 - https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html
 - https://developers.google.com/drive/api/v3/manage-downloads

Sheets API Docs
 - https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html


