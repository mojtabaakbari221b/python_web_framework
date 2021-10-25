from class_based_app_with_werzeug import AppResponse , App
from middleware import BaseMiddleware

app = App()

@app.route("/" , methods=["GET"])
def index(request):
    return AppResponse("index !" , status=200)

@app.route("/contact")
def contact(request):
    return AppResponse("contact us !" , status=200)

@app.route("/katibe/<string:slug>")
def katibe(request , slug):
    return AppResponse(f"katibe {slug}!" , status=200)

class FirstMiddleware(BaseMiddleware):
    def process_request(self, req):
        print(f"{__class__.__name__} Processing request", req.url)

    def process_response(self, req, res):
        print(f"{__class__.__name__} Processing response", req.url)

class SecondMiddleware(BaseMiddleware):
    def process_request(self, req):
        print(f"{__class__.__name__} Processing request", req.url)

    def process_response(self, req, res):
        print(f"{__class__.__name__} Processing response", req.url)

app.middleware.add(SecondMiddleware)
app.add_middleware(FirstMiddleware)