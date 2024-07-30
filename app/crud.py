from sqlalchemy.orm import Session
from .models import Device, Battery


class DBHandler:
    """Класс содержащий все взаимодействия с моделями"""
    def __init__(self, session: Session):
        self.session = session

    def get_device(self, device_id: int):
        return self.session.query(Device).get(device_id)

    def get_devices(self):
        return self.session.query(Device).all()

    def add_device(self, name: str):
        device = Device(name=name)
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device

    def update_device(self, device_id: int, name: str):
        device = self.get_device(device_id)
        if device:
            device.name = name
            self.session.commit()
            self.session.refresh(device)
        return device

    def delete_device(self, device_id: int):
        device = self.get_device(device_id)
        if device:
            self.session.delete(device)
            self.session.commit()
        return device

    def get_battery(self, battery_id: int):
        return self.session.query(Battery).get(battery_id)

    def get_batteries(self):
        return self.session.query(Battery).all()

    def add_battery(self, name: str, device_id: int):
        device = self.get_device(device_id)
        if not device:
            raise Exception("Устройство не найдено")
        if len(device.batteries) >= 5:
            raise Exception("У устройства уже есть 5 батарей")
        battery = Battery(name=name, device_id=device_id)
        self.session.add(battery)
        self.session.commit()
        self.session.refresh(battery)
        return battery

    def update_battery(self, battery_id: int, name: str, device_id: int):
        battery = self.get_battery(battery_id)
        if battery:
            battery.name = name
            battery.battery_id = device_id
            self.session.commit()
            self.session.refresh(battery)
        return battery

    def delete_battery(self, battery_id: int):
        battery = self.get_battery(battery_id)
        if battery:
            self.session.delete(battery)
            self.session.commit()
        return battery
