from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/users",
                   tags=["users"],
                    responses={404 :{"message":"no encontrado"}})


# Iniciar el Server: uvicorn users:app --reload

#Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int
#Basemodel crea un json con los datos de la lista 

users_list = [User(id=1, name="Martin",surname="Pereira",url="https//martindev.com",age= 47 ),
         User(id=2,name="Vale",surname="Pereira",url="https//valentinagamer.com",age= 7 ),
         User(id=3,name="Pymue",surname="Cui",url="https//compasto.com", age= 3 ),]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Martin", "surname": "Pereira", "url": "https//Martindev.com"},
            {"name": "Vale", "surname": "Pereira", "url": "https//Valentinagamer.com"},
            {"name": "Pymue", "surname": "Cui", "url": "https//Comopasto.com"}]

@router.get("/users")
async def users():
      return users_list   


# Usando Path 
@router.get("/user/{id}")
async def user(id:int):
   return search_user(id)
    
# Usando Query hay que usar ?id=1 se concatena con & etc...
@router.get("/userquery/")
async def user(id:int):
   return search_user(id)

#Usando Post para crear un usuario
@router.post("/user",response_model=User, status_code=201)
async def p_user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="Ya existe el Usuario" )
        
    else:
        users_list.append (user)
        return user

#Usando Put para actualizar un usuario
@router.put("/user", response_model=User, status_code=201)
async def put_user(user:User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list [index] = user
            found = True

    if not found:
        raise HTTPException(status_code=304, detail="No se Actualizo  Usuario" )
    else:
        return user

#USando Delete o para eliminar es mejor usar un Path en vez de query
# Se busca el id en este caso del usuario para eliminarlo    
@router.delete("/user/{id}",status_code=204)
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list): #Busca usuario para eliminarlo 
        if saved_user.id == id:
            del users_list [index]  #del elimina usuario de la lista
            found = True
            raise HTTPException(status_code=204, detail="Se elimino el  Usuario" )
        
    if not found:
        raise HTTPException(status_code=404, detail="No a eliminado a el  Usuario" ) 

# busca usuario mediante el id con filter si no  lo encuentra sale Error 
# filter se puede usar para buscar objetos en una lista   
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list )
    try:
        return list(users)[0]
    except:
        return{"Error": "No se ha encontrado el usuario"}