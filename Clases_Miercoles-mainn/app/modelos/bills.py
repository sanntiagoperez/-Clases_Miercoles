from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from .cliente import Clientt, clientread
from .transactions import transactiont
from datetime import datetime

class BillBase(SQLModel):
    date: datetime = Field(default_factory=datetime.now)

class createbill(BillBase):
    pass

class updatebill(BillBase):
    pass

class bills(BillBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    client_id: int = Field(default=None, foreign_key="clientt.id")
    
    client: Clientt = Relationship(back_populates="bill")
    transactions: list[transactiont] = Relationship(back_populates="bill")

class billread(BillBase):
    id: int 
    client: clientread | None = None

    @computed_field
    @property
    def vr_total(self) -> float:
        transacciones = getattr(self, "transactions", None)
        
        if not transacciones:
            return 0.0
            
        total_bill = 0.0
        for transaction in transacciones:
            total_bill += transaction.unitari_value * transaction.cantidad
            
        return total_bill

class billreadcompuesta(billread):
    transactions: list[transactiont] = []