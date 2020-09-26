"""Commander for interacting with Google Drive"""

import sys
import os
import csv
from .perms import DRIVE_READONLY, SHEET_READONLY, SHEET_FULL
from .drive import Drive
from .sheets import SheetsApi, Spreadsheet

BLUE = "\033[94m"
NOCOLOR = "\033[0m"

def ls(args) -> None:
    drive = Drive(DRIVE_READONLY, credentials=args.creds, token=args.token)
    files = drive.ls(args.path)

    print(args.path)
    files = sorted(files, key=lambda x: x.name)
    for file in files:
        full_path = os.path.join(args.path, file.name)

        color = NOCOLOR
        if file.isDir:
            color = BLUE

        if args.l:
            timestamp = file.modifiedTime
            print("%s%s (%s)%s" % (color, full_path, timestamp, NOCOLOR))
        else:
            print("%s%s%s" % (color, full_path, NOCOLOR))

def csv_download(args):
    drive  = Drive(DRIVE_READONLY, credentials=args.creds, token=args.drive_token)
    api = SheetsApi(SHEET_READONLY, credentials=args.creds, token=args.sheets_token)

    drive.ls(args.SPREADSHEET)
    if args.SPREADSHEET not in drive.fs:
        print("File not found")
        sys.exit(-1)

    f = drive.fs[args.SPREADSHEET]
    sheet = Spreadsheet(api, f.id)
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
    sheets = SheetsApi(SHEET_FULL, credentials=args.creds, token=args.sheets_token)

    drive.ls(args.SPREADSHEET)
    if args.SPREADSHEET not in drive.fs:
        print("File not found")
        sys.exit(-1)
    f = drive.fs[args.SPREADSHEET]
    sheet = Spreadsheet(sheets, f.id)
    sheet.upload_csv(args.CSV, args.SHEET)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    def print_help(_arg):
        parser.print_help()
    parser.set_defaults(func=print_help)
    subparsers = parser.add_subparsers()

    def new_drive_subparser(cmd, func):
        sub = subparsers.add_parser(cmd)
        sub.add_argument("--creds", default="credentials.json", metavar="CREDENTIALS.JSON")
        sub.add_argument("--token", default="token.json", metavar="TOKEN.JSON")
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

    p_csv_download = new_sheets_subparser("csv-download", csv_download)
    p_csv_download.add_argument("SPREADSHEET", type=str, help="Path to the SPREADSHEET")
    p_csv_download.add_argument("SHEET", type=str, help="Name of the SHEET within the spreadsheet")
    p_csv_download.add_argument("CSV", type=str, default=None, nargs="?",
        help="Write output to this CSV file. Printing to stdout if not specified")

    p_csv_upload = new_sheets_subparser("csv-upload", csv_upload)
    p_csv_upload.add_argument("SPREADSHEET", type=str, help="Path to the SPREADSHEET")
    p_csv_upload.add_argument("SHEET", type=str, help="Name of the SHEET within the spreadsheet")
    p_csv_upload.add_argument("CSV", type=str)

    pargs, unknown_args = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + unknown_args

    pargs.func(pargs)
