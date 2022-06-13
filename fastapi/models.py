from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Todo(Base):
    __tablename__ = "todos"  # sets table name
    id = Column(
        Integer, primary_key=True, index=True
    )  # id column [Storage Class - INTEGER, Primary key, Index]
    title = Column(String)  # title column [Storage Class - TEXT]
    complete = Column(
        Boolean, default=False
    )  # complete column [Storage Class - INTEGER]
