from class_based_app_with_werzeug import AppResponse , App
from middleware import BaseMiddleware

app = App()

@app.route("/detail" , methods=["POST" , "GET", "PUT"])
class DetailView():
    def get(self , request):
        return AppResponse(f"detail in {request.method} method !" , status=200)
    
    def post(self , request):
        return AppResponse(f"detail in {request.method} method !" , status=200)