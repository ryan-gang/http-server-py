import socket
from RequestHandler import RequestHandler
from ResponseHandler import ResponseHandler

CRLF = "\r\n"


def handle_request(path: str) -> str:
    resp_handler = ResponseHandler()

    if path == "/":
        return resp_handler.create_success_response()
    elif path.startswith("/echo"):
        body = path.split("/echo/")[1]
        headers = {"Content-Type": "text/plain", "Content-Length": f"{len(body)}"}
        return resp_handler.create_success_response(headers, body)
    else:
        return resp_handler.create_failure_response()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print("Connected by", addr)
        request = conn.recv(2048)
        req_handler = RequestHandler(request)
        method, path, version = req_handler.get_status_line()
        print(handle_request(path).encode())
        conn.send(handle_request(path).encode())


if __name__ == "__main__":
    main()
