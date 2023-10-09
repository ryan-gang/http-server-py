import socket
from typing import Optional

CRLF = "\r\n"


class RequestHandler:
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


def handle_request(path: str) -> str:
    req_handler = RequestHandler()

    if path == "/":
        return req_handler.create_success_response()
    elif path.startswith("/echo"):
        body = path.split("/echo/")[1]
        headers = {"Content-Type": "text/plain", "Content-Length": f"{len(body)}"}
        return req_handler.create_success_response(headers, body)
    else:
        return req_handler.create_failure_response()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print("Connected by", addr)
        data = conn.recv(1024)
        first_line, *req_headers = data.decode().split(CRLF)
        method, path, version = first_line.split(" ")
        print(handle_request(path).encode())
        conn.send(handle_request(path).encode())


if __name__ == "__main__":
    main()
