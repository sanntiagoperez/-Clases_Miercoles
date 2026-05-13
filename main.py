from fastapi import FastAPI
from Model.clientes import Cliente, ClienteCrear, ClienteEditar

app = FastAPI()

@app.get("/")
def home():
    return {"Mensaje": "Bienvenido a mi api de clientes"}

lista_clientes: list[Cliente] = []

@app.get("/clientes")
async def lista_clientes():
    return {"clientes": lista_clientes}

@app.post("/clientes")
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val_id = len(lista_clientes) + 1
    cliente_val = Cliente(id=cliente_val_id, **datos_cliente.model_dump())
    lista_clientes.append(cliente_val)
    return {"mensaje": "Cliente creado", "cliente": cliente_val}

@app.put("/clientes/{id}")
async def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            cliente_actualizado = Cliente(id=id, **datos_cliente.model_dump())
            lista_clientes[i] = cliente_actualizado
            return {"Mensaje": "Cliente actualizado correctamente", "cliente": cliente_actualizado}
    return {"mensaje": "Cliente no encontrado"}

@app.delete("/clientes/{id}")
async def eliminar_clientes(id: int):
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            cliente_eliminado = lista_clientes.pop(i)
            return {"mensaje": f"Cliente {id} eliminado", "cliente": cliente_eliminado}
    return {"mensaje": "Cliente no encontrado"}

@app.get("/clientes/{id}")
async def obtener_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    return {"mensaje": "Cliente no encontrado"}