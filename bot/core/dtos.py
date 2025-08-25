from pydantic import BaseModel


class UsersMeDTO(BaseModel):
    tg_id: int
    is_superuser: bool
