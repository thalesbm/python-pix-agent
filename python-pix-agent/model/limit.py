from pydantic import BaseModel

from datetime import datetime

class LimitModel(BaseModel):
    value: int = None
    has_limit: bool = False
    last_update: datetime = datetime.now()
