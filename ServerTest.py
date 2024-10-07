from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/":
            self.path = "/index.html"

        # Ignore favicon requests
        if self.path == "/favicon.ico":
            self.send_response(204)  # No content
            self.end_headers()
            return

        try:
            file_path = os.path.join(os.getcwd(), "Static", self.path.lstrip("/"))  # Updated to "Static"
            file_ext = os.path.splitext(self.path)[1]

            if file_ext == ".html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
            elif file_ext == ".css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
            elif file_ext == ".js":
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")

            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", "utf-8"))
            print(f"File not found: {file_path}")  # Log the missing file


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
