import socket
from typing import Optional
import threading
import sys
import os

CRLF = "\r\n"


class ResponseHandler:
    # Stateless.
    http_ver = "HTTP/1.1"
    success_code = "200"
    success_text = "OK"
    failure_code = "404"
    failure_text = "Not Found"

    def create_status_line(self, http_ver: str, code: str, text: str) -> str:
        return f"{http_ver} {code} {text}"

    def end_status_line(self, status_line: str) -> str:
        return status_line + CRLF

    def create_response_headers(self, headers: dict[str, str]) -> str:
        if not headers:
            return ""
        headers_str: list[str] = []
        for key in headers:
            val = headers[key]
            str_repr = f"{key}: {val}"
            headers_str.append(str_repr)
        return f"{CRLF}".join(headers_str) + CRLF

    def end_response_headers(self, response_headers: str) -> str:
        return response_headers + CRLF

    def create_response(
        self, http_ver: str, code: str, text: str, headers: dict[str, str], body: Optional[str]
    ) -> str:
        status_line = self.create_status_line(http_ver, code, text)
        status_line = self.end_status_line(status_line)
        response_headers = self.create_response_headers(headers)
        response_headers = self.end_response_headers(response_headers)

        resp = status_line + response_headers
        if body:
            resp += body
            resp = self.end_response(resp)
        return resp

    def create_success_response(
        self, headers: dict[str, str] = {}, body: Optional[str] = None
    ) -> str:
        return self.create_response(
            self.http_ver, self.success_code, self.success_text, headers, body
        )

    def create_failure_response(
        self, headers: dict[str, str] = {}, body: Optional[str] = None
    ) -> str:
        return self.create_response(
            self.http_ver, self.failure_code, self.failure_text, headers, body
        )

    def end_response(self, response: str) -> str:
        return response + CRLF


class RequestHandler:
    # Stateful.
    def __init__(self, request: bytes) -> None:
        self.parse_request(request)

    def parse_request(self, request: bytes) -> None:
        req, self.body = request.decode().split(CRLF * 2)
        status_line, *headers_str = req.split(CRLF)
        self.method, self.path, self.version = status_line.split(" ")
        self.headers: dict[str, str] = {}
        for string in headers_str:
            key, val = string.split(": ")
            self.headers[key] = val

    def get_body(self) -> str:
        return self.body

    def get_headers(self) -> dict[str, str]:
        return self.headers

    def get_status_line(self) -> tuple[str, str, str]:
        return self.method, self.path, self.version


def fetch_response(req_handler: RequestHandler, args: list[str]) -> str:
    resp_handler = ResponseHandler()
    _, path, _ = req_handler.get_status_line()
    headers = req_handler.get_headers()

    if path == "/":
        return resp_handler.create_success_response()
    elif path.startswith("/echo"):
        query_param = path.split("/echo/")[1]
        headers = {"Content-Type": "text/plain", "Content-Length": f"{len(query_param)}"}
        return resp_handler.create_success_response(headers, query_param)
    elif path == "/user-agent":
        ua = headers["User-Agent"]
        headers = {"Content-Type": "text/plain", "Content-Length": f"{len(ua)}"}
        return resp_handler.create_success_response(headers, body=ua)
    elif len(args) > 1:
        flag, directory = args[1], args[2]
        if flag == "--directory":
            file = path.split("/files/")[1]
            all_files = os.listdir(directory)
            if file in all_files:
                file_path, file_contents = os.path.join(directory, file), ""
                with open(file_path, "r") as f:
                    file_contents = f.read()
                headers = {
                    "Content-Type": "application/octet-stream",
                    "Content-Length": f"{len(file_contents)}",
                }
                return resp_handler.create_success_response(headers, body=file_contents)
    return resp_handler.create_failure_response()


def handle_request(conn: socket.socket, addr: socket.AddressFamily, args: list[str]):
    size = 1024
    with conn:
        print("Connected by", addr)
        try:
            request = conn.recv(size)
            if not request:
                raise Exception("Client disconnected.")
            req_handler = RequestHandler(request)
            response = fetch_response(req_handler, args).encode()
            print(request, response)
            conn.send(response)
        except Exception:
            return


def main():
    args = sys.argv
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    print("Started Server.")
    while True:
        conn, addr = server_socket.accept()
        conn.settimeout(30)
        threading.Thread(target=handle_request, args=(conn, addr, args)).start()


if __name__ == "__main__":
    main()
