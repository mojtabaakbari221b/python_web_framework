import re
from webob import Response , Request, response

class App():
    def __init__(self):
        self.mapper = {}
    
    def __call__(self, environ , start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)


    def handle_request(self, request):
        for path , handler in self.mapper.items():
            if path == request.path :
                response = handler()
                return response
        response = self.default_response()
        return response

    def default_response(self):
        response = Response()
        response.status = 404
        response.text = "Page Not Found !"
        return response

    def route(self , path):
        def wrapper(handler):
            print(path)
            self.mapper[path] = handler
            return handler
        return wrapper


app = App()

@app.route("/")
def index():
    response = Response()
    response.status = 404
    response.text = "inedx !"
    return response

@app.route("/contact")
def contact():
    response = Response()
    response.status = 404
    response.text = "contact us !"
    return response