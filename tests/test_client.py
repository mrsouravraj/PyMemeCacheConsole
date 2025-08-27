import socket
import threading
import time

from pymemecacheconsole.client import MemcachedClient


def start_fake_server(responses, host="localhost", port=11212):
    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((host, port))
            srv.listen(1)
            conn, _ = srv.accept()
            with conn:
                _ = conn.recv(4096)
                conn.sendall(responses.pop(0).encode("utf-8"))

    th = threading.Thread(target=server, daemon=True)
    th.start()


def test_client_set_and_get():
    # Fake responses: one for set, one for get
    responses = ["STORED\r\n", "VALUE foo 0 3\r\nbar\r\nEND\r\n"]
    start_fake_server(responses.copy())
    time.sleep(0.05)

    client = MemcachedClient(host="localhost", port=11212)
    assert client.set("foo", "bar") is True

    # Start server for get
    start_fake_server(responses[1:])
    time.sleep(0.05)
    assert client.get("foo") == "bar"


