import os
import socket
import sys
import threading

from RequestHandler import RequestHandler
from ResponseHandler import ResponseHandler

CRLF = "\r\n"


def fetch_response(req_handler: RequestHandler, args: list[str]) -> str:
    # Generates response for every request.
    # Calling ResponseHandler() as required.
    resp_handler = ResponseHandler()
    method, path, _ = req_handler.get_status_line()
    headers = req_handler.get_headers()
    body = req_handler.get_body()

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
            if method == "GET":
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

            elif method == "POST":
                file_name = path.split("/files/")[1]
                file_path = os.path.join(directory, file_name)
                file_contents = body
                with open(file_path, "w") as f:
                    f.write(file_contents)
                return resp_handler.create_created_response(body=file_contents)

    return resp_handler.create_failure_response()


def handle_request(conn: socket.socket, addr: socket.AddressFamily, args: list[str]):
    # This func runs in every new thread, parsing the request, creating a response
    # Sending it out, closing connection and closing thread.
    size = 1024
    with conn:
        print("Connected by", addr)
        try:
            request = conn.recv(size)
            if not request:
                raise Exception("Client disconnected.")
            req_handler = RequestHandler(request)
            response = fetch_response(req_handler, args).encode()
            # print(request, response)
            conn.send(response)
        except Exception:
            return


def main():
    args = sys.argv
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    print("Started Server.")
    while True:
        conn, addr = server_socket.accept()
        conn.settimeout(30)  # Set timeout for connection to 30 seconds.
        # Spin out a new thread to process this request, return control back to main thread.
        threading.Thread(target=handle_request, args=(conn, addr, args)).start()


if __name__ == "__main__":
    main()
