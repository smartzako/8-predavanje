import cgi

from google.appengine.api import users, memcache

from handlers.base_handler import BaseHandler
from models.models import Objava, Komentar


class DodajObjavoHandler(BaseHandler):
    def get(self):
        return self.render_template("dodaj_objavo.html")

    def post(self):
        vrednost_csrf = self.request.get("csrf-zeton")

        if not memcache.get(vrednost_csrf):
            return self.write("CSRF napad v dogajanju.")

        naslov = cgi.escape(self.request.get("title"))
        vsebina = cgi.escape(self.request.get("text"))
        uporabnik = users.get_current_user()
        email = uporabnik.email()
        nova_objava = Objava(naslov=naslov,
                             vsebina=vsebina,
                             uporabnik_email=email)
        nova_objava.put()
        return self.write("Objava dodana.")


class PreglejObjaveHandler(BaseHandler):
    def get(self):
        objave = Objava.query().order(-Objava.cas_objave).fetch()
        params = {
            "objave": objave
        }
        return self.render_template("preglej_objave.html", params)


class PreglejObjavoHandler(BaseHandler):
    def get(self, objava_id):
        objava = Objava.get_by_id(int(objava_id))
        if not objava:
            return self.write('Te objave ni.')
        komentarji = Komentar.query(Komentar.objava_id == str(objava.key.id())).order(-Komentar.cas_objave).fetch()
        params = {
            "objava": objava,
            "komentarji": komentarji,
        }
        return self.render_template("preglej_objavo.html", params)

    def post(self, objava_id):
        vrednost_csrf = self.request.get("csrf-zeton")

        if not memcache.get(vrednost_csrf):
            return self.write("CSRF napad v dogajanju.")

        vsebina = cgi.escape(self.request.get("text"))
        Komentar.shrani_komentar(objava_id, vsebina)



        return self.write("Komentar dodan.")


