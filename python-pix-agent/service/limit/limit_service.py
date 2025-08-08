from model.limit import LimitModel

from datetime import datetime

class LimitService:
    
    def __init__(self):
        pass
    
    def update(self, limit: LimitModel):
        self.limit = limit

    def get(self) -> LimitModel:
        
        limit = LimitModel()
        limit.value = 1000
        limit.last_update = datetime.now()
        
        return limit
        
