from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str
    edad: int
    descripcion: str | None = None


class ClienteCrear(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int


class ClienteEditar(ClienteBase):
    pass

class ClienteEliminar(ClienteBase):
    id:int
