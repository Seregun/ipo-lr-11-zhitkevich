import uuid
from transports.client import Client
from transports.train import Train
from transports.transportcompany import TransportCompany
from transports.truck import Truck
from transports.vehicle import Vehicle

def main():  # Основная функция программы
    company = TransportCompany("Global Logistics")  # Создание транспортной компании

    while True:  # Бесконечный цикл для работы меню
        print("\n--- Меню ---")  # Заголовок меню
        print("1. Добавить клиента")  # Пункт меню: Добавить клиента
        print("2. Добавить транспорт")  # Пункт меню: Добавить транспорт
        print("3. Список транспорта")  # Пункт меню: Список транспорта
        print("4. Распределить груз")  # Пункт меню: Распределить груз
        print("5. Выход")  # Пункт меню: Выход

        choice = input("Введите пункт меню: ")  # Считывание выбора пользователя

        if choice == "1":  # Если выбран пункт 1
            name = input("Введите имя клиента: ")  # Ввод имени клиента
            cargo_weight = float(input("Введите вес груза (в тоннах): "))  # Ввод веса груза
            is_vip = input("Клиент VIP? (да/нет): ").strip().lower() == "да"  # Проверка статуса VIP
            try:
                new_client = Client(name, cargo_weight, is_vip)  # Создание объекта клиента
                company.add_client(new_client)  # Добавление клиента в компанию
                print(f"Добавлен клиент: {new_client}")  # Подтверждение добавления
            except ValueError as e:
                print(f"Ошибка: {e}")  # Вывод ошибки, если данные некорректны

        elif choice == "2":  # Если выбран пункт 2
            print("1. Добавить грузовик")  # Подменю: Добавить грузовик
            print("2. Добавить поезд")  # Подменю: Добавить поезд
            vehicle_choice = input("Введите ваш выбор: ")  # Считывание выбора типа транспорта
            capacity = float(input("Введите грузоподъемность (в тоннах): "))  # Ввод грузоподъемности

            if vehicle_choice == "1":  # Если выбран грузовик
                color = input("Введите цвет грузовика: ")  # Ввод цвета грузовика
                try:
                    new_truck = Truck(capacity, color)  # Создание объекта грузовика
                    company.add_vehicle(new_truck)  # Добавление грузовика в компанию
                    print(f"Добавлен грузовик: {new_truck}")  # Подтверждение добавления
                except ValueError as e:
                    print(f"Ошибка: {e}")  # Вывод ошибки, если данные некорректны

            elif vehicle_choice == "2":  # Если выбран поезд
                number_of_cars = int(input("Введите количество вагонов: "))  # Ввод количества вагонов
                try:
                    new_train = Train(capacity, number_of_cars)  # Создание объекта поезда
                    company.add_vehicle(new_train)  # Добавление поезда в компанию
                    print(f"Добавлен поезд: {new_train}")  # Подтверждение добавления
                except ValueError as e:
                    print(f"Ошибка: {e}")  # Вывод ошибки, если данные некорректны

        elif choice == "3":  # Если выбран пункт 3
            vehicles = company.list_vehicles()  # Получение списка транспорта
            print("\n--- Транспорт ---")  # Заголовок списка транспорта
            for vehicle in vehicles:  # Проход по списку транспорта
                print(vehicle)  # Вывод каждого транспортного средства

        elif choice == "4":  # Если выбран пункт 4
            try:
                company.optimize_cargo_distribution()  # Оптимизация распределения грузов
                print("Распределение груза завершено успешно.")  # Подтверждение завершения
                for vehicle in company.vehicles:  # Проход по списку транспорта
                    print(vehicle)  # Вывод транспортного средства
                    for client in vehicle.clients_list:  # Проход по списку клиентов
                        print(f"  - {client}")  # Вывод клиента
            except Exception as e:
                print(f"Ошибка: {e}")  # Вывод ошибки, если что-то пошло не так

        elif choice == "5":  # Если выбран пункт 5
            print("Завершение программы. До свидания!")  # Сообщение о завершении программы
            break  # Выход
main()