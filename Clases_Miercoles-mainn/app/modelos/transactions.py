from sqlmodel import SQLModel, Field, Relationship

class transactions(SQLModel):
    cantidad: int = Field(default=0)
    unitari_value: float = Field(default=0.0)
    description: str | None = Field(default=None)

class transactioncreate(transactions):
    pass

class transactionalter(transactions):
    pass

class updatetransaction(transactions):
    pass

class transactiont(transactions, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bill_id: int = Field(foreign_key="bills.id")
    bill: list["bills"] = Relationship(back_populates="transactions")

class transactionread(transactions):
    id: int
    