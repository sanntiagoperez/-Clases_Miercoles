from pydantic import BaseModel

class Cliente(BaseModel):
    id:int
    fecha:str 
    total:float
    Cliente:str 