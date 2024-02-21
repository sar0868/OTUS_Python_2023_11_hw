

class CharField(object):
    def __init__(self, required: bool, nullable: bool, field: str = None):
        self.nullable: bool = nullable
        self.required: bool = required
        self._field: str = field

    def __get__(self, instance, owner):
        return self._field

    def __set__(self, instance, value):
        if len(value) < 3:
            raise ValueError
        self._field = value

    # def validate(self):
    #     if se
    #
    #     return isinstance(self._field, str)

class Exampl:
    obj1 = CharField(required=True, nullable=False)

    def __init__(self, value):
        self.obj1 = value


temp1 = Exampl('sss')
print(temp1.__dict__)

print(temp1.__dict__)
print(temp1.obj1)
temp1.is_admin  = False
print(temp1.__dict__)
print(temp1.is_admin)

