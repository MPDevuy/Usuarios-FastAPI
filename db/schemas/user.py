def user_schema (user) -> dict:
    return { "id": str(user["_id"]),
            "username": user ["username"],
            "email": user ["email"]  }

#se puede traer directamente User sin que sea el dict

def users_schemas(users) -> list:
    return [user_schema(user) for user in users ]