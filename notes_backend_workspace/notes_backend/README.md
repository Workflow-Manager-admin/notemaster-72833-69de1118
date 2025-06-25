# notes_backend

## Overview

A FastAPI-based backend for managing notes. Provides RESTful CRUD endpoints for note creation, retrieval, update, and deletion.  
Currently uses in-memory storage (for prototyping), easily upgradeable to a database backend.

## Endpoints

- `GET /notes`: List all notes
- `POST /notes`: Create a new note
- `GET /notes/{note_id}`: Retrieve a specific note
- `PUT /notes/{note_id}`: Update an existing note
- `DELETE /notes/{note_id}`: Delete a note

See `/docs` or `/redoc` for full interactive OpenAPI docs.

## Configuration

- `.env.example`: Example environment variables for future DB configs.
- `requirements.txt`: Python dependencies.

## Running Locally

```sh
cd notes_backend_workspace/notes_backend
uvicorn src.api.main:app --reload
```

## Extending Storage

Replace `src/api/storage.py` with a real database repository.  
DB settings can be loaded from `.env`.

