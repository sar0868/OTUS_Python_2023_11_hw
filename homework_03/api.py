#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import json
import datetime
import logging
import hashlib
import re
import uuid
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class CharField(object):
    # __slots__ = ('required', 'nullable', '__field')

    def __init__(self, required: bool, nullable: bool, field: str = None):
        self.nullable: bool = nullable
        self.required: bool = required
        self._field: str = field

    def __get__(self, instance, owner):
        return self._field

    def __set__(self, instance, value):
        self._field = value

    def validate(self):
        return isinstance(self._field, str)

    def __eq__(self, other):
        if isinstance(other, CharField):
            return self._field == other._field
        if isinstance(other, str):
            return self._field == other

    def __repr__(self):
        return self._field


class ArgumentsField:

    def __init__(self, required: bool, nullable: bool,
                 phone: "PhoneField" = None,
                 email: "EmailField" = None,
                 first_name: 'CharField' = None,
                 last_name: 'CharField' = None,
                 birthday: 'BirthDayField' = None,
                 gender: 'GenderField' = None
                 ):
        ...


class EmailField(CharField):

    def validate(self):
        regexp = re.compile('@')
        return regexp.search(self._field)


class PhoneField(CharField):
    def validate(self):
        regexp = re.compile("^['7',7]\w{10}")
        return regexp.search(self._field) or self._field is None


class DateField(CharField):
    def validate(self):
        if isinstance(self._field, datetime.datetime):
            if datetime.datetime.now() - datetime.timedelta(self._field.year) <= 70:
                print("ok")
        else:
            print("no")




        # return regexp.search(self._field) or self._field is None


class BirthDayField(DateField):
    pass


class GenderField(CharField):
    pass


class ClientIDsField(object):
    __slots__ = ('required')

    def __init__(self, required):
        self.required = required


class ClientsInterestsRequest(object):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(object):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


class MethodRequest(object):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=True)  # может быть пустым

    def __init__(self, request):
        for k, v in request.items():
            # setattr(self, k, v)
            if hasattr(self, k):
                setattr(self, k, v)
                # if k == "arguments":
                #     setattr(self, k, v)
                # else:
                #     attr = getattr(self, k)
                #     attr.field = v
                # attr = getattr(self, k)
                # if not attr.is_valid():
                #     self.code = BAD_REQUEST

    #
    # # проверить есть ли поле запроса в классе и если есть заполнить его,
    # # если данные не валидны -> исключение
    #
    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN

    #
    @property
    def response(self):
        response = {"score": self.__response}
        return {"code": self.code, "response": response}

    def create_response(self):
        self.__response = ""


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512(datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).hexdigest()
    else:
        digest = hashlib.sha512(request.account + request.login + SALT).hexdigest()
    if digest == request.token:
        return True
    return False


def method_handler(request, ctx, store):
    request = MethodRequest(request)

    response, code = request.response, request.code
    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
