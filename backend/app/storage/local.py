from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from app.core.config import settings
from app.models.storage import StoredFile

class LocalStorage:

    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save(
        self,
        file: UploadFile,
    ) -> StoredFile:
        extension = Path(file.filename).suffix

        stored_filename = f"{uuid.uuid4()}{extension}"

        destination = self.storage_path / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return StoredFile(
            stored_filename=stored_filename,
            storage_path=str(destination),
            file_size=destination.stat().st_size,
        )