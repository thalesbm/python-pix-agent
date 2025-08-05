from pydantic import BaseModel

class GraphState(BaseModel):
    input: str
    output: str