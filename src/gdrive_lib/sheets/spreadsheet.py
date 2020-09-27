"""Handles operations on Google Spreadsheets."""

import csv
from typing import Any, List, Optional
from .sheets_api import SheetsApi

class Spreadsheet:
    __api : SheetsApi
    file_id : str

    def __init__(self, api, file_id) -> None:
        self.__api = api
        self.file_id = file_id


    def get_data(self, sheet_name=None, cell_range="A:Z") -> List[Any]:
        """Returns all values in the range A:Z within the given sheet."""

        if sheet_name is not None:
            cell_range = "%s!%s" % (sheet_name, cell_range)

        result = self.__api.values().get(spreadsheetId=self.file_id, range=cell_range).execute()
        values = result.get('values', [])
        return values

    def upload_csv(self, local, sheet_name, delimiter=',', cell="A1") -> None:
        """Reads all values from the csv file and writes it to the remote sheet."""
        spreadsheet = self.__api.get(self.file_id).execute()

        matching_sheets = [sheet for sheet in spreadsheet['sheets']
                    if sheet['properties']['title'] == sheet_name]

        sheet : Optional[str] = None
        if len(matching_sheets) > 0:
            sheet = matching_sheets[0]

        with open(local, "r") as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            lines = list(reader)

            if sheet is None:
                self.add_sheet(sheet_name)
            else:
                rows = len(lines)
                cols = max([len(line) for line in lines])
                self.resize_sheet(sheet, rows, cols)
            self.write_data(lines, sheet_name=sheet_name, cell=cell)

    def add_sheet(self, sheet_name) -> None:
        """Add a sheet with the given name to the file"""

        requests = [
            { "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "gridProperties": {
                            "rowCount": 1,
                            "columnCount": 1
                        }
                    }
                }
            }
        ]
        return self.__api.batch_update(self.file_id, requests)

    def resize_sheet(self, sheet, rows, cols) -> None:
        """Resize the given sheet to the given rows and cols"""

        sheet_id = sheet['properties']['sheetId']
        cur_rows = sheet['properties']['gridProperties']['rowCount']
        cur_cols = sheet['properties']['gridProperties']['columnCount']
        requests = []
        if cur_rows < rows:
            requests.append({
                "insertDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": cur_rows,
                        "endIndex": rows
                    },
                    "inheritFromBefore": True
                }
            })
        elif cur_rows > rows:
            requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": rows
                    }
                }
            })
        if cur_cols < cols:
            requests.append({
                "insertDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": cur_cols,
                        "endIndex": cols
                    },
                    "inheritFromBefore": True
                }
            })
        elif cur_cols > cols:
            requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": cols
                    }
                }
            })
        self.__api.batch_update(self.file_id, requests)


    def write_data(self, values, sheet_name=None, cell="A1") -> None:
        """Writes the given values into the cells within the given sheet."""

        if sheet_name is not None:
            cell = "%s!%s" % (sheet_name, cell)

        body = { "values": values }

        self.__api.values().update(
            spreadsheetId=self.file_id,
            range=cell,
            body=body,
            valueInputOption="USER_ENTERED").execute()

        return values
