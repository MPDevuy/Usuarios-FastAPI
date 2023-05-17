from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schemas
from db.client import client_db
from bson import ObjectId


router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],
                    responses={status.HTTP_404_NOT_FOUND :{"message":"no encontrado"}})




users_list = []



@router.get("/", response_model= list[User])
async def users():
      return users_schemas(client_db.local.users.find()) 


# Usando Path 
@router.get("/{id}")
async def user(id:str):
   return search_user("_id", ObjectId(id))
    
# Usando Query hay que usar ?id=1 se concatena con & etc...
@router.get("/userquerydb/")
async def user(id:str):
   return search_user("_id", ObjectId(id))

#Usando Post para crear un usuario
@router.post("/",response_model=User, status_code= status.HTTP_201_CREATED)
async def user(user:User):

    if type(search_user("email".user.email)) == User:
              raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, detail= "Ya existe el Usuario")
      
 
   # transformamos el usuario en un diccionario
    user_dict = dict(user)
     
    del user_dict["id"]

   #conectar a la BD para insertar usuarios
    id =  client_db.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema (client_db.local.users.find_one({"_id":id})) #MongoDB crea el id con _id

    return User(**new_user)




#Usando Put para actualizar un usuario
@router.put("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def put_user(user:User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list [index] = user
            found = True

    if not found:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="No se Actualizo  Usuario" )
    else:
        return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):

    found = client_db.local.users.find_one_and_delete({"_id": ObjectId(id)})
           
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No a eliminado a el  Usuario" ) 

  
def search_user(Field: str, key):
    
    try:
        user = user_schema (client_db.local.users.find_one({Field: key}))              
        return User(**user_schema(user))
   
       
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")
    

