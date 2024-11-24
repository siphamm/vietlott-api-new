from pydantic import BaseModel


class AddResultInput(BaseModel):
    date: str
    result: str
