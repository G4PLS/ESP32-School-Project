from Webserver import Webserver
#from Webserver import AccessPoint
from Webserver.Response import Response

def check_handler(method, path_params, query_params, body):
    response = Response()
    response.set_status(Response.Status.OK)
    response.set_content_type(Response.ContentType.HTML)

    name = path_params.get("name", "Stranger")
    age = path_params.get("age", 0)

    response.set_body(f"<h1>Hello, {name}! Youre {age}</h1>")
    return response

#a = AccessPoint.AccessPoint("ESP32", "")
x = Webserver.Webserver()

def handle_index(*args):
    response = Response()
    response.set_status(Response.Status.OK)
    response.set_content_type(Response.ContentType.HTML)
    response.set_body(x._files.get("index", ""))
    return response

def handle_about(*args):
    response = Response()
    response.set_status(Response.Status.OK)
    response.set_content_type(Response.ContentType.HTML)
    response.set_body(x._files.get("about", ""))
    return response

def handle_style(method, path_params, query_params, body):
    response = Response()
    response.set_content_type(Response.ContentType.CSS)
    response.set_status(Response.Status.OK)

    style_name = path_params.get("style_name", None)

    if not style_name:
        response.set_status(Response.Status.INTERNAL_SERVER_ERROR)
        response.set_body(None)
        return response
    
    style_name = style_name.split(".")[0]

    response.set_body(x._styles.get(style_name, ""))
    return response

x.router.add_route("GET", "/static/css/{style_name}", handle_style)
x.router.add_route("GET", "/", handle_index)
x.router.add_route("GET", "/about", handle_about)

#a.start()
x.start()