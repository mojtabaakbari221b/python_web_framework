import os
from werkzeug.wrappers import Request
from werkzeug.middleware.shared_data import SharedDataMiddleware
from .. import settings

class ServeStaticMiddleware(SharedDataMiddleware):
    def add(self , middleware_cls ):
        self.app = middleware_cls(self.app)

    def __call__(self):
        app = self
        try :
            while app.app :
                app = app.app
        except :
            app.serve_static()
    
    def request_dispatcher(self , request):
        response = self.app.request_dispatcher(request)
        self.__call__()
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
            if settings.STATIC_URL is not None or len(settings.STATIC_URL.strip()) != 0:
                static_url = settings.STATIC_URL
            else :
                static_url = "/static"
            if settings.STATIC_PATH is not None and len(settings.STATIC_PATH.strip()) != 0:
                self.app = middleware_cls(self.app, {
                        static_url : os.path.join(os.path.dirname(settings.BASE_DIR), settings.STATIC_PATH),
                    })
            else :
                raise ValueError("you should set valid value for STATIC_PATH in setting.py")
        else :
            self.app = middleware_cls(self.app)