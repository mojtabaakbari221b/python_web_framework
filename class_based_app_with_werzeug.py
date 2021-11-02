from werkzeug.wrappers import Response , Request
from werkzeug.routing import Rule , Map
from werkzeug.exceptions import NotFound, HTTPException, MethodNotAllowed
import inspect
from middleware import BaseMiddleware
from templates import TextResponse

class App():
    def __init__(self):
        self.mapper = {}
        self.map = Map()
        self.middleware = BaseMiddleware(self)
    
    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)

    # def __call__(self, environ , start_response):
    #     return self.handle_request(environ, start_response)
    
    # def handle_request(self, environ,start_response):
    #     request = Request(environ)
    #     response = self.request_dispatcher(request)
    #     return response(environ, start_response)

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
        return TextResponse("Page Not Found !" , status=404)

    def error_method_not_allowed(self, method):
        return TextResponse(f"method {method} not allowed!" , status=405)
    
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
    

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
