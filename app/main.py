import socket

CRLF = "\r\n"
success_response = f"HTTP/1.1 200 OK{CRLF}"
failure_response = f"HTTP/1.1 404 Not Found{CRLF}"


def create_response(path: str) -> str:
    secret = path.split("/")[-1]
    response = success_response
    response += f"Content-Type: text/plain{CRLF}"
    response += f"Content-Length: {len(secret)}{CRLF}"
    response += f"{CRLF}"  # end-headers
    response += f"{secret}{CRLF}"
    return response


def handle_request(path: str) -> str:
    if path == "/":
        return success_response
    elif path.startswith("/echo"):
        return create_response(path)
    else:
        return failure_response


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
        conn.send(handle_request(path).encode())


if __name__ == "__main__":
    main()
