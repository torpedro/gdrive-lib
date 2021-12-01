import datetime
from os.path import join


class File():
    """Represents what we know about a file on the Google Drive."""

    def __init__(self, base_path, data):
        self.data = data
        self.id = data['id']
        self.name = data['name']
        self.parents = data['parents']
        self.is_dir = data['mimeType'] == "application/vnd.google-apps.folder"

        if "trashed" in data:
            self.trashed = data["trashed"]
        else:
            self.trashed = False

        if "modifiedTime" in data:
            self.modified_time = datetime.datetime.strptime(
                data["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ")

        self.path = join(base_path, self.name)

    @staticmethod
    def ROOT():
        return File("/", {
            "id": "root",
            "name": "",
            "parents": [],
            "mimeType": "application/vnd.google-apps.folder"
        })
