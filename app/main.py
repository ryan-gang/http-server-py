import socket

CRLF = "\r\n"
success_response = "HTTP/1.1 200 OK\r\n\r\n"
failure_response = "HTTP/1.1 404 Not Found\r\n\r\n"


def handle_request(path: str) -> str:
    if path == "/":
        return success_response
    else:
        return failure_response


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print("Connected by", addr)
        data = conn.recv(1024)
        first_line, *req_headers = data.decode().split(CRLF)
        method, path, version = first_line.split(" ")
        conn.send(handle_request(path).encode())


if __name__ == "__main__":
    main()
