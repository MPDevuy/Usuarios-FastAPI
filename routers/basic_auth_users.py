from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

outh2 = OAuth2PasswordBearer(tokenUrl=("login")) #outh2 es un standard de seguridad se crea el token que autentica 


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password : str

users_db = {
    "martin": {
        "username": "tin900",
        "full_name": "Martin Pereira",
        "email": "tin900@hotmail.com",
        "disable": False,
        "password": "123456"
    } ,
     "pymue": {
        "username": "pymue",
        "full_name": "Pymue Cui",
        "email": "CuiCui@hotmail.com",
        "disable": True,
        "password": "123456"
    } ,
     "vale": {
        "username": "vale",
        "full_name": "Valentina Pereira",
        "email": "valemichi@outlook.com",
        "disable": False,
        "password": "123456"
    } 
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username]) #los ** significan que enviamos varios parametros a la peticion 
 
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])  #Solo devuelve el usuario sin la contraseña 
     
 #funcion que confirma la dependencia
async def current_user(token: str = Depends(outh2)):
    user =  search_user(token)
    if not user:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, 
             detail="Credenciales Invalidas",
            headers={"WWW-authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="Usuario Inactivo")
    
            
    return user




 #creamos instancia de la app mediante post y pedimos los datos por el form    
@router.post("/login_basic")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) #comprobamos usuario 
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="el Usuario no es correcto" )
    
    user = search_user_db(form.username)
    if not form.password == user.password: #comprobamos password
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="la contraseña no es correcta" ) 
    # access token permite generar un token para no tener que loguearnos constantemente con todos los datos
    return {"access.token": user.username, "token.type" : "bearer"}


# get para obtener usuario autenticado
@router.get("/users_basic/me")
async def me (user: User = Depends(current_user)):
    return user