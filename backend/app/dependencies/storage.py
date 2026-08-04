from app.storage.local import LocalStorage


def get_storage() -> LocalStorage:
    return LocalStorage()