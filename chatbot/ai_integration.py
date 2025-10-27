"""
Optional AI Integration Module for Enhanced Chatbot Responses

This module provides integration with OpenAI's GPT API for more intelligent
and contextual responses. To use this feature:

1. Install openai: pip install openai
2. Set your OpenAI API key: export OPENAI_API_KEY=your-api-key
3. Import and use the AIResponseGenerator class in app.py

Example usage:
    from ai_integration import AIResponseGenerator
    
    ai_generator = AIResponseGenerator()
    response = ai_generator.generate_response(user_message, conversation_history)
"""

import os
import json
from typing import List, Dict, Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not installed. Install with: pip install openai")

class AIResponseGenerator:
    """
    AI-powered response generator using OpenAI's GPT API
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the AI response generator
        
        Args:
            api_key: OpenAI API key (if not provided, will use environment variable)
            model: OpenAI model to use (default: gpt-3.5-turbo)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is required. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        self.model = model
        openai.api_key = self.api_key
        
        # System prompt to define the chatbot's personality and capabilities
        self.system_prompt = """You are a helpful, friendly, and intelligent AI assistant. You can help users with:
- General questions and conversations
- Time and date information
- Weather-related discussions (though you don't have real-time weather data)
- Problem-solving and advice
- Creative writing and brainstorming
- Educational topics

Be conversational, helpful, and engaging. Keep responses concise but informative. If you don't know something, admit it and offer to help in other ways."""

    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate an AI-powered response to user input
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages (optional)
            
        Returns:
            AI-generated response string
        """
        try:
            # Prepare messages for the API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Limit to last 10 messages for context
                    messages.append({
                        "role": msg.get('role', 'user'),
                        "content": msg.get('message', '')
                    })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=150,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            # Fallback to a simple response
            return "I'm having trouble processing your request right now. Please try again in a moment."

    def generate_response_with_context(self, user_message: str, context: Dict = None) -> str:
        """
        Generate response with additional context
        
        Args:
            user_message: The user's message
            context: Additional context (e.g., current time, user preferences)
            
        Returns:
            AI-generated response string
        """
        try:
            # Add context to system prompt
            system_prompt = self.system_prompt
            if context:
                context_info = []
                if 'current_time' in context:
                    context_info.append(f"Current time: {context['current_time']}")
                if 'current_date' in context:
                    context_info.append(f"Current date: {context['current_date']}")
                if 'user_name' in context:
                    context_info.append(f"User's name: {context['user_name']}")
                
                if context_info:
                    system_prompt += f"\n\nAdditional context: {', '.join(context_info)}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating AI response with context: {e}")
            return "I'm having trouble processing your request right now. Please try again in a moment."

    def is_available(self) -> bool:
        """
        Check if AI integration is available
        
        Returns:
            True if OpenAI is properly configured, False otherwise
        """
        return OPENAI_AVAILABLE and bool(self.api_key)

# Example usage and testing
if __name__ == "__main__":
    # Test the AI integration
    try:
        ai_generator = AIResponseGenerator()
        
        if ai_generator.is_available():
            print("AI integration is available!")
            
            # Test basic response
            response = ai_generator.generate_response("Hello! How are you?")
            print(f"AI Response: {response}")
            
            # Test with context
            context = {
                'current_time': '2023-12-15 14:30:00',
                'current_date': 'December 15, 2023'
            }
            response_with_context = ai_generator.generate_response_with_context(
                "What's the weather like?", context
            )
            print(f"AI Response with context: {response_with_context}")
        else:
            print("AI integration is not available. Check your API key.")
            
    except Exception as e:
        print(f"Error testing AI integration: {e}")
