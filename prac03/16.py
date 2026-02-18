# multiple_inheritance.py

class Flyable:
    def fly(self):
        print("I can fly")


class Swimmable:
    def swim(self):
        print("I can swim")


class Duck(Flyable, Swimmable):
    def quack(self):
        print("Duck says quack")


# Использование
duck = Duck()
duck.fly()
duck.swim()
duck.quack()
