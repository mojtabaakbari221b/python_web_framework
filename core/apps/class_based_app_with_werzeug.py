from werkzeug.routing import Rule , Map
from werkzeug.exceptions import NotFound, HTTPException, MethodNotAllowed
import inspect
from ..middlewares.middleware import BaseMiddleware
from ..templates.templates import TextResponse
from werkzeug.middleware.shared_data import SharedDataMiddleware
import os
from .. import settings

class App():
    def __init__(self):
        self.mapper = {}
        self.map = Map()
        self.middleware = BaseMiddleware(self)
    
    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)

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

    def serve_static(self):
        if settings.STATIC_PATH is not None or len(settings.STATIC_PATH.strip()) != 0:
            self.middleware = SharedDataMiddleware(self.middleware, {
                    settings.STATIC_URL: os.path.join(os.path.dirname(settings.BASE_DIR), settings.STATIC_PATH),
                })
        else :
            raise ValueError("you should set valid value for STATIC_PATH in setting.py")
        
