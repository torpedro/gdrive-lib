#!/usr/bin/python
import sys
import os
from datetime import datetime

dirname = os.path.dirname(__file__)
sys.path.append(("%s/.." % (dirname)))
# pylint: disable=wrong-import-position
from gdrive_lib.drive import Drive
# pylint: enable=wrong-import-position

def download_all_files_in_directory(remote_dir, download_dir):
    """Downloads all files in the Google Drive directory at [remote_dir] (not recursively)
         into the [download_dir] on the local machine."""

    drive = Drive("https://www.googleapis.com/auth/drive.readonly")
    files = drive.ls(remote_dir)
    for file in files:
        if not file.is_dir:
            local_path = os.path.join(download_dir, file.name)

            do_download = True
            if args.only_new and os.path.isfile(local_path):
                mod_time = datetime.fromtimestamp(os.path.getmtime(local_path))
                if mod_time > file.modified_time:
                    print("Skipping %s, because the local file is newer." % (file.name))
                    do_download = False

            if do_download:
                print("Downloading %s" % (file.name))
                drive.download(file.path, local_path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("REMOTE_DIR", type=str)
    parser.add_argument("LOCAL_DIR", type=str)
    parser.add_argument("--only_new", action='store_true')
    parser.add_argument("--noauth_local_webserver", action='store_true')
    args = parser.parse_args()

    download_all_files_in_directory(args.REMOTE_DIR, args.LOCAL_DIR)
