import socket
import os
from Webserver.HtmlParser import HtmlParser
from Webserver.Response import Response

class Router:
    def __init__(self, static_dir="static"):
        self._routes: dict[str, dict[str, callable]] = {}  # Routes stored by method and path
        self._static_dir = static_dir  # Directory for static files

    def add_route(self, method, path, handler):
        """Add a route for a specific HTTP method and path."""
        if method not in self._routes:
            self._routes[method] = {}
        self._routes[method][path] = handler

    def remove_route(self, method, path):
        """Remove a route by method and path."""
        if method in self._routes and path in self._routes[method]:
            del self._routes[method][path]

    def handle_request(self, method, path, query_params=None, body=None):
        """Find and execute the handler for a given method and path."""
        # Check for exact match in defined routes

        handler = self._routes.get(method, {}).get(path, None)
        
        if handler:
            if callable(handler):
                return handler(method, None, query_params, body)
            return self._serve_static_file(path)  # Serve static file if handler is a file path
        
        # Handle dynamic routes (e.g., /users/{user_id})
        for route, handler in self._routes.get(method, {}).items():
            route_parts = route.split("/")
            path_parts = path.split("/")
            
            if len(route_parts) == len(path_parts):
                path_params = {}
                match = True
                
                for i in range(len(route_parts)):
                    if route_parts[i].startswith("{") and route_parts[i].endswith("}"):
                        param_name = route_parts[i][1:-1]
                        path_params[param_name] = path_parts[i]
                    elif route_parts[i] != path_parts[i]:
                        match = False
                        break
                
                if match:
                    return handler(method, path_params, query_params, body)

        return None  # Return None if no matching handler found

    def _serve_static_file(self, path):
        """Serve a static file for a given path."""
        file_path = os.path.join(self._static_dir, path.lstrip("/"))
        try:
            with open(file_path, "r") as f:
                return f.read()  # Read the file contents and return as response
        except FileNotFoundError:
            return None  # File not found, return 404
        
    def parse_query_params(self, query_string):
        """Parse query parameters from a query string."""
        params = {}
        if query_string:
            pairs = query_string.split("&")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    params[key] = value
        return params


class Webserver:
    def __init__(self, port=80, static_dir="static"):
        self._port = port
        self._socket = None
        self.router = Router(static_dir)  # Pass static directory to router
        self._files = {}
        self._styles = {}
        
        self._load_files()

    def _load_files(self):
        """Load static files into memory (e.g., index.html)."""

        def get_file_content(file):
            # Using basic string operations to strip the extension
            file_name = file.rsplit('.', 1)[0]
            
            # Construct the full path manually
            file_path = self.router._static_dir + "/" + file

            try:
                with open(file_path, "r") as f:
                    return file_name, f.read()
            except OSError as e:
                print(f"Error reading file {file_path}: {e}")
                return None, None

        for file in os.listdir(self.router._static_dir):  # Now using self.router._static_dir
            if file.endswith(".html"):
                name, content = get_file_content(file)
                if not name or not content:
                    continue

                self._files[name] = content
            elif file.endswith(".css"):
                name, content = get_file_content(file)
                if not name or not content:
                    continue
                
                self._styles[name] = content
            else:
                continue
            
        print(f"Files: {self._files.keys()}")
        print(f"Styles: {self._styles.keys()}")


    def start(self):
        """Start the web server."""
        print("STARTING WEBSERVER")
        if self._socket is not None:
            return

        addr = socket.getaddrinfo("0.0.0.0", self._port)[0][-1]
        self._socket = socket.socket()

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(addr)

        self._socket.listen(1)

        print(f"Webserver Listening on {addr}")
        self._connection_handling()

    def _connection_handling(self):
        """Handle incoming connections."""
        print("HANDLING CONNECTIONS")
        while True:
            client, addr = self._socket.accept()
            print(f"Client connected from {addr}")

            buffer_size = 1024

            request = b''
            while True:
                data = client.recv(buffer_size)
                request += data
                if not data or len(data) < buffer_size:
                    break

            req_str = request.decode()

            # Use HtmlParser to convert the request to a dictionary
            html_data = HtmlParser.convert(req_str)

            method = html_data['request_type']
            path = html_data['pure_path']
            query_params = html_data.get('query_params', {})
            body = html_data.get("body", None)

            # Try to find a handler for the request
            response = self.router.handle_request(method, path, query_params=query_params, body=body)

            if not response:
                response = Response()
                response.set_status(Response.Status.INTERNAL_SERVER_ERROR)
                response.set_content_type(Response.ContentType.HTML)

            response_data = response.build().encode()

            client.send(response_data)

            client.close()

    def set_routing(self, routing):
        """Set up the routes for the webserver."""
        self.router = routing
