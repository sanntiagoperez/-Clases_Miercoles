from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..database import Sesion_dependencia
from ..modelos.cliente import Clientt, Clientcreate, Clientupdate
from ..list import list_client

router_client = APIRouter()

@router_client.get("/clients", response_model=list[Clientt])
async def list_clients(sesion: Sesion_dependencia):
    clients = sesion.exec(select(Clientt)).all()
    return clients

@router_client.get(
        "clients/{client_id}",
        response_model=(Clientt)
)
async def listar_client(client_id: int, sesion: Sesion_dependencia):
    client_bd = sesion.get(Clientt, client_id)
    if not client_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=f"No existe el cliente"
            )
    return client_bd

@router_client.post("/client/{client_id}", response_model=Clientt)
async def create_client(data_client: Clientcreate, sesion: Sesion_dependencia):
    client_val = Clientt.model_validate(data_client.model_dump())
    sesion.add(client_val)
    sesion.commit()
    sesion.refresh(client_val)
    return client_val

@router_client.patch("/client/{client_id}", response_model=Clientt)
async def alter_client(client_id: int, data_client: Clientupdate, sesion: Sesion_dependencia):
    client_bd = sesion.get(Clientt, client_id)
    if not client_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=f"No existe el cliente"
            )
    client_dict = data_client.model_dump(exclude_unset=True)
    client_bd.sqlmodel_update(client_dict)
    sesion.add(client_bd)
    sesion.commit()
    sesion.refresh(client_bd)
    return client_bd
    
@router_client.delete("/client/{client_Id}", response_model=Clientt)
async def delete_client(client_id: int, sesion: Sesion_dependencia):
    client_bd = sesion.get(Clientt, client_id)
    if not client_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=f"No existe el cliente"
            )
    sesion.delete(client_bd)
    sesion.commit()
    return client_bd