from werkzeug.wrappers import Request
from werkzeug.middleware.shared_data import SharedDataMiddleware

class ServeStaticMiddleware(SharedDataMiddleware):
    def add(self , middleware_cls ):
        self.app = middleware_cls(self.app)

    def __call__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        request = Request(environ)
        response = self.app.request_dispatcher(request)
        return response(environ, start_response)
    
    def request_dispatcher(self , request):
        response = self.app.request_dispatcher(request)
        super().__call__(self.environ , self.start_response)
        return response

class BaseMiddleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.request_dispatcher(request)
        return response(environ, start_response)

    def request_dispatcher(self , request):
        self.process_request(request)
        response = self.app.request_dispatcher(request)
        self.process_response(request, response)

        return response
    
    def process_request(self, request):
        print("im processing the request")

    def process_response(self, request, response):
        print("im processing the response")
        return response

    def add(self, middleware_cls):
        if middleware_cls == ServeStaticMiddleware :
            self.app = middleware_cls(self.app, {
                "/static" : "/home/mojtaba/w/projects/python_web_framework/paper/static",
            })
        else :
            self.app = middleware_cls(self.app)