from google.appengine.ext import ndb
from google.appengine.api import users, taskqueue


class Objava(ndb.Model):
    vsebina = ndb.TextProperty()
    naslov = ndb.StringProperty()
    uporabnik_email = ndb.StringProperty()
    cas_objave = ndb.DateTimeProperty(auto_now_add=True)
    cas_posodobitve = ndb.DateTimeProperty(auto_now=True)
    cas_izbrisa = ndb.DateTimeProperty()


class Komentar(ndb.Model):
    objava_id = ndb.StringProperty()
    vsebina = ndb.TextProperty()
    uporabnik_email = ndb.StringProperty()
    cas_objave = ndb.DateTimeProperty(auto_now_add=True)
    cas_posodobitve = ndb.DateTimeProperty(auto_now=True)
    cas_izbrisa = ndb.DateTimeProperty()

    @staticmethod
    def shrani_komentar(objava_id, vsebina):
        uporabnik = users.get_current_user()
        email = uporabnik.email()
        nov_komentar = Komentar(vsebina=vsebina,
                                uporabnik_email=email,
                                objava_id=objava_id)
        nov_komentar.put()

        objava =  Objava.get_by_id(int(objava_id))
        taskqueue.add(url='/task/send-comment-mail',
                      params={
                          "email_avtorja_objave": objava.uporabnik_email,
                          "email_avtorja_komentarja": email
                      })
