from core.apps.class_based_app_with_werzeug import App
from core.middlewares.middleware import FirstMiddleware , SecondMiddleware, ServeStaticMiddleware
from core.templates.templates import HttpResponse , TextResponse

app = App()

@app.route("/" , methods=["GET"])
def index(request):
    return HttpResponse(template_name="index.html",templates_dir="static/templates" , context={'name': 'World !'} , status=200)

@app.route("/contact")
def contact(request):
    return TextResponse("contact us !" , status=200)

@app.route("/katibe/<string:slug>")
def katibe(request , slug):
    return TextResponse(f"katibe {slug}!" , status=200)



app.middleware.add(FirstMiddleware)
app.middleware.add(ServeStaticMiddleware)
app.middleware.add(SecondMiddleware)
app.run(app=app)