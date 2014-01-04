

import os
import jinja2
import webapp2
import logging

from security import Root


# TEMPLATE DIRECTORY CONFIGURATIONS FOR ERROR PAGES
error_dir    = os.path.join(os.path.dirname(__file__), '../templates')
error_env    = jinja2.Environment(loader = jinja2.FileSystemLoader(error_dir), autoescape = True)

class Handler(webapp2.RequestHandler):

    def w(cls,*a, **kw):
        Handler.response.out.write(*a, **kw)
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = error_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))




def handle_500(request, response, exception):
    response.set_status(500)
    tmp = Handler()
    tmp.response = response
    logging.exception(exception)
    tmp.render('error_pages/500.html')


