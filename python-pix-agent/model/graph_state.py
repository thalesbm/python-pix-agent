from pydantic import BaseModel
from typing import List

class GraphState(BaseModel):
    user_message: str
    intention: str
    answer: str
    receipt: str