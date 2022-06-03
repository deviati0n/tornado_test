import os

import tornado
from tornado.ioloop import IOLoop
from tornado.web import Application

from database.data_class import DataFunction
from database.user_class import UserFunction
from utils.context import ProjectContext

context = ProjectContext()
user_func = UserFunction()
data_func = DataFunction()


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")

    def get_current_user(self):
        return self.get_secure_cookie("user")


class DataHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_func.set_last_request(self.current_user.decode("utf-8"))

        first_filter = self.get_argument("amount", None)
        second_filter = self.get_argument("sort", None)
        amount = data_func.take_distinct_amount()

        data = data_func.receive_data(first_filter, second_filter)

        self.set_header("Content-Type", "text/html")
        self.render(
            "html/data.html",
            value=data,
            amount=amount
        )


class LogoutHadler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


class LoginHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "text/html")
        self.render("html/login.html", value="ok")

    def post(self):
        self.set_header("Content-Type", "text/html")

        if user_func.add_user(self.get_argument("login"), self.get_argument("password")):
            self.set_secure_cookie("user", self.get_argument("login"))
            self.redirect("/data")
        else:
            self.render("html/login.html", value="error")


def main():
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__)),
        cookie_secret=context.api_config.api_cookie,
        login_url='/login',
        debug=True
    )

    app = tornado.web.Application([
        (r"/", BaseHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHadler),
        (r"/data", DataHandler),
    ], **settings)

    app.listen(context.api_config.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
