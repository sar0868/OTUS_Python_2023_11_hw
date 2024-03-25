

class CharField(object):
    def __init__(self, required: bool, nullable: bool, field: str = ""):
        self.nullable: bool = nullable
        self.required: bool = required
        self._field: str = field

    def __get__(self, instance, cls):
        return getattr(instance, self._field)

    def __set__(self, instance, value):
        if self.validate(value):
            raise ValueError
        setattr(instance, self._field, value)

    def validate(self, value):
        return value == "qqqq"

class Exampl:
    obj1 = CharField(required=True, nullable=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                print(k)
                setattr(self, k, v)
            else:
                print(self.__dict__)
                print(f"don't attr {k}")

        # self.obj1 = value
        # print(self.obj1)
        # if self.obj1.validate():
        #     print("ok")
        # else:
        #     print("no")


temp1 = Exampl(obj1="hello")
print(temp1.__dict__)
# field = CharField(required=True, nullable=False, field="eee")
# print(field)
temp1.obj1 = "hii1"
print(f"Print temp1.obj1 = {temp1.obj1}")
print(type(temp1.obj1))
temp1.is_admin = False
print(temp1.__dict__)
print(temp1.is_admin)



