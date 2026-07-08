from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from ..database import Sesion_dependencia
from ..modelos.bills import bills, createbill, billread, billreadcompuesta, updatebill
from ..modelos.cliente import Clientt
from ..list import list_client
from ..list import list_bill

router_bills = APIRouter()

@router_bills.get("/bills", response_model=list[billreadcompuesta])
async def Listar_bill(sesion: Sesion_dependencia):
    query = select(bills)
    listar_bill = sesion.exec(query).all()  
    return listar_bill

@router_bills.get("/bills/{bill_id}", response_model=billread)
async def obtener_bill_por_id(bill_id: int, sesion: Sesion_dependencia):
    bill_bd = sesion.get(bills, bill_id)
    if not bill_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No existe la factura"
        )
    return bill_bd

@router_bills.post("/bills/{client_id}", response_model=bills)
async def create_bill(client_id: int, data_bill: createbill, sesion: Sesion_dependencia):
    client_encontrado = sesion.get(Clientt, client_id)
    if not client_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente no encontrado"
        )
    
    bill_dict = data_bill.model_dump()
    bill_dict ["client_id"] = client_id
    bill_val = bills.model_validate(bill_dict)

    sesion.add(bill_val)
    sesion.commit()
    sesion.refresh(bill_val)
    return bill_val 

@router_bills.patch("/bills/{bill_id}", response_model=billread)
async def alter_bill(bill_id: int, data_bill: updatebill, sesion: Sesion_dependencia):
    bill_bd = sesion.get(bills, bill_id)
    if not bill_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la factura"
        )
    bill_dict = data_bill.model_dump(exclude_unset=True)
    bill_bd.sqlmodel_update(bill_dict)
    
    sesion.add(bill_bd)
    sesion.commit()
    sesion.refresh(bill_bd)
    return bill_bd

# Eliminar factura por ID
@router_bills.delete("/bills/{bill_id}", response_model=billread)
async def delete_bill(bill_id: int, sesion: Sesion_dependencia):
    bill_bd = sesion.get(bills, bill_id)
    if not bill_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la factura"
        )
    sesion.delete(bill_bd)
    sesion.commit()
    return bill_bd