# super_function.py

class Animal:
    def __init__(self, name):
        self.name = name
        print("Animal constructor called")

    def speak(self):
        print("Animal makes a sound")


class Dog(Animal):
    def __init__(self, name, breed):
        # вызываем конструктор родителя
        super().__init__(name)
        self.breed = breed
        print("Dog constructor called")

    def speak(self):
        print(f"{self.name} barks")


# Использование
dog = Dog("Buddy", "Labrador")
dog.speak()
