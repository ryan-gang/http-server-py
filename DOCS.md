# README.md

A multi-threaded toy http-server written in Python, capable of serving
concurrent clients. Part of the Codecrafters series.

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

## Stage 4 : Respond with content

- Parse request content, return part of it in response.

Ref : https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages

## Stage 5 : Parse Headers

- Parse Headers, put into a `dict[str, str]`.

## Stage 6 : Concurrent connections

- Server needs to be able to handle multiple clients simultaneously. Easy way to
  do that is to spin off new threads for every new request. But its not very
  sustainable.  
  Alternatives might be Thread pools, multiprocessing, event loop, async.  
  Ref : https://stackoverflow.com/questions/23828264

- For local testing, use `ncat` to hold a persistent conn, then use another
  client like `httpie` or `curl`.  
  Ref : https://nmap.org/ncat/

## Stage 7 : Get File

- Return file contents in the body of the response.

## Stage 8 : Post File

- Put request body into a file.
