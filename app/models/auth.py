from pydantic import BaseModel


class UserTokenInfo(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
