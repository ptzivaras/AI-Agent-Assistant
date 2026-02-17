"""
API routes for ticket operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.app.database import get_db
from app.app.schemas import (
    TicketCreate,
    TicketResponse,
    TicketListResponse,
    TicketStatsResponse
)
from app.app.services import AIService
from app.app.crud import (
    create_ticket,
    get_ticket,
    get_tickets,
    get_tickets_count,
    get_tickets_stats
)
from app.app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket with AI classification"
)
async def create_new_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new ticket and automatically classify it using AI.
    
    The AI will analyze the message and return:
    - **category**: Type of issue (Technical, Billing, Feature Request, etc.)
    - **urgency**: Priority level (Low, Medium, High, Critical)
    - **sentiment**: User sentiment (Positive, Neutral, Negative)
    - **confidence**: AI confidence score (0.0 to 1.0)
    
    Example:
    ```json
    {
        "user_message": "My application crashes when I upload large files. This is urgent!"
    }
    ```
    """
    try:
        logger.info(f"Creating new ticket with message length: {len(ticket_data.user_message)}")
        
        # Call AI service for classification
        ai_service = AIService()
        ai_result = await ai_service.classify_ticket(ticket_data.user_message)
        
        # Create ticket in database
        db_ticket = create_ticket(
            db=db,
            user_message=ticket_data.user_message,
            classification=ai_result["classification"],
            ai_raw_response=ai_result["raw_response"],
            model_version=ai_result["model_version"]
        )
        
        logger.info(f"Ticket created successfully with ID: {db_ticket.id}, Category: {db_ticket.category}")
        return db_ticket
        
    except Exception as e:
        logger.error(f"Failed to create ticket: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {str(e)}"
        )


@router.get(
    "",
    response_model=TicketListResponse,
    summary="Get list of tickets with filtering and pagination"
)
async def list_tickets(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records"),
    category: Optional[str] = Query(None, description="Filter by category"),
    urgency: Optional[str] = Query(None, description="Filter by urgency level"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence score"),
    db: Session = Depends(get_db)
):
    """
    Get a list of tickets with optional filtering.
    
    Filters:
    - **category**: Filter by specific category
    - **urgency**: Filter by urgency level (Low, Medium, High, Critical)
    - **min_confidence**: Only show tickets with confidence >= this value
    
    Pagination:
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum records to return (1-100)
    """
    logger.info(f"Listing tickets with filters - category: {category}, urgency: {urgency}, min_confidence: {min_confidence}")
    
    tickets = get_tickets(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        urgency=urgency,
        min_confidence=min_confidence
    )
    
    total = get_tickets_count(
        db=db,
        category=category,
        urgency=urgency,
        min_confidence=min_confidence
    )
    
    return TicketListResponse(
        total=total,
        tickets=tickets,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/stats",
    response_model=TicketStatsResponse,
    summary="Get ticket statistics"
)
async def ticket_statistics(db: Session = Depends(get_db)):
    """
    Get aggregate statistics about all tickets:
    - Total number of tickets
    - Count grouped by category
    - Count grouped by urgency level
    - Average AI confidence score
    """
    logger.info("Fetching ticket statistics")
    stats = get_tickets_stats(db)
    
    return TicketStatsResponse(
        total_tickets=stats["total_tickets"],
        by_category=stats["by_category"],
        by_urgency=stats["by_urgency"],
        avg_confidence=stats["avg_confidence"]
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Get a specific ticket by ID"
)
async def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific ticket by its ID.
    
    Returns full ticket details including:
    - User message
    - AI classification results
    - Confidence score
    - Model version used
    - Creation timestamp
    """
    logger.info(f"Fetching ticket with ID: {ticket_id}")
    ticket = get_ticket(db, ticket_id)
    
    if not ticket:
        logger.warning(f"Ticket not found: {ticket_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found"
        )
    
    return ticket
