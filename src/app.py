import webapp2
from settings import *
from src.main import main


wsgi = webapp2.WSGIApplication(
    [
        ('/', main.IndexPage),
    ],
    debug=DEBUG,
    config=CONFIG
)