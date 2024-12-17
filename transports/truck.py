from .vehicle import Vehicle
class Truck(Vehicle):  # Класс грузовика, наследуется от Vehicle
    def __init__(self, capacity, color):  # Конструктор для создания грузовика
        super().__init__(capacity)  # Вызов конструктора родительского класса
        if not isinstance(color, str):
            raise ValueError("Color must be a string.")  # Проверка типа цвета
        self.color = color  # Цвет грузовика

    def __str__(self):  # Метод для строкового представления грузовика
        return f"Truck (ID: {self.vehicle_id}, Color: {self.color}, Capacity: {self.capacity}, Load: {self.current_load})"