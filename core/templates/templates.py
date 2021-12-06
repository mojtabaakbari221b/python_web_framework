import os
from werkzeug.wrappers import Response
from jinja2 import Environment,FileSystemLoader, select_autoescape

class TextResponse(Response):
    pass

class HttpResponse(Response):
    def __init__(self, template_name , templates_dir="templates" , context=None , status=200):
        if context is None :
            context = {}

        env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir)),
            autoescape=select_autoescape([
                'html',
                'htm',
                'xml',
            ])
        )

        template = env.get_template(template_name).render(**context)

        super(HttpResponse , self).__init__(template , status = status , content_type="text/html")
