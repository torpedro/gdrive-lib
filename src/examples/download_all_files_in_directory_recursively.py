#!/usr/bin/python
import sys
import os
dirname = os.path.dirname(__file__)
sys.path.append(("%s/.." % (dirname)))

# pylint: disable=wrong-import-position
from gdrive_lib.drive.drive import Drive
# pylint: enable=wrong-import-position

def download_all_files_from_directory_rec(source_dir, target_dir):
    """Downloads all files in the Google Drive directory at [source_dir] (recursively)
         into the [target_dir] on the local machine."""
    drive = Drive("https://www.googleapis.com/auth/drive.readonly")
    files = drive.ls(source_dir)
    for file in files:
        if not file.is_dir:
            print("Downloading %s" % (file.name))
            output_file = os.path.join(target_dir, file.name)
            drive.download(file.path, output_file)
        else:
            new_source_dir = os.path.join(source_dir, file.name)
            download_all_files_from_directory_rec(new_source_dir, target_dir)


def main(remote, local):
    download_all_files_from_directory_rec(remote, local)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("USAGE: %s REMOTE_DIR LOCAL_DIR" % os.path.basename(__file__))
        sys.exit(-1)


    remote_dir = sys.argv[1]
    download_dir = sys.argv[2]
    sys.argv = [sys.argv[0]] + sys.argv[3:]
    main(remote_dir, download_dir)
