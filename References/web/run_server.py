from http.server import HTTPServer, CGIHTTPRequestHandler

server = HTTPServer(('',8080),CGIHTTPRequestHandler)

server.serve_forever()