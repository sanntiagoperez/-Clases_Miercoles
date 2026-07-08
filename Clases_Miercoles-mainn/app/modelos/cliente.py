from sqlmodel import SQLModel, Field, Relationship

class ClientBase(SQLModel):
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)
    description: str | None = Field(default=None)

class Clientcreate(ClientBase):
    pass

class Clientupdate(ClientBase):
    pass

class Clientt(ClientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bill: list["bills"] = Relationship(back_populates="client")

class clientread(ClientBase):
    id: int