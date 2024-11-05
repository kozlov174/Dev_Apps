from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import psycopg2

conn_db = psycopg2.connect("postgresql://user:12345@127.0.0.1:5432/my_project")

app = FastAPI()

class Pharmacy(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    telegram_chat: str
    #affordable_medicines:

class Medicine(BaseModel):
    id: int
    name: str
    reception_date: str
    receipt: bool
    form: str


@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(url='/docs')

@app.get("/all_pharmacies")
def get_all_pharmacies():
    cursor = conn_db.cursor()
    cursor.execute('SELECT * FROM pharmacy')
    return cursor.fetchall()
@app.get("/current_pharmacy")
def get_current_pharmacy(id):
    cursor = conn_db.cursor()
    cursor.execute('SELECT * FROM pharmacy WHERE id = %s', (id,))
    return cursor.fetchone()

@app.post("/add_pharmacy")
def add_pharmacy(name, address, phone, telegram_chat):
    cursor = conn_db.cursor()
    cursor.execute('INSERT INTO pharmacy (name, address, phone, telegram_chat) VALUES (%s, %s, %s, %s);', (name,address,phone,telegram_chat))
    conn_db.commit()
    cursor.close()
    return "Аптека успешно добавлена"

@app.post("/delete_pharmacy")
def delete_pharmacy(id):
    cursor = conn_db.cursor()
    cursor.execute('DELETE FROM pharmacy WHERE id = %s', (id,))
    conn_db.commit()
    cursor.close()
    return "Аптека успешно удалена"

@app.post("/update_pharmacy")
def update_pharmacy(id, name, address, phone, telegram_chat):
    cursor = conn_db.cursor()
    cursor.execute('UPDATE pharmacy WHERE id = %s SET name=%s, address=%s, phone=%s, telegram_chat=%s ', (id, name, address, phone, telegram_chat))
    conn_db.commit()
    cursor.close()
    return "Информация обновлена"