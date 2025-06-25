from typing import Dict, List, Optional
from datetime import datetime
from threading import Lock

from .models import Note, NoteCreate, NoteUpdate

class InMemoryNoteStorage:
    """
    Thread-safe in-memory storage for notes, intended for development/demos.
    Can be replaced with a real DB implementation in future.
    """
    def __init__(self):
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1
        self._lock = Lock()

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """Returns a list of all notes."""
        with self._lock:
            return list(self._notes.values())

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Note]:
        """Returns a single note by ID, or None if not found."""
        with self._lock:
            return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def create_note(self, note_create: NoteCreate) -> Note:
        """Creates and returns a new Note."""
        now = datetime.utcnow()
        with self._lock:
            note = Note(
                id=self._next_id,
                title=note_create.title,
                content=note_create.content,
                created_at=now,
                updated_at=now
            )
            self._notes[self._next_id] = note
            self._next_id += 1
            return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
        """Updates the note with note_id. Returns updated Note, or None if not found."""
        with self._lock:
            note = self._notes.get(note_id)
            if note is None:
                return None
            data = note.model_dump()
            if note_update.title is not None:
                data["title"] = note_update.title
            if note_update.content is not None:
                data["content"] = note_update.content
            data["updated_at"] = datetime.utcnow()
            updated_note = Note(**data)
            self._notes[note_id] = updated_note
            return updated_note

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """Deletes the note with the given ID. Returns True if deleted, False if not found."""
        with self._lock:
            if note_id in self._notes:
                del self._notes[note_id]
                return True
            else:
                return False

# Expose a single instance for app-wide use
note_storage = InMemoryNoteStorage()
