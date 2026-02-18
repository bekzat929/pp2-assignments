# method_overriding.py

class Animal:
    def speak(self):
        print("Animal makes a sound")


class Cat(Animal):
    # переопределяем метод родителя
    def speak(self):
        print("Cat meows")


class Dog(Animal):
    def speak(self):
        print("Dog barks")


# Использование
a = Animal()
c = Cat()
d = Dog()

a.speak()
c.speak()
d.speak()
