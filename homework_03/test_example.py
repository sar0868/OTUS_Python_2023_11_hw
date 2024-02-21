import datetime
import re

import api


def test_valid_email():
    email = api.EmailField(required=False, nullable=True, data="@ddsd@fs")
    assert email.validate()


def test_method_request():
    arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1},
    request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": '', "arguments": arguments}
    temp = api.MethodRequest(request)
    # assert temp.login == "admin"
    print(temp.arguments)
    print(temp.account)
    print(temp.is_admin)


def test_incorrect_request():
    arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1},
    requests = [
        ({"login": "admin", "token": "", "method": "online_score", "arguments": arguments}, api.OK),
        ({"account": "horns&hoofs", "token": "", "method": "online_score", "arguments": arguments}, api.INVALID_REQUEST),
        ({"account": "horns&hoofs", "login": "admin", "token": "",
          "method": "online_score", "arguments": arguments}, api.OK),
                ]
    for request in requests:
        response = api.MethodRequest(request[0])
        assert response.code == request[1], response.code

# test_incorrect_request()
test_method_request()
# datatemp = api.DateField(required=False, nullable=True, field=datetime.date(2022,12,25))
# print(datatemp._field)
# datatemp.validate()
# test_valid_email()
# class A:
#     def __init__(self, name):
#         self.name = name
#
#
#
#     def __eq__(self, other):
#         if isinstance(other, A):
#             return self.name == other.name
#         if isinstance(other, str):
#             return self.name == other
#
# a = A("user")
# print(a == "user")
#
# regexp = re.compile("^7\d{10}")
# n = '7'
# if regexp.search(str(n)+ str(2345678901)):
#     print('ok')
# else:
#     print('no')
