from .vehicle import Vehicle
from .client import Client
class TransportCompany:  # Класс транспортной компании
    def __init__(self, name):  # Конструктор для создания компании
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")  # Проверка типа имени
        self.name = name  # Название компании
        self.vehicles = []  # Список транспортных средств компании
        self.clients = []  # Список клиентов компании

    def add_vehicle(self, vehicle):  # Метод для добавления транспортного средства
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Invalid vehicle type.")  # Проверка типа транспортного средства
        self.vehicles.append(vehicle)  # Добавление транспортного средства в список

    def list_vehicles(self):  # Метод для получения списка всех транспортных средств
        return [str(vehicle) for vehicle in self.vehicles]  # Возвращение строкового представления транспорта

    def add_client(self, client):  # Метод для добавления клиента
        if not isinstance(client, Client):
            raise ValueError("Invalid client type.")  # Проверка типа клиента
        self.clients.append(client)  # Добавление клиента в список

    def optimize_cargo_distribution(self):  # Метод для оптимизации распределения грузов
        self.clients.sort(key=lambda x: x.is_vip, reverse=True)  # Сортировка клиентов (VIP в начале)
        for client in self.clients:  # Проход по списку клиентов
            for vehicle in sorted(self.vehicles, key=lambda v: v.capacity - v.current_load):  # Сортировка транспорта по свободной грузоподъемности
                try:
                    vehicle.load_cargo(client)  # Попытка загрузить груз клиента
                    break  # Выход из цикла, если загрузка успешна
                except ValueError:
                    continue  # Переход к следующему транспортному средству, если загрузка невозможна