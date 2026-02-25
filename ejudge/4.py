import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        # Печатает координаты в формате (x, y)
        print(f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        # Обновляет координаты точки
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        # Вычисляет Евклидово расстояние до другой точки
        distance = math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)
        return distance

# 1. Читаем начальные координаты первой точки
x1, y1 = map(int, input().split())
p1 = Point(x1, y1)
p1.show() # Вывод: начальные координаты

# 2. Читаем координаты для перемещения первой точки
x2, y2 = map(int, input().split())
p1.move(x2, y2)
p1.show() # Вывод: координаты после перемещения

# 3. Читаем координаты второй точки для расчета расстояния
x3, y3 = map(int, input().split())
p2 = Point(x3, y3)

# 4. Рассчитываем расстояние и выводим с 2 знаками после запятой
result_dist = p1.dist(p2)
print(f"{result_dist:.2f}")