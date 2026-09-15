from fastapi import FastAPI,Depends,HTTPException
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
# Create Todos
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

# Get Todos

@app.get("/todos")
def get_todos(db:Session=Depends(get_db)):
    todo = db.query(Todo).all()
    return{
        "Total":len(todo),
        "data":todo
    }
# Get Specific Todo
@app.get("/todos/{todo_id}")
def get_todo(todo_id:int,db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todos not Found"
        )
    return{
        todo
    }

# Update todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int,title:str,completed:str,db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todos not Found"
        )
    todo.title = title
    todo.completed = completed
    db.commit()
    db.refresh(todo)
    return{
        "Message":"Todo Updated",
        "data":todo
    }

# Delete Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todos not Found"
        )

    db.delete(todo)
    db.commit()
    return{
        "Message":"Todo Deleted Successful"
    }