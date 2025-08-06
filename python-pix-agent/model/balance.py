from pydantic import BaseModel

class BalanceModel(BaseModel):
    balance: int = 0
