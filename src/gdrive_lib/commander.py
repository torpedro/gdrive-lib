"""Commander for interacting with Google Drive"""

import sys
import os
import csv
import argparse
import re
from .drive.drive import Drive
from .drive.drive_api import DRIVE_READONLY, DRIVE_PER_FILE
from .sheets.sheets import Sheets
from .sheets.sheets_api import SHEET_FULL, SHEET_READONLY

BLUE = "\033[94m"
NOCOLOR = "\033[0m"

def ls(args) -> None:
    drive = Drive(DRIVE_READONLY, credentials=args.creds, token=args.drive_token)
    files = drive.ls(args.path)

    print(args.path)
    files = sorted(files, key=lambda x: x.name)
    for file in files:
        full_path = os.path.join(args.path, file.name)

        color = NOCOLOR
        if file.is_dir:
            color = BLUE

        if args.l:
            timestamp = file.modified_time
            print("%s%s (%s)%s" % (color, full_path, timestamp, NOCOLOR))
        else:
            print("%s%s%s" % (color, full_path, NOCOLOR))

def csv_download(args):
    drive = Drive(DRIVE_READONLY, credentials=args.creds, token=args.drive_token)
    sheets = Sheets(SHEET_READONLY, credentials=args.creds, token=args.sheets_token)

    drive.ls(args.SPREADSHEET)
    if drive.fs.file_exists_at_path(args.SPREADSHEET):
        print("File not found")
        sys.exit(-1)

    f = drive.fs.by_path(args.SPREADSHEET)
    sheet = sheets.get_spreadsheet(f.id)
    data  = sheet.get_data(sheet_name=args.SHEET)

    if args.CSV is None:
        writer = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)
    else:
        with open(args.CSV, mode='w') as fh:
            writer = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

def csv_upload(args):
    drive  = Drive(DRIVE_READONLY, credentials=args.creds, token=args.drive_token)
    sheets = Sheets(SHEET_FULL, credentials=args.creds, token=args.sheets_token)

    drive.ls(args.SPREADSHEET)
    if drive.fs.file_exists_at_path(args.SPREADSHEET):
        print("File not found")
        sys.exit(-1)
    f = drive.fs.by_path(args.SPREADSHEET)
    sheet = sheets.get_spreadsheet(f.id)
    sheet.upload_csv(args.CSV, args.SHEET)

class ScpArgs:
    is_remote : bool
    path : str

    def __init__(self, path):
        match = re.match(r"^drive:(.+)$", path)
        if match:
            self.is_remote = True
            self.path = match.group(1)
        else:
            self.is_remote = False
            self.path = path


def scp(args):
    src : ScpArgs = args.src
    dst : ScpArgs = args.dst

    if src.is_remote and (not dst.is_remote):
        print("Downloading %s to %s" % (src.path, dst.path))
        drive = Drive(DRIVE_READONLY, credentials=args.creds, token=args.drive_token)
        drive.ls(src.path)
        drive.download(src.path, dst.path)
    elif (not src.is_remote) and dst.is_remote:
        print("Uploading %s to %s" % (src.path, dst.path))
        drive = Drive(DRIVE_PER_FILE, credentials=args.creds, token=args.drive_token)
        drive.ls(dst.path)
        drive.upload(src.path, dst.path)
    else:
        print("One of the two given paths must be local while the other is remote!")
        sys.exit(-1)

def main():
    parser = argparse.ArgumentParser()
    def print_help(_arg):
        parser.print_help()
    parser.set_defaults(func=print_help)
    subparsers = parser.add_subparsers()

    def new_drive_subparser(cmd, func):
        sub = subparsers.add_parser(cmd)
        sub.add_argument("--creds", default="credentials.json", metavar="CREDENTIALS.JSON")
        sub.add_argument("--token", default="token.json", metavar="TOKEN.JSON", dest="drive_token")
        sub.set_defaults(func=func)
        return sub

    def new_sheets_subparser(cmd, func):
        sub = subparsers.add_parser(cmd)
        sub.add_argument("--creds", default="credentials.json", metavar="CREDENTIALS.JSON")
        sub.add_argument("--drive-token", default="token.json", metavar="TOKEN.JSON")
        sub.add_argument("--sheets-token", default="token.json", metavar="TOKEN.JSON")
        sub.set_defaults(func=func)
        return sub

    p_ls = new_drive_subparser("ls", ls)
    p_ls.add_argument("path", type=str, metavar="PATH")
    p_ls.add_argument("-l", action='store_true')

    p_scp = new_drive_subparser("scp", scp)
    p_scp.add_argument("src", type=ScpArgs, metavar="SOURCE")
    p_scp.add_argument("dst", type=ScpArgs, metavar="TARGET")

    p_csv_download = new_sheets_subparser("csv-download", csv_download)
    p_csv_download.add_argument("SPREADSHEET", type=str, help="Path to the SPREADSHEET")
    p_csv_download.add_argument("SHEET", type=str, help="Name of the SHEET within the spreadsheet")
    p_csv_download.add_argument("CSV", type=str, default=None, nargs="?",
        help="Write output to this CSV file. Printing to stdout if not specified")

    p_csv_upload = new_sheets_subparser("csv-upload", csv_upload)
    p_csv_upload.add_argument("SPREADSHEET", type=str, help="Path to the SPREADSHEET")
    p_csv_upload.add_argument("SHEET", type=str, help="Name of the SHEET within the spreadsheet")
    p_csv_upload.add_argument("CSV", type=str)

    args, unknown_args = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + unknown_args

    args.func(args)

if __name__ == "__main__":
    main()
