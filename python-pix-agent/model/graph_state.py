from pydantic import BaseModel

class GraphState(BaseModel):
    user_message: str
    limit: int = 0
    intention: str = ""
    answer: str = ""
    receipt: str = ""
    key: str = ""
    value: str = ""
