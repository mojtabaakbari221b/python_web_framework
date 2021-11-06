from class_based_app_with_werzeug import App
from middleware import BaseMiddleware
from templates import TextResponse

app = App()
app.serve_static(static_path="paper/static")

@app.route("/detail" , methods=["POST" , "GET", "PUT"])
class DetailView():
    def get(self , request):
        return TextResponse(f"detail in {request.method} method !" , status=200)
    
    def post(self , request):
        return TextResponse(f"detail in {request.method} method !" , status=200)