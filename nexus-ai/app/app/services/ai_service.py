"""
AI Service for Ticket Classification

NOTE: This is a MOCK implementation for testing without AI API keys.
For production, replace with real OpenAI/Anthropic API calls.
"""
import json
import re
from typing import Dict, Any
from app.app.schemas import AIClassification
from app.app.logger import get_logger

logger = get_logger(__name__)


class AIService:
    """
    Mock AI Service for ticket classification
    Uses keyword-based rules to simulate AI classification
    
    TODO: Replace with real AI API (OpenAI/Anthropic) when API key is available
    """
    
    def __init__(self):
        self.model_version = "mock-classifier-v1.0"
        
        # Keywords for category classification
        self.category_keywords = {
            "Technical Issue": ["crash", "error", "bug", "not working", "broken", "failed", "freeze", "slow"],
            "Billing": ["payment", "invoice", "charge", "refund", "subscription", "price", "cost", "billing"],
            "Feature Request": ["feature", "add", "improve", "enhancement", "suggestion", "would like", "could you"],
            "Account": ["login", "password", "access", "account", "register", "sign in", "authentication"],
            "Bug Report": ["unexpected", "wrong", "incorrect", "issue", "problem", "glitch"],
        }
        
        # Keywords for urgency detection
        self.urgency_keywords = {
            "Critical": ["urgent", "critical", "immediately", "emergency", "asap", "production down", "can't work"],
            "High": ["important", "soon", "quickly", "priority", "blocking", "cannot"],
            "Medium": ["would like", "should", "need", "help"],
            "Low": ["whenever", "eventually", "minor", "small", "question"],
        }
        
        # Keywords for sentiment detection
        self.sentiment_keywords = {
            "Negative": ["frustrated", "angry", "terrible", "awful", "hate", "worst", "broken", "useless"],
            "Positive": ["thank", "great", "love", "excellent", "wonderful", "appreciate", "good"],
            "Neutral": [],  # Default
        }
    
    async def classify_ticket(self, user_message: str) -> Dict[str, Any]:
        """
        Classify a ticket using mock AI logic
        
        Args:
            user_message: User's problem description
            
        Returns:
            Dictionary with classification results and raw response
        """
        logger.info(f"Classifying ticket with message length: {len(user_message)}")
        
        try:
            message_lower = user_message.lower()
            
            # Classify category
            category = self._classify_category(message_lower)
            logger.debug(f"Classified category: {category}")
            
            # Classify urgency
            urgency = self._classify_urgency(message_lower)
            logger.debug(f"Classified urgency: {urgency}")
            
            # Detect sentiment
            sentiment = self._detect_sentiment(message_lower)
            logger.debug(f"Detected sentiment: {sentiment}")
            
            # Calculate confidence (mock - based on message length and keyword matches)
            confidence = self._calculate_confidence(message_lower, category, urgency, sentiment)
            logger.debug(f"Calculated confidence: {confidence}")
            
            # Create classification result
            classification = AIClassification(
                category=category,
                urgency=urgency,
                sentiment=sentiment,
                confidence=confidence
            )
            
            # Mock raw AI response (simulating structured output)
            raw_response = {
                "model": self.model_version,
                "classification": classification.model_dump(),
                "reasoning": f"Classified as {category} with {urgency} urgency based on content analysis",
                "mock": True  # Indicator that this is mock data
            }
            
            logger.info(f"Successfully classified ticket: {category} / {urgency} / {sentiment} (confidence: {confidence:.2f})")
            
            return {
                "classification": classification,
                "raw_response": json.dumps(raw_response),
                "model_version": self.model_version
            }
            
        except Exception as e:
            logger.error(f"Error during ticket classification: {str(e)}", exc_info=True)
            raise Exception(f"AI classification failed: {str(e)}")
    
    def _classify_category(self, message: str) -> str:
        """Classify message category based on keywords"""
        scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "General Inquiry"  # Default category
    
    def _classify_urgency(self, message: str) -> str:
        """Classify urgency level based on keywords"""
        for urgency, keywords in self.urgency_keywords.items():
            if any(keyword in message for keyword in keywords):
                return urgency
        
        return "Medium"  # Default urgency
    
    def _detect_sentiment(self, message: str) -> str:
        """Detect sentiment based on keywords"""
        for sentiment, keywords in self.sentiment_keywords.items():
            if any(keyword in message for keyword in keywords):
                return sentiment
        
        return "Neutral"  # Default sentiment
    
    def _calculate_confidence(self, message: str, category: str, urgency: str, sentiment: str) -> float:
        """
        Calculate mock confidence score
        Higher confidence if:
        - Message is longer (more context)
        - Multiple keywords matched
        - Clear indicators present
        """
        confidence = 0.5  # Base confidence
        
        # Length bonus (up to +0.2)
        length_bonus = min(len(message) / 500, 0.2)
        confidence += length_bonus
        
        # Keyword match bonus
        all_keywords = [kw for keywords in self.category_keywords.values() for kw in keywords]
        matches = sum(1 for keyword in all_keywords if keyword in message)
        keyword_bonus = min(matches * 0.05, 0.2)
        confidence += keyword_bonus
        
        # Non-default classification bonus
        if category != "General Inquiry":
            confidence += 0.1
        
        # Cap at 0.95 (never 100% confident in mock)
        return min(confidence, 0.95)


# TODO: Real AI Implementation Example (for when API key is available)
"""
class RealAIService:
    def __init__(self, api_key: str):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model_version = "gpt-4"
    
    async def classify_ticket(self, user_message: str) -> Dict[str, Any]:
        prompt = '''
        Classify the following support ticket:
        
        Message: {user_message}
        
        Return JSON with:
        - category: one of [Technical Issue, Billing, Feature Request, Account, Bug Report, General Inquiry]
        - urgency: one of [Low, Medium, High, Critical]
        - sentiment: one of [Positive, Neutral, Negative]
        - confidence: float between 0.0 and 1.0
        '''
        
        response = self.client.chat.completions.create(
            model=self.model_version,
            messages=[{"role": "user", "content": prompt.format(user_message=user_message)}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        classification = AIClassification(**result)
        
        return {
            "classification": classification,
            "raw_response": response.choices[0].message.content,
            "model_version": self.model_version
        }
"""
