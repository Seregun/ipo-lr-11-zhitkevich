class Client:  # Класс для описания клиента
    def __init__(self, name, cargo_weight, is_vip=False):  # Конструктор для создания клиента
        if not isinstance(name, str) or not isinstance(cargo_weight, (int, float)) or not isinstance(is_vip, bool):
            raise ValueError("Недопустимые типы входных данных.")  # Проверка типов данных
        self.name = name  # Имя клиента
        self.cargo_weight = cargo_weight  # Вес груза клиента
        self.is_vip = is_vip  # Статус VIP (по умолчанию False)

    def __str__(self):  # Метод для строкового представления клиента
        return f"Имя клиента: {self.name}, Вес груза (в тоннах): {self.cargo_weight}, VIP: {self.is_vip}"