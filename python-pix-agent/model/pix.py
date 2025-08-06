from pydantic import BaseModel

class PixModel(BaseModel):
    key: str = ""
    value: str = ""
