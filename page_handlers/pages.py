from .base import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html')


class Requests(BaseHandler):
    def get(self):
        self.render('requests.html')
