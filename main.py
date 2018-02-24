#!/usr/bin/env python

import webapp2

from handlers.cookie_handler import CookieHandler
from handlers.main_handler import MainHandler
from handlers.objave_handler import DodajObjavoHandler, PreglejObjaveHandler, PreglejObjavoHandler
from workers.mail_worker import MailWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/dodaj-objavo', DodajObjavoHandler),
    webapp2.Route('/preglej-objave', PreglejObjaveHandler),
    webapp2.Route('/preglej-objavo/<objava_id:\d+>', PreglejObjavoHandler),
    webapp2.Route('/task/send-comment-mail', MailWorker),
], debug=True)
