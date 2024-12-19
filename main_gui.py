import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random

# Класс транспортной компании
class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Vehicle must be an instance of Vehicle class")
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return self.vehicles

    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Client must be an instance of Client class")
        self.clients.append(client)

    def optimize_cargo_distribution(self):
        # Сортировка клиентов: VIP клиенты в приоритете
        self.clients.sort(key=lambda x: x.vip, reverse=True)

        # Распределение грузов
        for client in self.clients:
            if client.cargo_assigned:
                continue

            for vehicle in self.vehicles:
                if vehicle.available_capacity >= client.cargo:
                    vehicle.load_cargo(client)
                    client.cargo_assigned = True
                    break

# Класс транспортного средства
class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, capacity):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.current_load = 0
        self.cargo_list = []

    @property
    def available_capacity(self):
        return self.capacity - self.current_load

    def load_cargo(self, client):
        self.current_load += client.cargo
        self.cargo_list.append(client)
        client.vehicle = self

# Класс клиента
class Client:
    def __init__(self, name, cargo, vip):
        self.name = name
        self.cargo = cargo
        self.vip = vip
        self.cargo_assigned = False
        self.vehicle = None

# Основной класс приложения
class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная компания")
        
        # Меню
        self.create_menu()

        # Панель управления
        self.create_control_panel()

        # Таблицы данных
        self.create_tables()

        # Статусная строка
        self.status_label = tk.Label(self.root, text="Добро пожаловать!", anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Транспортная компания
        self.transport_company = None

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Экспорт результата", command=self.export_data)
        menu.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu.add_cascade(label="Помощь", menu=help_menu)

    def create_control_panel(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(control_frame, text="Добавить клиента", command=self.add_client).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(control_frame, text="Добавить транспорт", command=self.add_vehicle).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(control_frame, text="Распределить грузы", command=self.optimize_cargo).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(control_frame, text="Удалить запись", command=self.delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(control_frame, text="Транспортная компания", command=self.create_company).pack(side=tk.LEFT, padx=5, pady=5)

        # Фильтрация
        tk.Label(control_frame, text="Фильтр по типу транспорта:").pack(side=tk.LEFT, padx=5, pady=5)
        self.filter_var = tk.StringVar()
        self.filter_var.set("Все")
        type_menu = ttk.Combobox(control_frame, textvariable=self.filter_var, values=["Все", "Грузовик", "Поезд"])
        type_menu.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(control_frame, text="Применить фильтр", command=self.apply_filter).pack(side=tk.LEFT, padx=5, pady=5)

    def create_tables(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.client_table = ttk.Treeview(table_frame, columns=("name", "cargo", "vip", "vehicle"), show="headings")
        self.client_table.heading("name", text="Имя клиента", command=lambda: self.sort_column(self.client_table, "name"))
        self.client_table.heading("cargo", text="Вес груза (кг)", command=lambda: self.sort_column(self.client_table, "cargo"))
        self.client_table.heading("vip", text="VIP", command=lambda: self.sort_column(self.client_table, "vip"))
        self.client_table.heading("vehicle", text="Транспорт", command=lambda: self.sort_column(self.client_table, "vehicle"))
        self.client_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.client_table.bind("<Double-1>", self.edit_client)

        self.vehicle_table = ttk.Treeview(table_frame, columns=("id", "type", "capacity", "load", "cargo_list"), show="headings")
        self.vehicle_table.heading("id", text="ID транспорта", command=lambda: self.sort_column(self.vehicle_table, "id"))
        self.vehicle_table.heading("type", text="Тип транспорта", command=lambda: self.sort_column(self.vehicle_table, "type"))
        self.vehicle_table.heading("capacity", text="Грузоподъемность", command=lambda: self.sort_column(self.vehicle_table, "capacity"))
        self.vehicle_table.heading("load", text="Текущая загрузка", command=lambda: self.sort_column(self.vehicle_table, "load"))
        self.vehicle_table.heading("cargo_list", text="Список грузов", command=lambda: self.sort_column(self.vehicle_table, "cargo_list"))
        self.vehicle_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.vehicle_table.bind("<Double-1>", self.edit_vehicle)

    def sort_column(self, table, column):
        """Сортировка таблицы по выбранному столбцу."""
        data = [(table.item(item, "values")) for item in table.get_children()]
        if column == "cargo" or column == "capacity" or column == "load":
            data.sort(key=lambda x: float(x[1] if column == "cargo" else x[2] if column == "capacity" else x[3]))
        else:
            data.sort(key=lambda x: x[0])
        for idx, item in enumerate(data):
            table.item(table.get_children()[idx], values=item)

    def apply_filter(self):
        """Применение фильтра к таблице транспортных средств."""
        filter_value = self.filter_var.get()
        for item in self.vehicle_table.get_children():
            vehicle_type = self.vehicle_table.item(item, "values")[1]
            if filter_value != "Все" and vehicle_type != filter_value:
                self.vehicle_table.detach(item)
            else:
                if item not in self.vehicle_table.get_children():
                    self.vehicle_table.reattach(item, '', 'end')

    def add_client(self):
        def save_client():
            name = name_entry.get()
            cargo = cargo_entry.get()
            vip = vip_var.get()

            if not name.isalpha() or len(name) < 2:
                messagebox.showerror("Ошибка", "Имя должно содержать минимум 2 буквы.")
                return

            try:
                cargo = float(cargo)
                if cargo <= 0 or cargo > 10000:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10000 кг.")
                return

            client = Client(name, cargo, vip)
            self.client_table.insert("", "end", values=(name, cargo, "Да" if vip else "Нет", ''))
            if self.transport_company:
                self.transport_company.add_client(client)
            self.status_label.config(text="Клиент добавлен.")
            client_window.destroy()

        def cancel_client():
            client_window.destroy()

        client_window = tk.Toplevel(self.root)
        client_window.title("Добавить клиента")

        tk.Label(client_window, text="Имя клиента:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(client_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(client_window, text="Вес груза (кг):").grid(row=1, column=0, padx=5, pady=5)
        cargo_entry = tk.Entry(client_window)
        cargo_entry.grid(row=1, column=1, padx=5, pady=5)

        vip_var = tk.BooleanVar()
        tk.Checkbutton(client_window, text="VIP клиент", variable=vip_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(client_window, text="Сохранить", command=save_client).grid(row=3, column=0, pady=10)
        tk.Button(client_window, text="Отмена", command=cancel_client).grid(row=3, column=1, pady=10)

    def add_vehicle(self):
        def save_vehicle():
            vehicle_type = type_var.get()
            capacity = capacity_entry.get()

            try:
                capacity = float(capacity)
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
                return

            vehicle_id = f"ID{random.randint(100, 999)}"
            vehicle = Vehicle(vehicle_id, vehicle_type, capacity)
            self.vehicle_table.insert("", "end", values=(vehicle_id, vehicle_type, capacity, "0", ''))
            if self.transport_company:
                self.transport_company.add_vehicle(vehicle)
            self.status_label.config(text="Транспорт добавлен.")
            vehicle_window.destroy()

        def cancel_vehicle():
            vehicle_window.destroy()

        vehicle_window = tk.Toplevel(self.root)
        vehicle_window.title("Добавить транспорт")

        tk.Label(vehicle_window, text="Тип транспорта:").grid(row=0, column=0, padx=5, pady=5)
        type_var = tk.StringVar()
        type_menu = ttk.Combobox(vehicle_window, textvariable=type_var, values=["Грузовик", "Поезд"])
        type_menu.grid(row=0, column=1, padx=5, pady=5)
        type_menu.current(0)

        tk.Label(vehicle_window, text="Грузоподъемность (кг):").grid(row=1, column=0, padx=5, pady=5)
        capacity_entry = tk.Entry(vehicle_window)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(vehicle_window, text="Сохранить", command=save_vehicle).grid(row=2, column=0, pady=10)
        tk.Button(vehicle_window, text="Отмена", command=cancel_vehicle).grid(row=2, column=1, pady=10)

    def edit_client(self, event):
        selected_item = self.client_table.selection()
        if not selected_item:
            return

        values = self.client_table.item(selected_item, "values")

        def save_changes():
            name = name_entry.get()
            cargo = cargo_entry.get()
            vip = vip_var.get()

            try:
                cargo = float(cargo)
                if cargo <= 0 or cargo > 10000:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10000 кг.")
                return

            self.client_table.item(selected_item, values=(name, cargo, "Да" if vip else "Нет", ''))
            client_window.destroy()

        client_window = tk.Toplevel(self.root)
        client_window.title("Редактировать клиента")

        tk.Label(client_window, text="Имя клиента:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(client_window)
        name_entry.insert(0, values[0])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(client_window, text="Вес груза (кг):").grid(row=1, column=0, padx=5, pady=5)
        cargo_entry = tk.Entry(client_window)
        cargo_entry.insert(0, values[1])
        cargo_entry.grid(row=1, column=1, padx=5, pady=5)

        vip_var = tk.BooleanVar(value=(values[2] == "Да"))
        tk.Checkbutton(client_window, text="VIP клиент", variable=vip_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(client_window, text="Сохранить", command=save_changes).grid(row=3, column=0, pady=10)
        tk.Button(client_window, text="Отмена", command=lambda: client_window.destroy()).grid(row=3, column=1, pady=10)

    def edit_vehicle(self, event):
        selected_item = self.vehicle_table.selection()
        if not selected_item:
            return

        values = self.vehicle_table.item(selected_item, "values")

        def save_changes():
            vehicle_type = type_var.get()
            capacity = capacity_entry.get()

            try:
                capacity = float(capacity)
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
                return

            self.vehicle_table.item(selected_item, values=(values[0], vehicle_type, capacity, values[3], ''))
            vehicle_window.destroy()

        vehicle_window = tk.Toplevel(self.root)
        vehicle_window.title("Редактировать транспорт")

        tk.Label(vehicle_window, text="Тип транспорта:").grid(row=0, column=0, padx=5, pady=5)
        type_var = tk.StringVar(value=values[1])
        type_menu = ttk.Combobox(vehicle_window, textvariable=type_var, values=["Грузовик", "Поезд"])
        type_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(vehicle_window, text="Грузоподъемность (кг):").grid(row=1, column=0, padx=5, pady=5)
        capacity_entry = tk.Entry(vehicle_window)
        capacity_entry.insert(0, values[2])
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(vehicle_window, text="Сохранить", command=save_changes).grid(row=2, column=0, pady=10)
        tk.Button(vehicle_window, text="Отмена", command=lambda: vehicle_window.destroy()).grid(row=2, column=1, pady=10)

    def delete_selected(self):
        for table in [self.client_table, self.vehicle_table]:
            selected_item = table.selection()
            for item in selected_item:
                table.delete(item)
        self.status_label.config(text="Запись удалена.")

    def optimize_cargo(self):
        if not self.transport_company:
            messagebox.showerror("Ошибка", "Сначала создайте транспортную компанию!")
            return

        self.transport_company.optimize_cargo_distribution()

        # Обновление данных в таблицах
        for i in self.client_table.get_children():
            client_data = self.client_table.item(i, "values")
            client = next(c for c in self.transport_company.clients if c.name == client_data[0])
            self.client_table.item(i, values=(client_data[0], client_data[1], client_data[2], client.vehicle.vehicle_id if client.vehicle else ''))

        for i in self.vehicle_table.get_children():
            vehicle_data = self.vehicle_table.item(i, "values")
            vehicle = next(v for v in self.transport_company.vehicles if v.vehicle_id == vehicle_data[0])
            self.vehicle_table.item(i, values=(vehicle_data[0], vehicle_data[1], vehicle_data[2], vehicle.current_load, ', '.join([c.name for c in vehicle.cargo_list])))

        # Обновление статуса
        self.status_label.config(text="Распределение завершено.")

    def export_data(self):
        # Экспорт данных в файл
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for item in self.client_table.get_children():
                    file.write(f"Клиент: {self.client_table.item(item, 'values')}\n")
                for item in self.vehicle_table.get_children():
                    file.write(f"Транспорт: {self.vehicle_table.item(item, 'values')}\n")
            self.status_label.config(text="Данные экспортированы.")

    def show_about(self):
        messagebox.showinfo("О программе\n", "ЛР12, Вариант 1\nРазработчик: Житкевич Максим")

    def create_company(self):
        def save_company():
            company_name = company_entry.get()
            if not company_name:
                messagebox.showerror("Ошибка", "Введите название компании")
                return
            self.transport_company = TransportCompany(company_name)
            company_window.destroy()
            self.status_label.config(text=f"Создана транспортная компания '{company_name}'")

        def cancel_company():
            company_window.destroy()

        company_window = tk.Toplevel(self.root)
        company_window.title("Создать компанию")

        tk.Label(company_window, text="Название компании:").grid(row=0, column=0, padx=5, pady=5)
        company_entry = tk.Entry(company_window)
        company_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(company_window, text="Создать", command=save_company).grid(row=1, column=0, pady=10)
        tk.Button(company_window, text="Отмена", command=cancel_company).grid(row=1, column=1, pady=10)
            
# Создание и запуск приложения
root = tk.Tk()
app = TransportApp(root)
root.mainloop()
