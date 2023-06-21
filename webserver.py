# author manfred scheucher <scheucher@math.tu-berlin.de>
# based on Python 3 server example

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import generate

hostName = "localhost"
serverPort = 8080

from datetime import datetime



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>compact arxiv</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        self.wfile.write(bytes(f"date: {date}<br>", "utf-8"))

        self.wfile.write(bytes(generate.perform(), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.") 
