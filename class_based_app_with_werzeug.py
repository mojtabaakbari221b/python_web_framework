from werkzeug.wrappers import Response , Request
from werkzeug.routing import Rule , Map
from werkzeug.exceptions import NotFound, HTTPException


class AppResponse(Response):
    pass

class App():
    def __init__(self):
        self.mapper = {}
        self.map = Map()
    
    def __call__(self, environ , start_response):
        return self.handle_request(environ, start_response)
    
    def handle_request(self, environ,start_response):
        request = Request(environ)
        response = self.request_dispatcher(request)
        return response(environ, start_response)

    def request_dispatcher(self, request):
        adapter = self.map.bind_to_environ(request.environ)
        try:
            endpoint , kwargs = adapter.match()
            handler = self.mapper[endpoint]
            return handler(request , **kwargs)
        except NotFound:
            return self.error_not_found()
        except HTTPException:
            return HTTPException(request)
    
    def error_not_found(self):
        return AppResponse("Page Not Found !" , status=404)

    def route(self , path):
        def wrapper(handler):
            endpoint = handler.__name__
            rule = Rule(path , endpoint=endpoint)
            self.map.add(rule)
            self.mapper[handler.__name__] = handler
            return handler
        return wrapper


app = App()

@app.route("/")
def index(request):
    return AppResponse("index !" , status=200)

@app.route("/contact")
def contact(request):
    return AppResponse("contact us !" , status=200)

@app.route("/katibe/<string:slug>")
def katibe(request , slug):
    return AppResponse(f"katibe {slug}!" , status=200)