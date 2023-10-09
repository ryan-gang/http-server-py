## Stage 1 : Bind to a port

Task is to start a TCP server on port 4221.

## Stage 2 : Respond with 200

- Accept a TCP connection
- Read data from the connection (we'll get to parsing it in later stages)
- Respond with `HTTP/1.1 200 OK\r\n\r\n` (there are two `\r\n`s at the end)

Ref : https://docs.python.org/3/library/socket.html#example
