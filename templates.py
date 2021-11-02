from werkzeug.wrappers import Response
from jinja2 import Environment, PackageLoader, select_autoescape

class AppResponse(Response):
    pass

class HttpResponse(Response):
    def __init__(self, path , context):
        self.path = path
        self.context = context
        env = Environment(
            loader=PackageLoader('paper', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template(self.path)
        template = template.render(self.context)
        self.template = template

    def __call__(self):
        print(self.template)
        return self.template
