from typing import List, Optional, Dict
from .file import File

class Filesystem:
    __by_id : Dict[str, File]
    __by_path : Dict[str, File]

    def __init__(self):
        self.__by_id = {}
        self.__by_path = {}
        self.add_file(File.ROOT())
    
    def add_file(self, file : File) -> Optional[File]:
        if not file.trashed:
            self.__by_id[file.id] = file
            self.__by_path[file.path] = file
            return file
        else:
            return None

    def remove_file(self, file : File) -> None:
        del self.__by_id[file.id]
        del self.__by_path[file.path]

    def file_exists_at_path(self, path : str) -> bool:
        return path in self.__by_path

    def by_id(self, file_id) -> Optional[File]:
        if file_id in self.__by_id:
            return self.__by_id[file_id]
        else:
            return None
    
    def by_path(self, path) -> File:
        if path in self.__by_path:
            return self.__by_path[path]
        else:
            raise BaseException("Looking up unknown file")

    def print(self) -> None:
        for path, _f in sorted(self.__by_path.items()):
            print(path)

