from pydantic import BaseModel

from model.pix import PixModel
from model.receipt import ReceiptModel
from model.balance import BalanceModel
from model.limit import LimitModel

class GraphState(BaseModel):
    user_message: str
    intention: str = ""
    answer: str = ""

    limit: LimitModel = LimitModel()
    balance: BalanceModel = BalanceModel()
    receipt: ReceiptModel = ReceiptModel()
    pix: PixModel = PixModel()
