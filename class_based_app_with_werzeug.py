from werkzeug.wrappers import Response , Request
from werkzeug.routing import Rule , Map
from werkzeug.exceptions import NotFound, HTTPException, MethodNotAllowed
import inspect

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
            if inspect.isclass(handler):
                instance = handler()
                handler = getattr(instance, request.method.lower(), None)
                assert handler is not None, "method not exists ."
            return handler(request , **kwargs)
        except NotFound:
            return self.error_not_found()
        except MethodNotAllowed:
            return self.error_method_not_allowed(request.method)
        except HTTPException:
            return HTTPException(request)
    
    def error_not_found(self):
        return AppResponse("Page Not Found !" , status=404)

    def error_method_not_allowed(self, method):
        return AppResponse(f"method {method} not allowed!" , status=405)
    
    def check_is_exists_rule_or_handler(self, path, endpoint):
        if endpoint in self.mapper:
            return True
        for rule in self.map.iter_rules():
            if path == rule.rule :
                return True
        return False


    def route(self , path , methods=None):
        def wrapper(handler):
            endpoint = handler.__name__
            assert not self.check_is_exists_rule_or_handler(path , endpoint), f"path {path} already exists"
            rule = Rule(path , endpoint=endpoint , methods=methods)
            self.map.add(rule)
            self.mapper[handler.__name__] = handler
            return handler
        return wrapper


app = App()

@app.route("/" , methods=["GET"])
def index(request):
    return AppResponse("index !" , status=200)

@app.route("/contact")
def contact(request):
    return AppResponse("contact us !" , status=200)

@app.route("/detail" , methods=["POST" , "GET", "PUT"])
class DetailView():
    def get(self , request):
        return AppResponse(f"detail in {request.method} method !" , status=200)
    
    def post(self , request):
        return AppResponse(f"detail in {request.method} method !" , status=200)

@app.route("/katibe/<string:slug>")
def katibe(request , slug):
    return AppResponse(f"katibe {slug}!" , status=200)