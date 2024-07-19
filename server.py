from http.server import SimpleHTTPRequestHandler, HTTPServer
import subprocess
import threading
import webbrowser
import os

# Path to your Tkinter application
ECO_BOX_APP_PATH = 'eco_box_app.py'

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/open-eco-box-app':
            # Launch Tkinter application and bring it to the foreground
            if os.name == 'nt':  # For Windows
                subprocess.Popen(['python', ECO_BOX_APP_PATH], shell=True)
            else:  # For Unix-like systems
                subprocess.Popen(['python3', ECO_BOX_APP_PATH])
            
            # Respond with a simple message
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Eco Box is now open.')
        else:
            super().do_GET()

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

def open_browser():
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    # Start the server in a new thread
    server_thread = threading.Thread(target=run_server, args=(8000,))
    server_thread.daemon = True
    server_thread.start()

    # Open the web interface in the default browser
    open_browser()
