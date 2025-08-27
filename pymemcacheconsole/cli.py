#!/usr/bin/env python3
import argparse
import socket
import sys

from .models import RetrievalCommand, StorageCommand
from .protocol import (
    deserialize_value_response,
    serialize_retrieval,
    serialize_storage,
)


def send_command(host: str, port: int, message: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode("utf-8"))
        data = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data.append(chunk.decode("utf-8"))
            if "END\r\n" in data[-1] or "STORED\r\n" in data[-1] or "NOT_STORED\r\n" in data[-1]:
                break
        return "".join(data)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pmcc",
        description="A simple Memcached client library and CLI.",
    )
    parser.add_argument("-host", "--host", "-H", dest="host", default="localhost", help="Memcached server hostname (default: localhost)")
    parser.add_argument("-p", "--port", dest="p", type=int, default=11211, help="Memcached server port (default: 11211)")
    parser.add_argument("command", choices=["set", "get", "add", "replace", "append", "prepend"], help="Command to run: set, get, add, replace, append, or prepend")
    parser.add_argument("args", nargs="*", help="Arguments for the command")

    if any(arg in ["-?", "--?"] for arg in sys.argv):
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    host = args.host
    port = args.p

    if args.command in ["set", "add", "replace", "append", "prepend"]:
        if len(args.args) < 2:
            print(f"Usage: pmcc {args.command} <key> <value>")
            sys.exit(1)
        key, value = args.args[0].rstrip("/"), args.args[1]
        cmd = StorageCommand(
            command=args.command,
            key=key,
            flags=0,
            exptime=0,
            bytes=len(value),
            value=value,
        )
        message = serialize_storage(cmd)
        response = send_command(host, port, message)
        print(response.strip())

    elif args.command == "get":
        if len(args.args) < 1:
            print("Usage: pmcc get <key>")
            sys.exit(1)
        key = args.args[0].rstrip("/")
        cmd = RetrievalCommand(keys=[key])
        message = serialize_retrieval(cmd)
        response = send_command(host, port, message)
        values = list(deserialize_value_response(response))
        if values:
            for v in values:
                print(f"{v.key} => {v.value}")
        else:
            print("(nil)")
  
if __name__ == "__main__":
    main()


