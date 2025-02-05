from pydantic import BaseModel


class UserTokenInfo(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str


class SignupPayload(BaseModel):
    username: str
    email: str
    password: str
    firstName: str
    lastName: str
    phone: str
