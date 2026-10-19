from fastapi import FastAPI,status,Path,HTTPException
from pydantic import BaseModel
from typing import Union

app = FastAPI(
    title="Note-Api",
    version="1.0.0"
)
DBNOTES = {}

class NoteBase(BaseModel):
    title : str
    note : str
class NewNote(NoteBase):
    pass
class NotesOut(NoteBase):
    pass

@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
def check_status():
    return {"status" : "Online"}

@app.post(
    "/new_note",
    status_code=status.HTTP_201_CREATED
)
def create_new_note(note : NewNote) -> dict:
    note_db = note.model_dump()
    DBNOTES[note.title] = note_db
    response = {"message" : "Note Created!", "data":note}
    print(response)
    return response

@app.get(
        "/get-notes",
        status_code=status.HTTP_200_OK,
        response_model=Union[str, list[NotesOut]]
)
def get_all_notes():
    if DBNOTES is None:
        return "Notes have not been Added!"
    return list(DBNOTES.values())

@app.get(
    "/get_note/{note_title}",
    response_model=NotesOut,
    status_code=status.HTTP_200_OK
)
def get_specific_note(
    note_title : str = Path(...)
):
    note_db = DBNOTES.get(note_title)
    if not note_db:
        raise HTTPException(
            detail="Note not Found!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return note_db

@app.delete("/delete_note/{note_title}", status_code=status.HTTP_200_OK)
def delete_note(
    note_title : str = Path(...)
):
    if note_title not in DBNOTES:
        return {"message" : "Note does Not exist"}
    
    del DBNOTES[note_title]

    return {"Message":"Note deleted successfully"}

