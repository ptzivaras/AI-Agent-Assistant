"""
AI Service for Ticket Classification
Supports: OpenAI & Groq (Version 2.0)
"""
import json
from typing import Dict, Any
from openai import OpenAI
from app.app.schemas import AIClassification
from app.app.logger import get_logger
from app.app.config import settings

logger = get_logger(__name__)


class AIService:
    """
    AI Service supporting multiple providers (OpenAI, Groq)
    Groq API is OpenAI-compatible but FREE and faster!
    """
    
    def __init__(self):
        """Initialize AI client based on AI_PROVIDER setting"""
        provider = settings.ai_provider.lower()
        
        if provider == "groq":
            self._init_groq()
        elif provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unknown AI provider: {provider}. Use 'openai' or 'groq'")
    
    def _init_groq(self):
        """Initialize Groq client (FREE & Fast)"""
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file!")
        
        try:
            # Groq uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = settings.groq_model
            self.temperature = 0.7
            self.max_tokens = 500
            self.provider_name = "Groq"
            logger.info(f"✅ Groq AI Service initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq: {str(e)}")
            raise Exception(f"Groq initialization failed: {str(e)}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file!")
        
        try:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
            self.temperature = settings.openai_temperature
            self.max_tokens = settings.openai_max_tokens
            self.provider_name = "OpenAI"
            logger.info(f"✅ OpenAI AI Service initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {str(e)}")
            raise Exception(f"OpenAI initialization failed: {str(e)}")
    
    async def classify_ticket(self, user_message: str) -> Dict[str, Any]:
        """
        Classify a support ticket using AI
        
        Args:
            user_message: User's problem description
            
        Returns:
            Dictionary with classification results and raw response
        """
        logger.info(f"🤖 Classifying ticket with {self.provider_name} ({self.model}), message length: {len(user_message)}")
        
        try:
            # Create the classification prompt
            prompt = self._create_classification_prompt(user_message)
            
            # Call AI API (works for both OpenAI and Groq)
            logger.debug(f"Sending request to {self.provider_name} API...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert support ticket classifier. Analyze tickets and return structured JSON classification."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"} if self.provider_name == "OpenAI" else None
            )
            
            # Parse the response
            raw_content = response.choices[0].message.content
            logger.debug(f"Received response: {raw_content[:200]}...")
            
            # Clean and parse JSON (handles Groq markdown formatting)
            ai_result = self._extract_json(raw_content)
            
            # Validate and create classification object
            classification = self._parse_classification(ai_result)
            
            # Get model version from response
            model_version = f"{self.provider_name}/{response.model}"
            
            logger.info(
                f"✅ Classification complete: {classification.category} / "
                f"{classification.urgency} / {classification.sentiment} "
                f"(confidence: {classification.confidence:.2f})"
            )
            
            return {
                "classification": classification,
                "raw_response": raw_content,
                "model_version": model_version
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse AI JSON response: {str(e)}")
            raise Exception(f"Invalid JSON from {self.provider_name}: {str(e)}")
        except Exception as e:
            logger.error(f"❌ AI classification error: {str(e)}", exc_info=True)
            raise Exception(f"AI classification failed: {str(e)}")
    
    def _extract_json(self, raw_content: str) -> Dict[str, Any]:
        """
        Extract JSON from AI response (handles markdown code blocks)
        
        Args:
            raw_content: Raw response from AI
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try direct JSON parse first
            return json.loads(raw_content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            import re
            
            # Look for ```json ... ``` or ``` ... ```
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
            if json_match:
                logger.debug("Extracted JSON from markdown code block")
                return json.loads(json_match.group(1))
            
            # Look for standalone JSON object {...}
            json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            if json_match:
                logger.debug("Extracted JSON object from text")
                return json.loads(json_match.group(0))
            
            # Cannot find valid JSON
            logger.error(f"Could not extract JSON from response: {raw_content[:500]}")
            raise json.JSONDecodeError("No valid JSON found in response", raw_content, 0)
    
    def _create_classification_prompt(self, user_message: str) -> str:
        """Create the classification prompt for AI"""
        return f"""Classify this support ticket into structured categories.

**User Message:**
{user_message}

**Instructions:**
Return ONLY a valid JSON object with these exact fields:

{{
    "category": "<one of: Technical Issue, Billing, Feature Request, Account, Bug Report, General Inquiry>",
    "urgency": "<one of: Low, Medium, High, Critical>",
    "sentiment": "<one of: Positive, Neutral, Negative>",
    "confidence": <float between 0.0 and 1.0>
}}

**Guidelines:**
- **Category**: Classify based on the main topic (technical problems, billing issues, feature ideas, etc.)
- **Urgency**: Detect urgency from keywords like "urgent", "critical", "asap", "emergency", "blocking", "can't work"
- **Sentiment**: Analyze emotional tone (frustrated = Negative, thankful = Positive, neutral = Neutral)
- **Confidence**: Your confidence in the classification (0.0 = unsure, 1.0 = very confident)

Return ONLY the JSON, no explanations."""
    
    def _parse_classification(self, ai_result: Dict[str, Any]) -> AIClassification:
        """
        Parse and validate AI classification result
        
        Args:
            ai_result: Raw JSON from AI
            
        Returns:
            Validated AIClassification object
        """
        try:
            # Extract fields with defaults
            category = ai_result.get("category", "General Inquiry")
            urgency = ai_result.get("urgency", "Medium")
            sentiment = ai_result.get("sentiment", "Neutral")
            confidence = float(ai_result.get("confidence", 0.8))
            
            # Validate category
            valid_categories = [
                "Technical Issue", "Billing", "Feature Request", 
                "Account", "Bug Report", "General Inquiry"
            ]
            if category not in valid_categories:
                logger.warning(f"Invalid category '{category}', defaulting to 'General Inquiry'")
                category = "General Inquiry"
            
            # Validate urgency
            valid_urgencies = ["Low", "Medium", "High", "Critical"]
            if urgency not in valid_urgencies:
                logger.warning(f"Invalid urgency '{urgency}', defaulting to 'Medium'")
                urgency = "Medium"
            
            # Validate sentiment
            valid_sentiments = ["Positive", "Neutral", "Negative"]
            if sentiment not in valid_sentiments:
                logger.warning(f"Invalid sentiment '{sentiment}', defaulting to 'Neutral'")
                sentiment = "Neutral"
            
            # Validate confidence (0.0 to 1.0)
            confidence = max(0.0, min(1.0, confidence))
            
            # Create Pydantic model (will validate Literal types)
            return AIClassification(
                category=category,
                urgency=urgency,
                sentiment=sentiment,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Error parsing classification: {str(e)}")
            # Return safe defaults
            return AIClassification(
                category="General Inquiry",
                urgency="Medium",
                sentiment="Neutral",
                confidence=0.5
            )
