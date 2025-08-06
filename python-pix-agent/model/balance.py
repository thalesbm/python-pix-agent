from pydantic import BaseModel

class BalanceModel(BaseModel):
    value: int = 0
