from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy import select
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind =  engine)

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class UpdateTaskBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]

class taskIdBase(BaseModel):
    task_id : Optional[int] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/tasks')
async def create_task(task: TaskBase, db: Session = Depends(get_db)):
    db_task = models.Task(title = task.title, description = task.description, completed= task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)


@app.get('/tasks')
async def get_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(models.Task)).scalars().all()
    return tasks

@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task: UpdateTaskBase, db: Session = Depends(get_db)):
    # Retrieve the existing task
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    # If the task with the given ID doesn't exist, return an error
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task ID not found")
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task ID not found")
    db.delete(db_task)
    db.commit()

    return {"detail": "Task deleted successfully"}
    

