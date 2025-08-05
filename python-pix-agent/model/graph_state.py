from pydantic import BaseModel
from typing import Optional, List

class GraphState(BaseModel):
    user_message: str
    intention: str
    answer: str
    receipt: str
    log: List[str]
    tipo: Optional[str] = None