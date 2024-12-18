from .vehicle import Vehicle
class Truck(Vehicle):  # Класс грузовика, наследуется от Vehicle
    def __init__(self, capacity, color):  # Конструктор для создания грузовика
        super().__init__(capacity)  # Вызов конструктора родительского класса
        if not isinstance(color, str):
            raise ValueError("Цвет должен быть строкой.")  # Проверка типа цвета
        self.color = color  # Цвет грузовика

    def __str__(self):  # Метод для строкового представления грузовика
        return f"Грузовик (ID: {self.vehicle_id}, Цвет: {self.color}, Вместимость: {self.capacity}, Загрузка: {self.current_load})"