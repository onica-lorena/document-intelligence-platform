from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from app.core.config import settings


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
    ) -> str:
        extension = Path(file.filename).suffix

        filename = f"{uuid.uuid4()}{extension}"

        destination = self.storage_path / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return filename