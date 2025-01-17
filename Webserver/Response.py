class Response:
    class Status:
        CONTINUE = "100 CONTINUE"
        
        OK = "200 OK"
        CREATED = "201 CREATED"
        ACCEPTED = "202 ACCEPTED"
        NO_CONTENT = "204 NO CONTENT"
        PARTIAL_CONTENT = "206 PARTIAL CONTENT"

        MOVED_PERMANANTELY = "301 MOVED PERMANENTLY"
        FOUND = "302 FOUND"
        SEE_OTHER = "303 SEE OTHER"
        NOT_MODIFIED = "304 NOT MODIFIED"
        TEMPORARY_REDIRECT = "307 TEMPORARY REDIRECT"
        PREMANENT_REDIRECT = "308 PERMANENT REDIRECT"

        BAD_REQUEST = "400 BAD REQUEST"
        UNAUTHERIZED = "401 UNAUTHERIZED"
        FORBIDDEN = "403 FORBIDDEN"
        NOT_FOUND = "404 NOT FOUND"
        METHOD_NOT_ALLOWED = "405 METHOD NOT ALLOWED"
        REQUEST_TIMEOUT = "408 REQUEST TIMEOUT"
        CONFLICT = "409 CONFLICT"
        GONE = "410 GONE"
        UNSUPPORTED_MEDIA_TYPE = "415 UNSUPPORTED MEDIA TYPE"

        INTERNAL_SERVER_ERROR = "500 INTERNAL SERVER ERROR"
        NOT_IMPLEMENTED = "501 NOT IMPLEMENTED"
        BAD_GATEWAY = "502 BAD GATEWAY"
        SERVICE_UNAVAILABLE = "503 SERVICE UNAVAILABLE"
        GATEWAY_TIMEOUT = "504 GATEWAY TIMEOUT"
        HTTP_VERSION_NOT_SUPPORTED = "505 HTTP VERSION NOT SUPPORTED"

    class Version:
        HTTP_1_0 = "HTTP/1.0"
        HTTP_1_1 = "HTTP/1.1"
        HTTP_2 = "HTTP/2"
        HTTP_3 = "HTTP/3"

    class Encoding:
        DEFLATE = "deflate"
        GZIP = "gzip"
        BROTLI = "br"
        IDENTITY = "identity"
        COMPRESS = "compress"

    class ContentType:
        HTML = "text/html"
        PLAIN = "text/plain"
        CSS = "text/css"
        JAVASCRIPT = "text/javascript"
        JSON = "application/json"
        XML = "application/XML"
        JPEG = "image/jpeg"
        PNG = "image/png"
        GIF = "image/gif"
        SVG = "image/svg+xml"
        WEBP = "image/webp"
        MP3 = "audio/mp3"
        WAV = "audio/wav"
        OGG_A = "audio/ogg"
        MIDI = "audio/midi"
        MP4 = "video/mp4"
        WEBM = "video/webm"
        OGG_V = "video/ogg"
        PDF = "application/pdf"
        MSWORD = "application/msword"
        MSEXCEL = "application/vnd.ms-excel"
        MSPOWERPOINT = "application/vnd.ms-powerpoint"
        ZIP = "application/zip"
        GZIP = "application/gzip"
        ZIP7 = "application/x-7z-compressed"
        WOFF = "font/woff"
        WOFF2 = "font/woff2"
        TTF = "font/ttf"
        OTF = "font/otf"
        BIN = "application/octet-stream"
        MUTIPART = "multipart/form-data"
        JAVASCRIPT_MODULE = "application/javascript"
        CSV = "text/csv"
        ICALENDAR = "text/calendar"
        RSS = "application/rss+xml"

    def __init__(self):
        self.http_version = Response.Version.HTTP_1_1
        self.status = Response.Status.INTERNAL_SERVER_ERROR
        self.content_type = Response.ContentType.PLAIN
        
        self.date = None
        self.server = None
        self.cookies = None
        self.content_encoding = None
        self.body = None

        self.additional_headers = []

    def set_headers(self, headers):
        self.headers = headers

    def set_content_type(self, content_type):
        self.content_type = content_type

    def set_status(self, status):
        self.status = status

    def set_body(self, body):
        self.body = body

    def set_date(self, date):
        self.date = date

    def set_server(self, server):
        self.server = server

    def set_cookies(self, cookies):
        self.cookies = cookies

    def set_content_encoding(self, content_encoding):
        self.content_encoding = content_encoding

    def build(self, calculate_content_length: bool = False):
        response = (
            f"{self.http_version} {self.status}\r\n"
            f"Content-Type: {self.content_type}\r\n"
        )

        if self.date:
            response += f"Date: {self.date}\r\n"
        if self.server:
            response += f"Server: {self.server}\r\n"
        if self.content_encoding:
            response += f"Content-Encoding: {self.content_encoding}\r\n"

        if self.cookies:
            response += f"Cookies: {self.cookies}"

        for header in self.additional_headers:
            response += f"{header}\r\n"


        if not self.body:
            return response
        
        if calculate_content_length:
            content_length = len(self.body.encode('utf-8'))
            response += f"Content-Length: {content_length}"

        response += "\r\n"

        response += self.body

        return response