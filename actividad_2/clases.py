class Persona():
    def __init__(self, name):
        self.name = name

mengli = Persona("Mengli")

# print(mengli.name)
#
# setattr(mengli, 'edad', 22)
#
# print(mengli.edad)

class Student():
    admitidos = ["name", "edad"]
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v) if k in self.admitidos else None

mengli_std = Student(name="Mengli", edad=22)

print(mengli_std.name)
# print(mengli_std.edad)
# attrs = vars(mengli_std)
#
# print(", ".join([f"{k}: {v}" for k, v in attrs.items()]))

mengli_std.tetas = 4
