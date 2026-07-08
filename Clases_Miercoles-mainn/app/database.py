from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine

sqlite_nombre = "bd_clientes.sqlite3"
sqlite_url = f"sqlite:///{sqlite_nombre}"

motor_bd = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@asynccontextmanager
async def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield

def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion

Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]

#https://sqlmodel.tiangolo.com/