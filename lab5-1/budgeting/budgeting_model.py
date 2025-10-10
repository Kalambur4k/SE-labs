from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IncomeCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма дохода")
    description: str = Field(..., min_length=1, max_length=255)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма расхода")
    description: str = Field(..., min_length=1, max_length=255)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# Base class for responses to enable ORM mode
class BaseResponse(BaseModel):
    class Config:
        orm_mode = True

class IncomeResponse(BaseResponse):
    id: int
    amount: float
    description: str
    user_id: int
    created_at: Optional[datetime] = None

class ExpenseResponse(BaseResponse):
    id: int
    amount: float
    description: str
    user_id: int
    created_at: Optional[datetime] = None


# Модель общего бюджета (если используется как агрегат)
class Budget(BaseModel):
    incomes: List[IncomeResponse] = []
    expenses: List[ExpenseResponse] = []