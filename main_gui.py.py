import dearpygui.dearpygui as dpg
from transports.client import Client
from transports.truck import Truck
from transports.train import Train
from transports.transportcompany import TransportCompany
import pickle

company = TransportCompany("Global Logistics")

def add_client_callback(sender, app_data, user_data):
    name = dpg.get_value("client_name")
    cargo_weight = dpg.get_value("client_weight")
    is_vip = dpg.get_value("client_vip")
    try:
        new_client = Client(name, cargo_weight, is_vip)
        company.add_client(new_client)
        dpg.configure_item("status", default_value="Клиент добавлен успешно.")
    except ValueError as e:
        dpg.configure_item("status", default_value=f"Ошибка: {e}")

def add_transport_callback(sender, app_data, user_data):
    transport_type = dpg.get_value("transport_type")
    capacity = dpg.get_value("transport_capacity")
    if transport_type == "Truck":
        color = dpg.get_value("truck_color")
        try:
            new_truck = Truck(capacity, color)
            company.add_vehicle(new_truck)
            dpg.configure_item("status", default_value="Грузовик добавлен успешно.")
        except ValueError as e:
            dpg.configure_item("status", default_value=f"Ошибка: {e}")
    elif transport_type == "Train":
        number_of_cars = dpg.get_value("number_of_cars")
        try:
            new_train = Train(capacity, number_of_cars)
            company.add_vehicle(new_train)
            dpg.configure_item("status", default_value="Поезд добавлен успешно.")
        except ValueError as e:
            dpg.configure_item("status", default_value=f"Ошибка: {e}")

def save_data_callback(sender, app_data, user_data):
    with open("data.pkl", "wb") as f:
        pickle.dump({"clients": company.clients, "vehicles": company.vehicles}, f)
    dpg.configure_item("status", default_value="Данные сохранены успешно.")

dpg.create_context()

# Загрузка шрифта, поддерживающего кириллицу
with dpg.font_registry():
    with dpg.font("Roboto-Regular.ttf", 20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font(default_font)

with dpg.window(label="Главное окно приложения"):
    with dpg.menu_bar():
        with dpg.menu(label="Меню"):
            dpg.add_menu_item(label="Экспорт результата", callback=save_data_callback)
            dpg.add_menu_item(label="О программе", callback=lambda: dpg.show_item("about_window"))

    with dpg.group(label="Управление клиентами"):
        dpg.add_input_text(label="Имя клиента", tag="client_name")
        dpg.add_input_float(label="Вес груза", tag="client_weight")
        dpg.add_checkbox(label="VIP статус", tag="client_vip")
        dpg.add_button(label="Добавить клиента", callback=add_client_callback)

    with dpg.group(label="Управление транспортом"):
        dpg.add_combo(label="Тип транспорта", items=["Грузовик", "Поезд"], tag="transport_type")
        dpg.add_input_float(label="Грузоподъемность", tag="transport_capacity")
        dpg.add_input_text(label="Цвет грузовика", tag="truck_color", show=False)
        dpg.add_input_int(label="Количество вагонов", tag="number_of_cars", show=False)
        dpg.add_button(label="Добавить транспорт", callback=add_transport_callback)

    dpg.add_text(tag="status", default_value="")

with dpg.window(label="О программе", tag="about_window", show=False):
    dpg.add_text("ЛР11 - GUI реализация")
    dpg.add_text("Вариант: 1")
    dpg.add_text("Разработчик: Житкевич Максим")
    dpg.add_button(label="Закрыть", callback=lambda: dpg.hide_item("about_window"))

dpg.create_viewport(title='ЛР11 GUI', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()