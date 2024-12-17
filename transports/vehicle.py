import uuid
from .client import Client
class Vehicle:  # Базовый класс для транспортного средства
    def __init__(self, capacity):  # Конструктор для создания транспортного средства
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Capacity must be a positive number.")  # Проверка грузоподъемности
        self.vehicle_id = str(uuid.uuid4())  # Уникальный идентификатор транспортного средства
        self.capacity = capacity  # Грузоподъемность транспортного средства
        self.current_load = 0  # Текущая загрузка (изначально 0)
        self.clients_list = []  # Список клиентов, чьи грузы загружены

    def load_cargo(self, client):  # Метод для загрузки груза клиента
        if not isinstance(client, Client):
            raise ValueError("Invalid client type.")  # Проверка типа клиента
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Exceeds vehicle capacity.")  # Проверка на превышение грузоподъемности
        self.current_load += client.cargo_weight  # Увеличение текущей загрузки
        self.clients_list.append(client)  # Добавление клиента в список загруженных

    def __str__(self):  # Метод для строкового представления транспортного средства
        return f"Vehicle ID: {self.vehicle_id}, Capacity: {self.capacity}, Current Load: {self.current_load}"
