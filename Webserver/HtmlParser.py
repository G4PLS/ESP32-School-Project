class HtmlParser:
    @staticmethod
    def convert(request) -> dict:
        # Split the request into the request line and headers

        request_lines = request.split('\r\n')

        # Ensure there's at least one line to parse
        if not request_lines or len(request_lines[0].split(" ")) < 3:
            raise ValueError(f"Malformed request line: {request_lines[0]}")

        # Get the request line (method, path, protocol)
        method, path, protocol = HtmlParser._parse_request_line(request_lines[0])

        # Parse the headers into a dictionary
        headers = HtmlParser._parse_headers(request_lines[1:])

        # Separate the path and query parameters
        pure_path, query_params_str = HtmlParser._parse_path_and_params(path)

        # Parse query_params into a dictionary
        query_params = HtmlParser._parse_query_params(query_params_str)

        # Parse cookies into a dictionary
        cookies = HtmlParser._parse_cookies(headers.get("Cookie", ""))

        body = HtmlParser._parse_body(request_lines[1:])

        # Return the parsed result
        return {
            "protocol": protocol or "",
            "origin": headers.get("Origin", ""),
            "host": headers.get("Host", ""),
            "user_agent": headers.get("User-Agent", ""),
            "conent_length": headers.get("Content-Length", "0"),
            "accept": headers.get("Accept", ""),
            "accept_language": headers.get("Accept-Language", ""),
            "accept_encoding": headers.get("Accept-Encoding", ""),
            "dnt": headers.get("DNT", ""),
            "sec_gpc": headers.get("Sec-GPC", ""),
            "connection": headers.get("Connection", ""),
            "cookie": cookies,  # Parsed cookies as a dictionary
            "path": path,
            "pure_path": pure_path,  # Pure path without query params
            "request_type": method,
            "query_params": query_params,  # Query parameters as a dictionary
            "body": body
        }
    
    @staticmethod
    def _parse_body(request_lines):
        is_body = False
        body = ""
        for line in request_lines:
            if is_body:
                body += line

            if line.strip() == "":
                is_body = True
                continue
        return body.strip()

    @staticmethod
    def _parse_request_line(request_line: str) -> tuple:
        """Parse the request line (method, path, protocol)."""
        parts = request_line.split(" ")
        if len(parts) < 3:
            raise ValueError(f"Malformed request line: {request_line}")
        return parts[0], parts[1], parts[2]

    @staticmethod
    def _parse_headers(header_lines: list) -> dict:
        """Parse header lines into a dictionary."""
        headers = {}
        for line in header_lines:
            if line.strip() == "":
                break
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    @staticmethod
    def _parse_path_and_params(path: str) -> tuple:
        """Separate the path and query parameters."""
        if "?" in path:
            return path.split("?", 1)[0], path.split("?", 1)[1]
        else:
            return path, ""

    @staticmethod
    def _parse_query_params(query_params_str: str) -> dict:
        """Parse the query parameters into a dictionary."""
        query_params = {}
        if query_params_str:
            params = query_params_str.split("&")
            for param in params:
                if "=" in param:
                    key, value = param.split("=", 1)
                    query_params[key] = value
        return query_params

    @staticmethod
    def _parse_cookies(cookie_header: str) -> dict:
        """Parse the cookies into a dictionary."""
        cookies = {}
        if cookie_header:
            cookie_list = cookie_header.split(";")
            for cookie in cookie_list:
                cookie = cookie.strip()  # Remove any leading/trailing spaces
                if "=" in cookie:
                    cookie_name, cookie_value = cookie.split("=", 1)
                    cookies[cookie_name.strip()] = cookie_value.strip()
        return cookies
