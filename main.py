from fastapi import FastAPI
from pydantic import BaseModel


# TO RUN : - uvicorn main:app --reload

# Initialize the app
app = FastAPI()

class Note(BaseModel):
    title: str
    content: str


my_notes = []

@app.get("/") 
def home():
    # We return a Python dictionary. 
    # FastAPI automatically converts this to JSON (data the web understands).
    return {"message": "Hello World from FastAPI"}


#API Endpoint to post data  ( POST )
@app.post("/notes")  
def create_note(new_note:Note):
    my_notes.append(new_note)

    return {"message:" : " Note added successfuly","Data": new_note}


#API Endpoint to get all notes
@app.get("/notes") 
def get_all_notes():
    return {"count: " : len(my_notes) , "notes" : my_notes}


#API Endpoint to read a specific note ( GET )
@app.get("/notes/{note_id}")
def get_note(note_id :int):
    if note_id < 0 or note_id >= len(my_notes):
        return {"message: " : "Note Not Found!"}
    return my_notes[note_id]


#API Endpoint to update a Note ( PUT )
@app.put("/notes/{note_id}")
def update_note(note_id:int, updated_note : str):
    if note_id < 0 or note_id >= len(my_notes):
        return {"message: " : "Note not Found!"}
    
    my_notes[note_id] = update_note

    return {"message: " : "Note updated"}


#API Endpoint to delte a node ( DELETE )
@app.delete("/notes/{note_id}")
def delete_note(note_id : int):
    if note_id < 0 or note_id >= len(my_notes):
        return {"message: " : "Note not Found!"}
    
    my_notes.pop(note_id)

    return {"message: " : "Note deleted"}





