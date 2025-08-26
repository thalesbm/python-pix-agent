from pydantic import BaseModel
from typing import Optional, Literal

class PixModel(BaseModel):
    key: str = ""
    has_key: bool = False
    value: str = ""
    has_value: bool = False
    more_information: Optional[str] = None
