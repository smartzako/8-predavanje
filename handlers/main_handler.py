from handlers.base_handler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")
