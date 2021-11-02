from webob import Response , Request
from templates import AppResponse

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
        return AppResponse("Page Not Found !" , status=404)

    def route(self , path):
        def wrapper(handler):
            self.mapper[path] = handler
            return handler
        return wrapper


app = App()

@app.route("/")
def index():
    return AppResponse("index !" , status=200)

@app.route("/contact")
def contact():
    return AppResponse("contact us !" , status=200)
