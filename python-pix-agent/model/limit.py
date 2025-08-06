from pydantic import BaseModel

from datetime import datetime

class LimitModel(BaseModel):
    limit: int = 0
    last_update: datetime = datetime.now()
