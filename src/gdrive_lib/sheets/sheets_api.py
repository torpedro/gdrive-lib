"""Manage queries and permissions for Sheets API"""

from typing import Any
from googleapiclient.discovery import build # type: ignore
from httplib2 import Http # type: ignore
from ..api_utils import init_credentials

class SheetsApi:
    """Handles interactions with Sheet documents."""

    def __init__(self,
            scope="https://www.googleapis.com/auth/spreadsheets.readonly",
            credentials="credentials.json",
            token="token.json") -> None:

        creds = init_credentials(credentials, token, scope)
        self.__service = build('sheets', 'v4', http=creds.authorize(Http()))

    def __api(self) -> Any:
        # pylint: disable=E1101
        return self.__service.spreadsheets()

    def values(self) -> Any:
        return self.__api().values()

    def get(self, spreadsheet_id) -> Any:
        return self.__api().get(spreadsheetId=spreadsheet_id)

    def batch_update(self, file_id, requests) -> None:
        """Send the given batch update [requests] for the given file"""

        if len(requests) > 0:
            body = { "requests": requests }
            self.__api().batchUpdate(spreadsheetId=file_id, body=body).execute()
