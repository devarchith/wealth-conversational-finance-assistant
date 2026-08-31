from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field, field_validator


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: Role
    is_active: bool = True
    created_at: datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isalpha() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must include at least one letter and one number")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str = Field(min_length=32, max_length=256)
    new_password: str = Field(min_length=10, max_length=128)


class UserProfile(BaseModel):
    display_name: str = Field(default="", max_length=80)
    preferred_currency: str = Field(default="USD", min_length=3, max_length=3)
    timezone: str = Field(default="UTC", max_length=64)
    financial_literacy: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    avatar_url: str | None = Field(default=None, max_length=500)

    @field_validator("preferred_currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class FinancialGoal(BaseModel):
    id: str | None = None
    name: str = Field(min_length=1, max_length=100)
    target_amount: float = Field(gt=0, le=1_000_000_000)
    current_amount: float = Field(default=0, ge=0, le=1_000_000_000)
    target_date: date | None = None


class FinancialProfile(BaseModel):
    monthly_income: float = Field(default=0, ge=0, le=100_000_000)
    monthly_expenses: float = Field(default=0, ge=0, le=100_000_000)
    current_savings: float = Field(default=0, ge=0, le=1_000_000_000)
    monthly_investment: float = Field(default=0, ge=0, le=100_000_000)
    risk_tolerance: str = Field(default="moderate", pattern="^(conservative|moderate|aggressive)$")
    investment_horizon_months: int = Field(default=60, ge=1, le=1200)
    goals: list[FinancialGoal] = Field(default_factory=list, max_length=20)


class Entity(BaseModel):
    type: str
    value: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = None

    @field_validator("message")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be blank")
        return value


class ChatResponse(BaseModel):
    response: str
    intent: str
    entities: list[Entity]
    confidence: float = Field(ge=0, le=1)
    engine: str
    conversation_id: str
    disclaimer: str = "Educational information, not professional financial advice."


class Recommendation(BaseModel):
    category: str
    priority: str
    title: str
    explanation: str


class RecommendationSummary(BaseModel):
    monthly_surplus: float
    savings_rate: float | None
    expense_ratio: float | None
    emergency_fund_target: float
    emergency_fund_gap: float
    risk_profile: str
    goal_progress: list[dict]
    recommendations: list[Recommendation]


class HistoryItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    last_engine: str | None = None
    last_intent: str | None = None


class Page(BaseModel):
    items: list[HistoryItem]
    page: int
    page_size: int
    total: int

