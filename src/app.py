import webapp2
from settings import *
from src.main import main


wsgi = webapp2.WSGIApplication(
    [
        webapp2.Route(r'/admin', name='admin', handler=main.Admin),
        webapp2.Route(r'/admin/form', name='form', handler=main.Form),
        webapp2.Route(r'/admin/delete', name='delete', handler=main.Delete),
        webapp2.Route(r'/img/<key:(.*)>', name='image', handler=main.Image),
        webapp2.Route(r'/contact/me', name='contactme', handler=main.ContactMe),
        webapp2.Route(r'/about/me', name='aboutme', handler=main.AboutMe),
        webapp2.Route(r'/available', name='available', handler=main.Available),
        webapp2.Route(r'/gallery/<gallery:[a-z]+>', name='gallery', handler=main.Gallery),
        webapp2.Route(r'/', name='home', handler=main.Index),
    ],
    debug=DEBUG,
    config=CONFIG
)