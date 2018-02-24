import webapp2
import os
import jinja2
import uuid

from google.appengine.api import users, memcache

template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        if self.request.cookies.get("sprejel-piskotek") == "DA":
            params["piskotek"] = True

        uporabnik = users.get_current_user()
        if uporabnik:
            params["url_odjave"] = users.create_logout_url("/")
        else:
            params["url_prijave"] = users.create_login_url("/")

        params["uporabnik"] = uporabnik

        params["csrf_zeton"] = str(uuid.uuid4())
        memcache.add(params["csrf_zeton"], True, 60 * 10)

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))
