from google.appengine.api import mail

from handlers.base_handler import BaseHandler


class MailWorker(BaseHandler):
    def post(self):
        email_avtorja_objave = self.request.get("email_avtorja_objave")
        email_avtorja_komentarja = self.request.get("email_avtorja_komentarja")

        mail.send_mail("info@ninjaforum.si",
                       email_avtorja_objave,
                       "Prisel nov komentar",
                       "<b>%s</b> je v tvoji temi napisal nov komentar." % email_avtorja_komentarja)
