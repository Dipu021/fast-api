from fastapi import FastAPI,Depends
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,Session,declarative_base

DATABASE_URL = "sqlite:///./test3.db"
app = FastAPI()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos")
def create_todos(title:str,db:Session=Depends(get_db)):
    todo = Todo(title=title,completed = "False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "Message":"Todo added successfully",
        "Data":todo
    }
