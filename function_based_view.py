from jinja2.environment import Template
from class_based_app_with_werzeug import App
from middleware import BaseMiddleware
# from core.templates import HttpResponse
from templates import HttpResponse , TextResponse


app = App()

@app.route("/" , methods=["GET"])
def index(request):
    return HttpResponse(template_name="index.html",templates_dir="paper/templates" , context={'name': 'mojtaba'} , status=200)

@app.route("/contact")
def contact(request):
    return TextResponse("contact us !" , status=200)

@app.route("/katibe/<string:slug>")
def katibe(request , slug):
    return TextResponse(f"katibe {slug}!" , status=200)

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
app.serve_static(static_path="paper/static")