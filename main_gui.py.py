import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random

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

    def create_tables(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.client_table = ttk.Treeview(table_frame, columns=("name", "cargo", "vip"), show="headings")
        self.client_table.heading("name", text="Имя клиента")
        self.client_table.heading("cargo", text="Вес груза")
        self.client_table.heading("vip", text="VIP")
        self.client_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vehicle_table = ttk.Treeview(table_frame, columns=("id", "type", "capacity", "load"), show="headings")
        self.vehicle_table.heading("id", text="ID транспорта")
        self.vehicle_table.heading("type", text="Тип транспорта")
        self.vehicle_table.heading("capacity", text="Грузоподъемность")
        self.vehicle_table.heading("load", text="Текущая загрузка")
        self.vehicle_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
                if cargo <= 0 or cargo > 1000:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 1000 тонн.")
                return

            self.client_table.insert("", "end", values=(name, cargo, "Да" if vip else "Нет"))
            self.status_label.config(text="Клиент добавлен.")
            client_window.destroy()

        client_window = tk.Toplevel(self.root)
        client_window.title("Добавить клиента")

        tk.Label(client_window, text="Имя клиента:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(client_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(client_window, text="Вес груза (тонн):").grid(row=1, column=0, padx=5, pady=5)
        cargo_entry = tk.Entry(client_window)
        cargo_entry.grid(row=1, column=1, padx=5, pady=5)

        vip_var = tk.BooleanVar()
        tk.Checkbutton(client_window, text="VIP клиент", variable=vip_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(client_window, text="Сохранить", command=save_client).grid(row=3, column=0, columnspan=2, pady=10)

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

            vehicle_id = f"ID{random.randint(1000, 9999)}"  # Генерация случайного ID транспорта
            self.vehicle_table.insert("", "end", values=(vehicle_id, vehicle_type, capacity, "0"))
            self.status_label.config(text="Транспорт добавлен.")
            vehicle_window.destroy()

        vehicle_window = tk.Toplevel(self.root)
        vehicle_window.title("Добавить транспорт")

        tk.Label(vehicle_window, text="Тип транспорта:").grid(row=0, column=0, padx=5, pady=5)
        type_var = tk.StringVar()
        type_menu = ttk.Combobox(vehicle_window, textvariable=type_var, values=["Грузовик", "Поезд"])
        type_menu.grid(row=0, column=1, padx=5, pady=5)
        type_menu.current(0)

        tk.Label(vehicle_window, text="Грузоподъемность (тонн):").grid(row=1, column=0, padx=5, pady=5)
        capacity_entry = tk.Entry(vehicle_window)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(vehicle_window, text="Сохранить", command=save_vehicle).grid(row=2, column=0, columnspan=2, pady=10)

    def optimize_cargo(self):
        clients = [(self.client_table.item(item)['values'][0],  # Имя клиента
                    float(self.client_table.item(item)['values'][1]),  # Вес груза
                    self.client_table.item(item)['values'][2] == "Да")  # VIP статус
                   for item in self.client_table.get_children()]

        vehicles = [(self.vehicle_table.item(item)['values'][0],  # ID транспорта
                     self.vehicle_table.item(item)['values'][1],  # Тип транспорта
                     float(self.vehicle_table.item(item)['values'][2]),  # Грузоподъемность
                     float(self.vehicle_table.item(item)['values'][3]))  # Текущая загрузка
                    for item in self.vehicle_table.get_children()]

        # Сортировка клиентов по VIP статусу и весу груза
        clients.sort(key=lambda x: (-x[2], -x[1]))

        for client_name, cargo_weight, is_vip in clients:
            for i, (vehicle_id, vehicle_type, capacity, current_load) in enumerate(vehicles):
                available_capacity = capacity - current_load
                if available_capacity >= cargo_weight:
                    # Обновление данных транспорта
                    vehicles[i] = (vehicle_id, vehicle_type, capacity, current_load + cargo_weight)
                    self.status_label.config(text=f"Груз {client_name} распределен.")
                    break
            else:
                messagebox.showwarning("Предупреждение", f"Недостаточно транспорта для клиента {client_name}.")

        # Обновление таблицы транспорта
        for item in self.vehicle_table.get_children():
            self.vehicle_table.delete(item)
        for vehicle_id, vehicle_type, capacity, current_load in vehicles:
            self.vehicle_table.insert("", "end", values=(vehicle_id, vehicle_type, capacity, current_load))

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("Результаты распределения грузов:\n")
                file.write("(Данные будут добавлены здесь)")
            messagebox.showinfo("Экспорт", "Результаты успешно сохранены.")

    def show_about(self):
        messagebox.showinfo("О программе", "ЛР 12, Вариант 1\nРазработчик: Житкевич Максим")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()
