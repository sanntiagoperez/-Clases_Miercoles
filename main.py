from fastapi import FastAPI
from Model.clientes import (
    Cliente, 
    ClienteBase,
    ClienteCrear, 
    ClienteEditar,
    ClienteEliminar
)


app = FastAPI()

@app.get("/")
def home():
    return {"Mensaje": "Bienvenido a mi api de clientes"}

#Lista Temporal
lista_clientes: list[Cliente] = []

#LISTAR CLIENTE
@app.get("/clientes")
async def listar_clientes():
    return {"clientes": lista_clientes}

#CREAR CLIENTE
@app.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):

    cliente_val_id = len(lista_clientes) + 1

    #Crear clientes por id
    cliente_val = Cliente(id=cliente_val_id,
     **datos_cliente.model_dump()
     )
     
     
    lista_clientes.append(cliente_val)

    return cliente_val
@app.get("/clientes/{id}")
async def obtener_cliente(id: int):

    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    return{"Mensaje": "Cliente no encontrado"}

#Editar CLiente
@app.put("/clientes/{id}")
async def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):

        if obj_cliente.id == id:

            cliente_actualizado = Cliente(
                id=id, **datos_cliente.model_dump()
                )

            #Reemplazar cliente en lista
            lista_clientes[i] = cliente_actualizado

            return {"Mensaje": "Cliente actualizado correctamente", "cliente": cliente_actualizado}

    return {"mensaje": "Cliente no encontrado"}

#Elimminar Cliente
@app.delete("/clientes/{id}")
async def eliminar_clientes(id: int):

    for i, cliente in enumerate(lista_clientes):

        if cliente.id == id:

            lista_clientes.pop(i)

            return {"mensaje": f"Cliente {id} eliminado"}
             
    return {"mensaje": "Cliente no encontrado"}

