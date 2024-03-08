from app.api.models.users import User
from app.api.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User