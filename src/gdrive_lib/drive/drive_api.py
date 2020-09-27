from googleapiclient.discovery import build # type: ignore
from httplib2 import Http # type: ignore
from ..api_utils import init_credentials

DRIVE_READONLY = "https://www.googleapis.com/auth/drive.readonly"
DRIVE_FULL     = "https://www.googleapis.com/auth/drive"
DRIVE_PER_FILE = "https://www.googleapis.com/auth/drive.file"

class DriveApi:
    """Handles interactions with the Google Drive filesystem."""

    def __init__(self, scope, credentials, token) -> None:
        creds = init_credentials(credentials, token, scope)
        self.__service = build('drive', 'v3', http=creds.authorize(Http()))

    def files(self):
        # pylint: disable=E1101
        return self.__service.files()
