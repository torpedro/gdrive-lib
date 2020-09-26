# Google Drive Archiver Lib

This is a library to write simple Google Drive management/backup tools using Python.

## Setup

To use the Google Drive API you need to do step 1 and step 2 as outlined in these docs (this needs to be done only once): 
https://developers.google.com/drive/api/v3/quickstart/python

You can see your live projects here: https://console.cloud.google.com/

You'll need to run the following commands to setup the virtual environment and download the packages:

```bash
python3 -m venv .google-drive-venv
source .google-drive-venv/bin/activate
ip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
```

Then you need to move the `credentials.json` file to wherever you're running the tools from and you're good to go.

To see that it all works and set the permissions run `src/examples/ls.py /`.

## Documentation

Drive API Docs
 - https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html
 - https://developers.google.com/drive/api/v3/manage-downloads

Sheets API Docs
 - https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html


## Examples

Below are some examples of how one can use this library to write tools interacting with Google Drive. There's also couple of working example scripts in `src/examples`.

```python
def download_all_files_from_directory(source_dir, target_dir):
  """Downloads all files in the Google Drive directory at [source_dir] (not recursively)
     into the [target_dir] on the local machine."""
  drive = Drive()
  files = drive.ls(source_dir)
  for file in files:
    if not file.isDir:
      print("Downloading %s" % (file.name))
      output_file = os.path.join(target_dir, file.name)
      drive.download(file.path, output_file)
```

```python
def upload_all_files_to_a_dated_directory(source_dir):
  """Uploads all the files in the given local directory to a dated directory under
     [/archive] in Google Drive. Creates the remote directories if they don't exist"""
  drive = Drive()
  remote_dir = "/archive"
  to_upload = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

  # Create a dated directory
  date = datetime.datetime.today().strftime('%Y-%m-%d')
  dated_dir = os.path.join(remote_dir, date)

  drive.ls(remote_dir)
  if not remote_dir in drive.fs:
    drive.mkdir(remote_dir)

  if not dated_dir in drive.fs:
    drive.mkdir(dated_dir)
  
  # Upload the files
  for file in to_upload:
    local = os.path.join(source_dir, file)
    remote = os.path.join(dated_dir, os.path.basename(local))
    drive.upload(local, remote)
```

## Guidelines

For code documentation, we try to follow the Google Styleguide: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
