# TO RUN : - uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

import models
import database


#if the table does not exist create it
models.Base.metadata.create_all(bind = database.engine)


# Initialize the app
app = FastAPI()

class NoteSchema(BaseModel):
    title: str
    content: str

    # tells pydantic: It's okay to read data from a standard Python class object
    class Config:
        orm_mode = True


#Dependency ( databse session)
# if a requst comes in , it opens a connections
# and upon leaving it closes the connection

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/") 
def home():
    # We return a Python dictionary. 
    # FastAPI automatically converts this to JSON (data the web understands).
    return {"message": "Hello World from FastAPI"}


#API Endpoint to post data  ( POST )
@app.post("/notes" , response_model=NoteSchema)  
def create_note(note:NoteSchema ,db :Session = Depends(get_db)):

   new_note = models.NoteDB(title=note.title ,content = note.content)

    #add to db
   db.add(new_note)

    #save
   db.commit()

   #refresh to get generated ID
   db.refresh(new_note)

   return new_note


#API Endpoint to get all notes
@app.get("/notes", response_model= List[NoteSchema]) 
def read_notes(db: Session = Depends(get_db)):
    #Select * from notes
    notes = db.query(models.NoteDB).all()
    return notes

@app.get("/notes/{note_id}" , response_model=NoteSchema)
def read_note(note_id: int , db : Session = Depends(get_db)):
    note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note


@app.put("/notes/{note_id}" , response_model= NoteSchema)
def update_note(note_id: int, updated_note: NoteSchema, db :Session = Depends(get_db)):
    db_note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.title = updated_note.title
    db_note.content = updated_note.content

    db.commit()

    db.refresh(db_note)
    return db_note



@app.delete("/notes/{note_id}",response_model= NoteSchema)
def delete_note(note_id : int , db: Session = Depends(get_db)):
    db_note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404 , detail = "Note not found")
    
    db.delete(db_note)
    db.commit()
    
    return {"message": "Note deleted successfully"}
