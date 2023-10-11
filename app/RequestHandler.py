CRLF = "\r\n"


class RequestHandler:
    """
    Parses the incoming request, gets the body, headers, method, path and version.
    Stores the values in instance variables. Returns as required.
    Stateful.
    """

    def __init__(self, request: bytes) -> None:
        self._parse_request(request)

    def _parse_request(self, request: bytes) -> None:
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
