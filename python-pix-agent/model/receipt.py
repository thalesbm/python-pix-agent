from pydantic import BaseModel

class ReceiptModel(BaseModel):
    receipt_id: str = ""
