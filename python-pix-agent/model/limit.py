from pydantic import BaseModel

from datetime import datetime

class LimitModel(BaseModel):
    value: int = 0
    last_update: datetime = datetime.now()
