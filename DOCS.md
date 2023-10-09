## Stage 1 : Bind to a port

Task is to start a TCP server on port 4221.

## Stage 2 : Respond with 200

- Accept a TCP connection.
- Read data from the connection.
- Respond with `HTTP/1.1 200 OK\r\n\r\n` (there are two `\r\n`s at the end)

Ref : https://docs.python.org/3/library/socket.html#example

## Stage 3 : Respond with 404

- Read data from the connection.
- Parse request contents and headers.
- Based on contents, return 200 / 404.

## Stage 4 : Respond with 404

- Parse request content, return part of it in response.

Ref : https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
