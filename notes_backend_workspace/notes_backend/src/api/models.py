from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base model for a note with title and content."""
    title: str = Field(..., description="Title of the note", max_length=255)
    content: Optional[str] = Field(None, description="Content/body of the note")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Model for note creation (input schema)."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Model for updating an existing note."""
    title: Optional[str] = Field(None, description="Title of the note", max_length=255)
    content: Optional[str] = Field(None, description="Content/body of the note")

# PUBLIC_INTERFACE
class Note(NoteBase):
    """Model representing a note with database fields."""
    id: int = Field(..., description="Unique ID of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        orm_mode = True

