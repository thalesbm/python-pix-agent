from pydantic import BaseModel

from datetime import datetime

class LimitModel(BaseModel):
    value: int = None
    last_update: datetime = datetime.now()
