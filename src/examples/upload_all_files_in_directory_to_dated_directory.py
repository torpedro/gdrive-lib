#!/usr/bin/python
import sys
import os
import datetime
dirname = os.path.dirname(__file__)
sys.path.append(("%s/.." % (dirname)))

# pylint: disable=wrong-import-position
from gdrive_lib.drive import Drive
# pylint: enable=wrong-import-position

def upload_all_files_to_a_dated_directory(source_dir):
    """Uploads all the files in the given local directory to a dated directory under /archive in Google Drive. Creates the remote directories if they don't exist"""
    drive = Drive()
    remote_dir = "/archive"
    to_upload = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Create a dated directory
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    dated_dir = os.path.join(remote_dir, date)

    drive.ls(remote_dir)
    if remote_dir not in drive.fs:
        drive.mkdir(remote_dir)

    if not dated_dir in drive.fs:
        drive.mkdir(dated_dir)

    # Upload the files
    for file in to_upload:
        local = os.path.join(source_dir, file)
        remote = os.path.join(dated_dir, os.path.basename(local))
        drive.upload(local, remote)

def main():
    upload_all_files_to_a_dated_directory("./test-for-uploads")

if __name__ == '__main__':
    main()
