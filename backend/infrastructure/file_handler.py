import os
from domain.ports.file_handling_port import FileHandlingPort

class LocalFileHandler(FileHandlingPort):
    def exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)

    def get_file_size(self, file_path: str) -> int:
        return os.path.getsize(file_path)

    def read_file(self, file_path: str, offset: int = 0, size: int = -1) -> bytes:
        with open(file_path, "rb") as f:
            f.seek(offset)
            return f.read(size)

    def write_file(self, file_path: str, data: bytes) -> None:
        with open(file_path, "wb") as f:
            f.write(data)

    def append_text_line(self, file_path: str, text: str) -> None:
        data = (text + "\n").encode("utf-8")
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "ab") as f:
            f.write(data)
