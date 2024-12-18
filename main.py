import uuid
from transports import truck, vehicle, client, train
from transports.transportcompany import TransportCompany

def main():  # Основная функция программы
    company = TransportCompany("Global Logistics")  # Создание транспортной компании

    while True:  # Бесконечный цикл для работы меню
        print("\n--- Меню ---")  # Заголовок меню
        print("1. Добавить клиента")  # Пункт меню: Добавить клиента
        print("2. Добавить транспорт")  # Пункт меню: Добавить транспорт
        print("3. Список транспорта")  # Пункт меню: Список транспорта
        print("4. Distribute Cargo")  # Пункт меню: Распределить груз
        print("5. Выход")  # Пункт меню: Выход

        choice = input("Введите пункт меню: ")  # Считывание выбора пользователя

        if choice == "1":  # Если выбран пункт 1
            name = input("Введите имя клиента: ")  # Ввод имени клиента
            cargo_weight = float(input("Введите вес: "))  # Ввод веса груза
            is_vip = input("Is VIP client? (yes/no): ").strip().lower() == "yes"  # Проверка статуса VIP
            try:
                new_client = client(name, cargo_weight, is_vip) # Создание объекта клиента
                company.add_client(client)  # Добавление клиента в компанию
                print(f"Added client: {client}")  # Подтверждение добавления
            except ValueError as e:
                print(f"Error: {e}")  # Вывод ошибки, если данные некорректны

        elif choice == "2":  # Если выбран пункт 2
            print("1. Add Truck")  # Подменю: Добавить грузовик
            print("2. Add Train")  # Подменю: Добавить поезд
            vehicle_choice = input("Enter your choice: ")  # Считывание выбора типа транспорта
            capacity = float(input("Enter capacity: "))  # Ввод грузоподъемности

            if vehicle_choice == "1":  # Если выбран грузовик
                color = input("Enter truck color: ")  # Ввод цвета грузовика
                try:
                    truck = truck(capacity, color)  # Создание объекта грузовика
                    company.add_vehicle(truck)  # Добавление грузовика в компанию
                    print(f"Added truck: {truck}")  # Подтверждение добавления
                except ValueError as e:
                    print(f"Error: {e}")  # Вывод ошибки, если данные некорректны

            elif vehicle_choice == "2":  # Если выбран поезд
                number_of_cars = int(input("Enter number of cars: "))  # Ввод количества вагонов
                try:
                    train = train(capacity, number_of_cars)  # Создание объекта поезда
                    company.add_vehicle(train)  # Добавление поезда в компанию
                    print(f"Added train: {train}")  # Подтверждение добавления
                except ValueError as e:
                    print(f"Error: {e}")  # Вывод ошибки, если данные некорректны

        elif choice == "3":  # Если выбран пункт 3
            vehicles = company.list_vehicles()  # Получение списка транспорта
            print("\n--- Vehicles ---")  # Заголовок списка транспорта
            for vehicle in vehicles:  # Проход по списку транспорта
                print(vehicle)  # Вывод каждого транспортного средства

        elif choice == "4":  # Если выбран пункт 4
            try:
                company.optimize_cargo_distribution()  # Оптимизация распределения грузов
                print("Cargo distribution completed successfully.")  # Подтверждение завершения
                for vehicle in company.vehicles:  # Проход по списку транспорта
                    print(vehicle)  # Вывод транспортного средства
                    for client in vehicle.clients_list:  # Проход по списку клиентов
                        print(f"  - {client}")  # Вывод клиента
            except Exception as e:
                print(f"Error: {e}")  # Вывод ошибки, если что-то пошло не так

        elif choice == "5":  # Если выбран пункт 5
            print("Exiting the program. Goodbye!")  # Сообщение о завершении программы
            break  # Выход
main()
