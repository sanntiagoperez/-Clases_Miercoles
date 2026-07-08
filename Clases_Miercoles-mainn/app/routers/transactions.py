from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..modelos.transactions import transactiont, transactioncreate, transactionread, updatetransaction
from ..modelos.bills import bills
from ..database import Sesion_dependencia

router_transactions = APIRouter()

@router_transactions.get("/transactions", response_model=list[transactiont])
async def listar_transactions(sesion: Sesion_dependencia):
    query = select(transactiont)
    resultado = sesion.exec(query).all()
    return resultado

@router_transactions.post("/transactions/{bill_id}", response_model=transactiont)
async def create_transactions(bill_id: int, data_transaction: transactioncreate, sesion: Sesion_dependencia):
    bill_encontrado = sesion.get(bills, bill_id)
    if not bill_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="factura no encontrada"
        )

    transaction_dict = data_transaction.model_dump()
    transaction_dict["bill_id"] = bill_id
    transaction_val = transactiont.model_validate(transaction_dict)

    sesion.add(transaction_val)
    sesion.commit()
    sesion.refresh(transaction_val)
    return transaction_val

@router_transactions.get("/transactions/{transaction_id}", response_model=transactionread)
async def obtener_transaction(transaction_id: int, sesion: Sesion_dependencia):
    transaction_bd = sesion.get(transactiont, transaction_id)
    if not transaction_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )
    return transaction_bd

@router_transactions.patch("/transactions/{transaction_id}", response_model=transactionread)
async def alter_transaction(transaction_id: int, data_transaction: updatetransaction, sesion: Sesion_dependencia):
    transaction_bd = sesion.get(transactiont, transaction_id)
    if not transaction_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )
    
    transaction_dict = data_transaction.model_dump(exclude_unset=True)
    transaction_bd.sqlmodel_update(transaction_dict)
    
    sesion.add(transaction_bd)
    sesion.commit()
    sesion.refresh(transaction_bd)
    return transaction_bd

@router_transactions.delete("/transactions/{transaction_id}", response_model=transactionread)
async def delete_transaction(transaction_id: int, sesion: Sesion_dependencia):
    transaction_bd = sesion.get(transactiont, transaction_id)
    if not transaction_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )
    sesion.delete(transaction_bd)
    sesion.commit()
    return transaction_bd