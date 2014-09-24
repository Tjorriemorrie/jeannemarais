import webapp2
from src.handlers import BaseHandler
from src.settings import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images
from src.main.models import Painting
import mimetypes
from google.appengine.api import mail


class Index(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'nav': 'home',
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/index.html')
        self.response.write(template.render(template_values))


class Gallery(BaseHandler):
    def get(self, gallery):
        paintings = Painting.query(ancestor=self.parent_key).filter(Painting.gallery == gallery).fetch()
        template_values = {
            'nav': gallery,
            'paintings': paintings,
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/gallery.html')
        self.response.write(template.render(template_values))


class Admin(BaseHandler):

    def get(self):
        paintings = Painting.query(ancestor=self.parent_key).order(-Painting.updated_at).fetch()
        template_values = {
            'paintings': paintings,
            'galleries': Painting.CHOICES_GALLERIES,
            'tab': self.request.GET.get('tab', 'figures'),
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/admin.html')
        self.response.write(template.render(template_values))


class Form(BaseHandler):

    def get(self):
        key = self.request.GET.get('key')
        if key:
            painting = ndb.Key(urlsafe=key).get()
        else:
            painting = Painting()
        template_values = {
            'galleries': Painting.CHOICES_GALLERIES,
            'painting': painting,
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/form.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        key = self.request.GET.get('key')
        if key:
            painting = ndb.Key(urlsafe=key).get()
        else:
            painting = Painting(parent=self.parent_key)
            image_upload = self.request.POST.get('image')
            image_name = image_upload.filename
            painting.image = image_upload.file.read()
            painting.image_name = image_name

        painting.gallery = str(self.request.POST.get('gallery'))
        painting.name = self.request.POST.get('name')
        painting.description = self.request.POST.get('description')
        painting.price = int(self.request.POST.get('price'))
        painting.special = bool(self.request.POST.get('special'))
        painting.sold = bool(self.request.POST.get('sold'))
        painting.copy = bool(self.request.POST.get('copy'))
        painting.copy_price = int(self.request.POST.get('copy_price'))
        painting.put()
        self.redirect('/admin?tab=%s' % painting.gallery)


class Image(BaseHandler):

    def get(self, key):
        painting = ndb.Key(urlsafe=key).get()
        if painting.image:
            # img = images.Image(painting.image)
            # img.resize(
            #     width=int(self.request.GET.get('w', 32)),
            #     height=int(self.request.GET.get('h', 32)),
            # )
            # # img.im_feeling_lucky()
            # jpg = img.execute_transforms(output_encoding=images.JPEG)
            # self.response.headers['Content-Type'] = 'image/jpeg'
            # self.response.out.write(jpg)
            self.response.headers[b'Content-Type'] = mimetypes.guess_type(painting.image_name)[0]
            self.response.write(painting.image)
        else:
            self.error(404)


class Delete(BaseHandler):
    def get(self):
        key = self.request.GET.get('key')
        if key:
            ndb.Key(urlsafe=key).delete()
        tab = self.request.GET.get('tab', 'figures')
        self.redirect('/admin?tab=%s' % tab)


class ContactMe(BaseHandler):
    def get(self):
        template_values = {
            'nav': 'contactme',
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/contactme.html')
        self.response.write(template.render(template_values))


class AboutMe(BaseHandler):
    def get(self):
        template_values = {
            'nav': 'aboutme',
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/aboutme.html')
        self.response.write(template.render(template_values))


class Available(BaseHandler):
    def get(self):
        paintings = Painting.query(ancestor=self.parent_key).fetch()
        specials = [painting for painting in paintings if painting.special]
        originals = [painting for painting in paintings if (not painting.special and not painting.sold)]
        prints = [painting for painting in paintings if (not painting.special and painting.copy)]
        template_values = {
            'nav': 'available',
            'specials': specials,
            'originals': originals,
            'prints': prints,
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/available.html')
        self.response.write(template.render(template_values))

    def post(self):
        post = self.request.POST
        painting = ndb.Key(urlsafe=post.get('painting_id')).get()
        mail.send_mail_to_admins(
            sender="{0} <{1}>".format(post.get('name'), post.get('email')),
            subject="Painting requested",
            body="""
                Dear Jeanne:

                I'm interested in your painting: {0}

                {1}
                {2}
            """.format(painting.name, post.get('name'), post.get('number'))
        )
        self.response.status = '200 OK'
