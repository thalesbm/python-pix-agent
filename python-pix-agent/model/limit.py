from pydantic import BaseModel, Field
from typing import Optional

from datetime import datetime

class LimitModel(BaseModel):
    value: Optional[int] = Field(default=None)
    has_limit: bool = False
    last_update: datetime = datetime.now()
