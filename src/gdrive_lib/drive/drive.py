"""Handles operations on the files within the Drive."""

import io
import datetime
from typing import List, Optional, Dict
from os.path import join, basename, dirname
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload # type: ignore
from .drive_api import DriveApi, DRIVE_READONLY
from .file import File
from .filesystem import Filesystem

FILE_FIELDS = 'id, name, parents, mimeType, trashed, modifiedTime'

class Drive():
    """Handles interactions with the Google Drive filesystem."""

    def __init__(self,
            scope=DRIVE_READONLY,
            credentials="credentials.json",
            token="token.json"):
        self.__api = DriveApi(scope, credentials, token)
        self.fs = Filesystem()

    def __files(self):
        return self.__api.files()

    def __add_file(self, base_path : str, data) -> Optional[File]:
        """Creates a new file in our internal cache of the Drive fs."""
        f = File(base_path, data)
        return self.fs.add_file(f)

    def __rm_file(self, f : File) -> None:
        """Removes a file from our internal cache of the Drive fs."""
        self.fs.remove_file(f)

    def __locate_file(self, remote : str) -> bool:
        """Returns true if the file exists on the remote Drive fs."""

        if self.fs.file_exists_at_path(remote):
            return True

        self.ls(dirname(remote))
        return self.fs.file_exists_at_path(remote)

    def ls(self, path : str) -> List[File]:
        """Tries to find the file at the path and all its children if it's a folder."""

        if not self.fs.file_exists_at_path(path):
            parent = dirname(path)
            if parent == path:
                assert path == "/"
            self.ls(parent)
            if not self.fs.file_exists_at_path(path):
                return []

        parent = self.fs.by_path(path).id

        query = "'%s' in parents" % (parent)
        fields = "nextPageToken, files(%s)" % (FILE_FIELDS)

        results = self.__files().list(pageSize=500, q=query, fields=fields).execute()
        items = results.get('files', [])
        if items:
            files : List[File] = []
            for data in items:
                f = self.__add_file(path, data)
                if f is not None:
                    files.append(f)
            return files
        return []

    def download(self, remote : str, local : str) -> None:
        """Downloads the contents of the [remote] file and writes them to the [local] target."""

        if not self.fs.file_exists_at_path(remote):
            print("Can not download the file because we can't find anything at that path.", remote)
            return None

        f = self.fs.by_path(remote)

        if f.is_dir:
            print("Can not download a directory.", remote)
            return None


        request = self.__files().get_media(fileId=f.id)
        fh = io.FileIO(local, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            _status, done = downloader.next_chunk()

    def mv(self, path : str, to_folder : str) -> Optional[File]:
        """Move the file at [path] to the given folder"""

        f = self.fs.by_path(path)
        folder_id = self.fs.by_path(to_folder).id

        # Retrieve the existing parents to remove
        old_data = self.__files().get(fileId=f.id, fields='parents').execute()
        previous_parents = ",".join(old_data.get('parents'))
        # Move the f to the new folder
        new_data = self.__files().update(
            fileId=f.id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields=FILE_FIELDS).execute()

        self.__rm_file(f)
        return self.__add_file(to_folder, new_data)

    def mkdir(self, remote : str) -> Optional[File]:
        """Creates a new folder if nothing exists at that path yet."""

        self.ls(dirname(remote))
        if self.fs.file_exists_at_path(remote):
            # Something already exists at that path
            print("Can not create directory because something already exists at the path.", remote)
            return None

        folder_name = basename(remote)
        parent_path = dirname(remote)

        parent = self.fs.by_path(parent_path).id

        file_metadata = {
            "name": folder_name,
            "mimeType": 'application/vnd.google-apps.folder',
            "parents": [parent]
        }
        f = self.__files().create(body=file_metadata, fields=FILE_FIELDS).execute()
        return self.__add_file(parent_path, f)


    def upload(self, local : str, remote : str) -> Optional[File]:
        """Upload the given [local] file to the [remote] location"""

        file_name = basename(remote)
        parent_path = dirname(remote)

        if self.__locate_file(remote):
            print("Can not upload file because the remote file exists already.", remote)
            return None
        if not self.__locate_file(parent_path):
            print("Can not upload file because folder does not exist.", parent_path)
            return None

        file_metadata = {'name': file_name, 'parents': [ self.fs.by_path(parent_path).id ]}
        media = MediaFileUpload(local)
        f = self.__files().create(body=file_metadata, media_body=media, fields=FILE_FIELDS).execute()
        return self.__add_file(parent_path, f)

    def print_fs(self) -> None:
        """Prints information about all files that are currently cached locally."""
        self.fs.print()

    def ls_all(self) -> None:
        """Retrieves information about all non-trashed files in the drive"""

        frontier = [ "/" ]
        while len(frontier) > 0:
            path = frontier.pop(0)
            children = self.ls(path)
            for f in children:
                if f.is_dir and not f.trashed:
                    frontier.append(f.path)

    def rm(self, remote) -> None:
        """Moves the given file to the trash."""

        if not self.__locate_file(remote):
            print("Can not find anything at the path.", remote)
            return None

        f = self.fs.by_path(remote)
        metadata = {
            "trashed": True
        }

        _new_data = self.__files().update(fileId=f.id, body=metadata, fields=FILE_FIELDS).execute()
        self.__rm_file(f)
        return None
