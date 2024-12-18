import uuid
from .client import Client
class Vehicle:  # Базовый класс для транспортного средства
    def __init__(self, capacity):  # Конструктор для создания транспортного средства
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Емкость должна быть положительным числом.")  # Проверка грузоподъемности
        self.vehicle_id = str(uuid.uuid4())  # Уникальный идентификатор транспортного средства
        self.capacity = capacity  # Грузоподъемность транспортного средства
        self.current_load = 0  # Текущая загрузка (изначально 0)
        self.clients_list = []  # Список клиентов, чьи грузы загружены

    def load_cargo(self, client):  # Метод для загрузки груза клиента
        if not isinstance(client, Client):
            raise ValueError("Недопустимый тип клиента.")  # Проверка типа клиента
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Превышает вместимость транспортного средства.")  # Проверка на превышение грузоподъемности
        self.current_load += client.cargo_weight  # Увеличение текущей загрузки
        self.clients_list.append(client)  # Добавление клиента в список загруженных

    def __str__(self):  # Метод для строкового представления транспортного средства
        return f"Транспорт ID: {self.vehicle_id}, Вместимость: {self.capacity}, Текущая нагрузка: {self.current_load}"
