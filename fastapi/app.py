from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session

import uvicorn
import models

# instance of FastAPI class
app = FastAPI()

# Create all tables stored in this metadata
models.Base.metadata.create_all(bind=engine, checkfirst=True)

# sets the templates folder for the app
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    # starts a database connection session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # closes database connection


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """
    Function to render base.html at route '/' as a get request and displays all records from todo table
    Args:
        request (Request): request in path operation that will return a template
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        TemplateResponse: render base.html
    """
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse(
        "base.html", {"request": request, "todo_list": todos}
    )


@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    """
    Function to render base.html at route '/add' as a post request and add new record to todo table
    Args:
        request (Request): request in path operation that will return a template
        title: tasks title to add
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        TemplateResponse: redirect to the '/' after adding records.
    """
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Function to render base.html at route '/update/{todo_id}' as a get request and update existing record from todo table
    Args:
        request (Request): request in path operation that will return a template
        todo_id (int): task id to update details
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        TemplateResponse: redirect to the '/' after updating records.
    """
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Function to render base.html at route '/delete/{todo_id}' as a get request and delete existing record from todo table
    Args:
        request (Request): request in path operation that will return a template
        todo_id (int): task id to delete details
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        TemplateResponse: redirect to the '/' after deleting records.
    """
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app=app)
