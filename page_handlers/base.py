import tornado.web
from datetime import date
from dateutil import parser as dateutil
import logging


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.log = logging.getLogger(__name__)

    @property
    def db(self):
        return self.application.db

    def parse_query(self, data, description):
        if type(data) == list:
            result = []
            for value in data:
                result.append(self.parse_query(value, description))
        elif type(data) == tuple:
            result = {}
            for i in range(len(description)):
                if type(data[i]) == date:
                    value = data[i].strftime('%Y-%m-%d')
                else:
                    value = data[i]
                result[description[i][0]] = value
        else:
            result = {}
        return result


class ApiBase(BaseHandler):
    def _start_date(self):
        start_date = self.get_argument('start_date', False)
        if start_date:
            start_date = dateutil.parse(start_date).strftime('%Y-%m-%d')
        return start_date

    def _end_date(self):
        end_date = self.get_argument('end_date', False)
        if end_date:
            end_date = dateutil.parse(end_date).strftime('%Y-%m-%d')
        return end_date
