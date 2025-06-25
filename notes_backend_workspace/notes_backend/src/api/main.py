from fastapi import FastAPI, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .models import Note, NoteCreate, NoteUpdate
from .storage import note_storage

app = FastAPI(
    title="Notes Backend API",
    description="A FastAPI backend for managing notes with CRUD operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "notes", "description": "CRUD endpoints for managing notes."},
        {"name": "health", "description": "Health check endpoint."},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"], summary="Health Check", description="Basic health check endpoint.")
def health_check():
    """Returns a simple health check message."""
    return {"message": "Healthy"}


# --- NOTES API ---

# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    status_code=200,
    summary="List all notes",
    description="Retrieves a list of all notes.",
    tags=["notes"],
)
def list_notes():
    """Returns a list of all notes."""
    return note_storage.list_notes()

# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=201,
    summary="Create a note",
    description="Creates a new note.",
    tags=["notes"],
)
def create_note(note: NoteCreate):
    """Create a new note with title and content."""
    return note_storage.create_note(note)

# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    status_code=200,
    summary="Get a note",
    description="Get a specific note by ID.",
    tags=["notes"],
)
def get_note(note_id: int = Path(..., gt=0, description="ID of the note")):
    """Get a note by its ID."""
    note = note_storage.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    status_code=200,
    summary="Update a note",
    description="Update the title and/or content of a specific note by ID.",
    tags=["notes"],
)
def update_note(note_id: int, note_update: NoteUpdate):
    """Update an existing note's title/content by ID."""
    note = note_storage.update_note(note_id, note_update)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=204,
    summary="Delete a note",
    description="Delete a note by its ID.",
    tags=["notes"],
)
def delete_note(note_id: int = Path(..., gt=0, description="ID of the note")):
    """Deletes a note by ID."""
    deleted = note_storage.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return None  # 204 response (no content)
