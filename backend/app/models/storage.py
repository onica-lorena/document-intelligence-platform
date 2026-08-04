from pydantic import BaseModel


class StoredFile(BaseModel):
    stored_filename: str
    storage_path: str
    file_size: int