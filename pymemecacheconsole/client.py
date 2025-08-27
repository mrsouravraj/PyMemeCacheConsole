import socket
from typing import Optional

from .models import RetrievalCommand, StorageCommand
from .protocol import (
    deserialize_value_response,
    serialize_retrieval,
    serialize_storage,
)


class MemcachedClient:
    def __init__(self, host: str = "localhost", port: int = 11211) -> None:
        self.host = host
        self.port = port

    def _send(self, message: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(message.encode("utf-8"))
            chunks = []
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                text = chunk.decode("utf-8")
                chunks.append(text)
                if (
                    "END\r\n" in text
                    or "STORED\r\n" in text
                    or "NOT_STORED\r\n" in text
                ):
                    break
            return "".join(chunks)

    def set(self, key: str, value: str, flags: int = 0, exptime: int = 0) -> bool:
        cmd = StorageCommand(
            command="set",
            key=key,
            flags=flags,
            exptime=exptime,
            bytes=len(value),
            value=value,
        )
        message = serialize_storage(cmd)
        response = self._send(message)
        return response.strip().startswith("STORED")

    def get(self, key: str) -> Optional[str]:
        cmd = RetrievalCommand(keys=[key])
        message = serialize_retrieval(cmd)
        response = self._send(message)
        values = list(deserialize_value_response(response))
        if values:
            return values[0].value
        return None


