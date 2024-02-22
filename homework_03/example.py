

class CharField(object):
    def __init__(self, required: bool, nullable: bool, field: str = None):
        self.nullable: bool = nullable
        self.required: bool = required
        self._field: str = field

    def __get__(self, instance, owner):
        return self._field

    def __set__(self, instance, value):
        # if self.validate():
        #     raise ValueError
        setattr(instance, self._field, value)

    def validate(self):
        return self == "qqqq"

class Exampl:
    obj1 = CharField(required=True, nullable=False)

    # def __init__(self, value):
    #     self.obj1 = value
    #     print(self.obj1)
        # if self.obj1.validate():
        #     print("ok")
        # else:
        #     print("no")


temp1 = Exampl()
print(temp1.__dict__)
# field = CharField(required=True, nullable=False, field="eee")
# print(field)
temp1.obj1 = "hii1"
print(temp1.obj1)
print(type(temp1.obj1))
temp1.is_admin = False
print(temp1.__dict__)
print(temp1.is_admin)



