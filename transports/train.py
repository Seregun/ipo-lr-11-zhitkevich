from transports.vehicle import Vehicle  # Импорт
class Train(Vehicle):  # Класс поезда, наследуется от Vehicle
    def __init__(self, capacity, number_of_cars):  # Конструктор для создания поезда
        super().__init__(capacity)  # Вызов конструктора родительского класса
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Number of cars must be a positive integer.")  # Проверка количества вагонов
        self.number_of_cars = number_of_cars  # Количество вагонов

    def __str__(self):  # Метод для строкового представления поезда
        return f"Train (ID: {self.vehicle_id}, Cars: {self.number_of_cars}, Capacity: {self.capacity}, Load: {self.current_load})"
