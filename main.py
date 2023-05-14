from fastapi import FastAPI
from routers import productos, users, basic_auth_users, jwt_auth_users, usersDB
from fastapi.staticfiles import StaticFiles  #para recursos estaticos (imagenes,etc)


app = FastAPI()

#Routers
app.include_router(productos.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)

app.include_router(jwt_auth_users.router)

app.include_router(usersDB.router)



app.mount("/static", StaticFiles(directory="static"),name="static") #mount establece path 



@app.get("/")
async def root():
    return "Hola MartinDev Bienvenido de a este mundo"

@app.get("/vale")
async def vale():
    return "Vale es una niña amorosa, que le gustan los gatos y gatas"          

@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

# Iniciar el Server: uvicorn main:app --reload
# Detener el Server: ctrl+C

# Documentacion Swagger: http://127.0.0.1:8000/docs
# Documentacion Redocly: http://127.0.0.1:8000/redoc
