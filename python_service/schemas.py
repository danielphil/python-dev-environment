from pydantic import BaseModel


class UserDetails(BaseModel):
    name: str


class User(UserDetails):
    id: int
