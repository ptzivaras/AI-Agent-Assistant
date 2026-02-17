"""
Pydantic schemas for Ticket validation and responses
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal


class TicketCreate(BaseModel):
    """Schema for creating a new ticket"""
    user_message: str = Field(
        ..., 
        min_length=10,
        max_length=5000,
        description="User's problem description (minimum 10 characters)",
        examples=["My application crashes when I try to upload files larger than 10MB"]
    )

    @field_validator('user_message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Remove extra whitespace and validate message content"""
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Message must be at least 10 characters long")
        return v


class AIClassification(BaseModel):
    """Schema for AI classification results (structured output)"""
    category: str = Field(
        ...,
        description="Ticket category",
        examples=["Technical Issue", "Billing", "Feature Request", "Account", "Bug Report"]
    )
    urgency: Literal["Low", "Medium", "High", "Critical"] = Field(
        ...,
        description="Urgency level based on message content"
    )
    sentiment: Literal["Positive", "Neutral", "Negative"] = Field(
        ...,
        description="Detected sentiment from user message"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="AI confidence score (0.0 to 1.0)"
    )

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0 and 1"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return round(v, 3)  # Round to 3 decimal places


class TicketResponse(BaseModel):
    """Schema for ticket response"""
    id: int = Field(..., description="Ticket ID")
    user_message: str = Field(..., description="Original user message")
    category: str = Field(..., description="AI-classified category")
    urgency: str = Field(..., description="AI-classified urgency level")
    sentiment: str = Field(..., description="AI-detected sentiment")
    confidence: float = Field(..., description="AI confidence score")
    model_version: str = Field(..., description="AI model version used")
    created_at: datetime = Field(..., description="Timestamp of ticket creation")

    class Config:
        from_attributes = True  # Allow ORM model conversion


class TicketListResponse(BaseModel):
    """Schema for paginated ticket list"""
    total: int = Field(..., description="Total number of tickets")
    tickets: list[TicketResponse] = Field(..., description="List of tickets")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class TicketStatsResponse(BaseModel):
    """Schema for ticket statistics"""
    total_tickets: int = Field(..., description="Total number of tickets")
    by_category: dict[str, int] = Field(..., description="Count by category")
    by_urgency: dict[str, int] = Field(..., description="Count by urgency")
    avg_confidence: float = Field(..., description="Average confidence score")
