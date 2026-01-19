from typing import Protocol

class FileHandlingPort(Protocol):
    def exists(self, file_path: str) -> bool:
        ...

    def get_file_size(self, file_path: str) -> int:
        ...

    def read_file(self, file_path: str, offset: int = 0, size: int = -1) -> bytes:
        ...

    def write_file(self, file_path: str, data: bytes) -> None:
        ...

    def append_text_line(self, file_path: str, text: str) -> None:
        ...
