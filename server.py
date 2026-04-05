from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Показываем картинки из папки images
app.mount("/img", StaticFiles(directory="img"), name="img")

# Показываем главную страницу
@app.get("/")
async def read_root():
    return FileResponse("index.html")

BOT_TOKEN = "8210952031:AAHDWNmBnuSf-uuk59mkqOln-FONCRoLaIo"
YOUR_CHAT_ID = "5334299531"

class Order(BaseModel):
    type: str
    area: str
    rooms: str
    phone: str

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.post("/api/order")
async def create_order(order: Order):
    msg_to_admin = (
        f"🚨 <b>НОВЫЙ ЗАКАЗ (МИНСК)</b> 🚨\n\n"
        f"<b>Полотно:</b> {order.type}\n"
        f"<b>Площадь:</b> {order.area} м²\n"
        f"<b>Комнат:</b> {order.rooms} шт.\n"
        f"<b>Телефон:</b> {order.phone}\n\n"
        f"👉 <i>Срочно звони!</i>"
    )
    send_telegram_message(msg_to_admin)
    return {"status": "success", "message": "Заказ отправлен"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
