from fastapi import FastAPI
from .routers.clientes import router_client
from .routers.bills import router_bills 
from .routers.transactions import router_transactions  
from .database import crear_tablas

app = FastAPI(lifespan=crear_tablas)

#Router Client

app.include_router(router_client, tags=["client"])

#Router Bill

app.include_router(router_bills, tags=["bill"])

#Router Transactions

app.include_router(router_transactions, tags=["transaction"])
