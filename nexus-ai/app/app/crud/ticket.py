"""
CRUD operations for Ticket model
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List, Dict
from app.app.models.ticket import Ticket
from app.app.schemas import AIClassification


def create_ticket(
    db: Session,
    user_message: str,
    classification: AIClassification,
    ai_raw_response: str,
    model_version: str
) -> Ticket:
    """
    Create a new ticket with AI classification results
    
    Args:
        db: Database session
        user_message: Original user message
        classification: AI classification result
        ai_raw_response: Raw JSON response from AI
        model_version: AI model version used
        
    Returns:
        Created Ticket object
    """
    db_ticket = Ticket(
        user_message=user_message,
        category=classification.category,
        urgency=classification.urgency,
        sentiment=classification.sentiment,
        confidence=classification.confidence,
        ai_raw_response=ai_raw_response,
        model_version=model_version
    )
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket


def get_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    """
    Get a single ticket by ID
    
    Args:
        db: Database session
        ticket_id: Ticket ID
        
    Returns:
        Ticket object or None if not found
    """
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_tickets(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    urgency: Optional[str] = None,
    min_confidence: Optional[float] = None
) -> List[Ticket]:
    """
    Get list of tickets with optional filtering and pagination
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        category: Filter by category (optional)
        urgency: Filter by urgency level (optional)
        min_confidence: Filter by minimum confidence score (optional)
        
    Returns:
        List of Ticket objects
    """
    query = db.query(Ticket)
    
    # Apply filters
    if category:
        query = query.filter(Ticket.category == category)
    
    if urgency:
        query = query.filter(Ticket.urgency == urgency)
    
    if min_confidence is not None:
        query = query.filter(Ticket.confidence >= min_confidence)
    
    # Order by created_at descending (newest first)
    query = query.order_by(desc(Ticket.created_at))
    
    # Apply pagination
    return query.offset(skip).limit(limit).all()


def get_tickets_count(
    db: Session,
    category: Optional[str] = None,
    urgency: Optional[str] = None,
    min_confidence: Optional[float] = None
) -> int:
    """
    Get total count of tickets with optional filtering
    
    Args:
        db: Database session
        category: Filter by category (optional)
        urgency: Filter by urgency level (optional)
        min_confidence: Filter by minimum confidence score (optional)
        
    Returns:
        Total count of tickets matching filters
    """
    query = db.query(func.count(Ticket.id))
    
    if category:
        query = query.filter(Ticket.category == category)
    
    if urgency:
        query = query.filter(Ticket.urgency == urgency)
    
    if min_confidence is not None:
        query = query.filter(Ticket.confidence >= min_confidence)
    
    return query.scalar()


def get_tickets_stats(db: Session) -> Dict:
    """
    Get aggregate statistics about tickets
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with statistics:
        - total_tickets: Total number of tickets
        - by_category: Count grouped by category
        - by_urgency: Count grouped by urgency
        - avg_confidence: Average confidence score
    """
    # Total tickets
    total = db.query(func.count(Ticket.id)).scalar()
    
    # Count by category
    category_counts = db.query(
        Ticket.category,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.category).all()
    
    by_category = {cat: count for cat, count in category_counts}
    
    # Count by urgency
    urgency_counts = db.query(
        Ticket.urgency,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.urgency).all()
    
    by_urgency = {urg: count for urg, count in urgency_counts}
    
    # Average confidence
    avg_conf = db.query(func.avg(Ticket.confidence)).scalar()
    avg_confidence = round(float(avg_conf), 3) if avg_conf else 0.0
    
    return {
        "total_tickets": total,
        "by_category": by_category,
        "by_urgency": by_urgency,
        "avg_confidence": avg_confidence
    }
