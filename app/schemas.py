from pydantic import BaseModel


class BatteryBase(BaseModel):
    name: str


class BatteryCreate(BatteryBase):
    device_id: int


class Battery(BatteryBase):
    id: int
    device_id: int

    class Config:
        from_attributes = True


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    name: str


class Device(DeviceBase):
    id: int
    batteries: list[Battery] = []

    class Config:
        from_attributes = True
