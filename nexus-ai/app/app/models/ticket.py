"""
Ticket Model for AI Classification System
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.app.database import Base


class Ticket(Base):
    """
    Ticket model for storing user issues with AI classification results
    
    Fields:
    - id: Primary key
    - user_message: Original user problem/message
    - category: AI-classified category (e.g., "Technical", "Billing", "Feature Request")
    - urgency: AI-classified urgency level (e.g., "Low", "Medium", "High", "Critical")
    - sentiment: AI-detected sentiment (e.g., "Positive", "Neutral", "Negative")
    - confidence: AI confidence score (0.0 to 1.0)
    - ai_raw_response: Raw JSON response from AI model
    - model_version: AI model used (e.g., "gpt-4", "claude-3")
    - created_at: Timestamp of ticket creation
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_message = Column(Text, nullable=False, comment="Original user problem message")
    
    # AI Classification Results
    category = Column(String(100), nullable=False, index=True, comment="AI-classified category")
    urgency = Column(String(50), nullable=False, index=True, comment="AI-classified urgency level")
    sentiment = Column(String(50), nullable=False, comment="AI-detected sentiment")
    
    # AI Metadata
    confidence = Column(Float, nullable=False, comment="AI confidence score (0.0-1.0)")
    ai_raw_response = Column(Text, nullable=True, comment="Raw JSON response from AI")
    model_version = Column(String(100), nullable=False, comment="AI model version used")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="Ticket creation timestamp")

    def __repr__(self):
        return f"<Ticket(id={self.id}, category={self.category}, urgency={self.urgency}, confidence={self.confidence:.2f})>"
