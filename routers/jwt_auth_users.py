from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta 


# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]" 

# to get a string like this run:
# openssl rand -hex 32

# tipo de algoritmo usado para encriptar la contraseña
ALGORITHM = "HS256"  

#duracion del token de validacion
ACCESS_TOKEN_DURATION = 1

# los squemas definen el algoritmo de encriptacion
crypt = CryptContext(schemes=["bcrypt"])


SECRET = "jajdkadksjdksjdsjdofjdo"

router = APIRouter()

outh2 = OAuth2PasswordBearer(tokenUrl=("login"))  


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password : str


#generamos contraseña con bscrypt encryptamos 
users_db = {
    "martin": {
        "username": "tin900",
        "full_name": "Martin Pereira",
        "email": "tin900@hotmail.com",
        "disable": False,
        "password": "$2y$12$xKHbTHFPUKBKaSipj99ceuboW.vA0fygJLbI.i4KhWt1J6G7pCbo."
    } ,
     "pymue": {
        "username": "pymue",
        "full_name": "Pymue Cui",
        "email": "CuiCui@hotmail.com",
        "disable": True,
        "password": "$2y$12$ih864DuSQ5DWlyndxsXp1.HLv1k6MjhmJtXwUxqwF.SvzPyzBgcNC" #123456
    } ,
     "vale": {
        "username": "vale",
        "full_name": "Valentina Pereira",
        "email": "valemichi@outlook.com",
        "disable": False,
        "password": "$2y$12$rieUiIstxjD/5rYtdSwzX.m7hy/pagNphOIQQm0V82Oj8gaGhiyFC" #12345 #https://bcrypt.online/
    } 
}




def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username]) #los ** significan que enviamos varios parametros a la peticion 
 
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])  #Solo devuelve el usuario sin la contraseña 
     

async def auth_user(token: str = Depends(outh2)):

    exception =  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Credenciales Invalidas",
                headers={"WWW-authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
                raise exception

    except JWTError:
            raise exception
    
    return search_user(username)

 #funcion que confirma la dependencia
async def current_user( user: User = Depends(auth_user)):  
    if user.disable:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="Usuario Inactivo")
    
            
    return user




 #creamos instancia de la app mediante post y pedimos los datos por el form    
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) #comprobamos usuario 
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="el Usuario no es correcto" )
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password): #comprobamos password con crypt.verify
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="la contraseña no es correcta" ) 
    
    

    access_token = { "sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)

    }

    # access token permite generar un token para no tener que loguearnos constantemente con todos los datos
    return {"access_token": jwt.encode (access_token, SECRET, algorithm=ALGORITHM ),"token.type" : "bearer"}


# get para obtener usuario autenticado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user