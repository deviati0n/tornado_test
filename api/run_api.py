import os
from typing import Optional, Awaitable

import tornado
from tornado.ioloop import IOLoop
from tornado.web import Application

from database.data_class import DataFunction
from database.user_class import UserFunction
from parsing.run_scraper import data_to_json, parsing, fill_table
from project.project_context import ProjectContext

context = ProjectContext()
user_func = UserFunction()
data_func = DataFunction()


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render("html/index.html")

    def get_current_user(self):
        return self.get_secure_cookie("user")


class DataHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_func.set_last_request(self.current_user.decode("utf-8"))

        amount_filter = self.get_argument("amount", None)
        sort_filter = self.get_argument("sort", None)

        amount = data_func.take_distinct_amount()
        data = data_func.receive_data(amount_filter, sort_filter)

        self.set_header("Content-Type", "text/html")
        self.render(
            "html/data.html",
            value=data,
            amount=amount
        )

    def post(self):
        result_of_pars = parsing()
        fill_table(result_of_pars)
        self.redirect('/data')


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


class SignInHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "text/html")
        self.render("html/signin.html")

    def post(self):
        self.set_header("Content-Type", "text/html")
        user_func.add_user(self.get_argument("login"), self.get_argument("password"))

        self.set_secure_cookie("user", self.get_argument("login"), expires_days=1)
        self.redirect("/data")


class LoginHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "text/html")
        self.render("html/login.html", value="ok")

    def post(self):
        self.set_header("Content-Type", "text/html")
        if user_func.check_user(self.get_argument("login"), self.get_argument("password")):
            self.set_secure_cookie("user", self.get_argument("login"))
            self.redirect("/data")
        else:
            self.render("html/login.html", value="error")


class ApiDataHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        all_rows = parsing()
        data_json = data_to_json(all_rows)
        self.write(data_json)


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
        (r"/signin", SignInHandler),
        (r"/logout", LogoutHandler),
        (r"/data", DataHandler),
        (r"/api/data", ApiDataHandler)
    ], **settings)

    app.listen(context.api_config.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
