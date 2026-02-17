"""
CRUD operations for Nexus AI
"""
from .ticket import (
    create_ticket,
    get_ticket,
    get_tickets,
    get_tickets_count,
    get_tickets_stats
)

__all__ = [
    "create_ticket",
    "get_ticket", 
    "get_tickets",
    "get_tickets_count",
    "get_tickets_stats"
]
