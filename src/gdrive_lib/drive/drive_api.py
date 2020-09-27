from googleapiclient.discovery import build # type: ignore
from httplib2 import Http # type: ignore
from ..api_utils import init_credentials

class DriveApi:
    """Handles interactions with the Google Drive filesystem."""

    # If [scope] is modified, token.json needs to be deleted.
    def __init__(self,
            scope="https://www.googleapis.com/auth/drive.readonly",
            credentials="credentials.json",
            token="token.json") -> None:
        creds = init_credentials(credentials, token, scope)
        self.__service = build('drive', 'v3', http=creds.authorize(Http()))

    def files(self):
        # pylint: disable=E1101
        return self.__service.files()
