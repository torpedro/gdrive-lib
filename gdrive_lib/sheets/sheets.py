from .sheets_api import SheetsApi
from .spreadsheet import Spreadsheet

class Sheets:
    def __init__(self, scope, credentials, token) -> None:
        self.__api = SheetsApi(scope, credentials, token)

    def get_spreadsheet(self, file_id : str) -> Spreadsheet:
        return Spreadsheet(self.__api, file_id)
