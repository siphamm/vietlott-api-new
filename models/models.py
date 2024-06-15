from pydantic import BaseModel


class AddResultInput(BaseModel):
    lottery_type: str
    date: str
    result: str
