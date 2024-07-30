from fastapi import FastAPI, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .database import SessionLocal, engine, Base
from .models import Device, Battery
from .crud import DBHandler
from .schemas import DeviceCreate, Device, BatteryCreate, Battery

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/devices")
def create_device(name: str = Form(...), db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    device = db_handler.add_device(name)
    return RedirectResponse(url=f"/devices/{device.id}", status_code=303)


@app.get("/devices", response_model=list[Device])
def read_devices(request: Request, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    devices = db_handler.get_devices()
    return templates.TemplateResponse("devices.html", {"request": request, "devices": devices})


@app.post("/devices/{device_id}")
def update_device(device_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    updated_device = db_handler.update_device(device_id, name)
    if updated_device is None:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return RedirectResponse(url=f"/devices/{device_id}", status_code=303)


@app.get("/devices/{device_id}", response_model=Device)
def read_device(device_id: int, request: Request, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    device = db_handler.get_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return templates.TemplateResponse("device.html", {"request": request, "device": device})


@app.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    device = db_handler.delete_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return {"message": "Устройство успешно удалено"}


@app.get("/batteries", response_model=list[Battery])
def read_batteries(request: Request, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    batteries = db_handler.get_batteries()
    return templates.TemplateResponse("batteries.html", {"request": request, "batteries": batteries})


@app.post("/batteries")
def create_battery(name: str = Form(...), device_id: int = Form(...), db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    try:
        battery = db_handler.add_battery(name, device_id)
        return RedirectResponse(url=f"/batteries/{battery.id}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batteries/{battery_id}")
def update_battery(battery_id: int, name: str = Form(...), device_id: int = Form(...), db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    updated_battery = db_handler.update_battery(battery_id, name, device_id)
    if updated_battery is None:
        raise HTTPException(status_code=404, detail="Батарея не найдена")
    return RedirectResponse(url=f"/batteries/{battery_id}", status_code=303)


@app.get("/batteries/{battery_id}", response_model=Battery)
def read_battery(battery_id: int, request: Request, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    battery = db_handler.get_battery(battery_id)
    if battery is None:
        raise HTTPException(status_code=404, detail="Батарея не найдена")
    return templates.TemplateResponse("battery.html", {"request": request, "battery": battery})


@app.post("/batteries/{battery_id}")
def update_battery(battery_id: int, name: str = Form(...), device_id: int = Form(...), db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    updated_battery = db_handler.update_battery(battery_id, name, device_id)
    if updated_battery is None:
        raise HTTPException(status_code=404, detail="Батарея не найдена")
    return RedirectResponse(url=f"/batteries/{battery_id}", status_code=303)


@app.delete("/batteries/{battery_id}")
def delete_battery(battery_id: int, db: Session = Depends(get_db)):
    db_handler = DBHandler(db)
    battery = db_handler.delete_battery(battery_id)
    if battery is None:
        raise HTTPException(status_code=404, detail="Батарея не найдена")
    return {"message": "Батарея успешно удалена"}
