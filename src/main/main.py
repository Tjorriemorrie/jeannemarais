import webapp2
from src.settings import JINJA_ENVIRONMENT
from google.appengine.ext import ndb


class IndexPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('main/templates/index.html')
        self.response.write(template.render(template_values))


