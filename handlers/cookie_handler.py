from handlers.base_handler import BaseHandler


class CookieHandler(BaseHandler):
    def post(self):
        self.response.set_cookie("sprejel-piskotek", "DA")
        return self.write("POST zahteva na CookieHandler")
