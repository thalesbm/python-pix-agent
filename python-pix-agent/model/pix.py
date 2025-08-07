from pydantic import BaseModel

class PixModel(BaseModel):
    key: str = ""
    has_key: bool = False
    value: str = ""
    has_value: bool = False
