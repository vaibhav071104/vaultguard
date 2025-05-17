from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TransferRequest(BaseModel):
    recipient_username: str
    amount: float
    

class TransactionCreate(BaseModel):
    type: str  # deposit, withdraw, transfer
    amount: float
    target_username: Optional[str] = None

# schemas.py
class TransactionOut(BaseModel):
    id: int
    type: str
    amount: float
    timestamp: datetime.datetime
    flagged: bool
    flag_reason: Optional[str] = None  # <-- add this line

    class Config:
        orm_mode = True

class WalletOut(BaseModel):
    balance: float
    transactions: List[TransactionOut]
