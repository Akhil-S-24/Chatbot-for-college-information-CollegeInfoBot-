"""
Enhanced Flask Chatbot with Optional AI Integration

This is an enhanced version of the main app.py that includes optional AI integration.
To use AI features, install openai and set your API key.

Usage:
    python app_with_ai.py

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (optional)
    USE_AI: Set to 'true' to enable AI responses (optional)
"""

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import json
import os
from datetime import datetime
import random

# Try to import AI integration
try:
    from ai_integration import AIResponseGenerator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("AI integration not available. Install openai package to enable AI features.")

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
USE_AI = os.getenv('USE_AI', 'false').lower() == 'true'
AI_GENERATOR = None

# Initialize AI if available and enabled
if AI_AVAILABLE and USE_AI:
    try:
        AI_GENERATOR = AIResponseGenerator()
        print("AI integration enabled!")
    except Exception as e:
        print(f"Failed to initialize AI: {e}")
        AI_GENERATOR = None

# In-memory storage for conversation history (use database in production)
conversations = {}

# Enhanced response patterns (fallback when AI is not available)
RESPONSE_PATTERNS = {
    'greetings': [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! I'm here to assist you. What's on your mind?",
        "Greetings! How may I be of service?",
        "Welcome! I'm your AI assistant. How can I help you today?"
    ],
    'goodbye': [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Farewell! Feel free to come back anytime!",
        "Bye! It was nice chatting with you!",
        "Take care! I'll be here whenever you need me."
    ],
    'help': [
        "I can help you with various topics! Try asking me about weather, time, or just have a casual conversation.",
        "I'm here to assist! You can ask me questions, have a chat, or request information.",
        "Feel free to ask me anything! I can help with general questions and conversations.",
        "I'm your AI assistant! I can help with questions, creative tasks, problem-solving, and more."
    ],
    'weather': [
        "I'd love to help with weather information, but I don't have access to real-time weather data. You might want to check a weather app or website!",
        "Weather updates would be great! Unfortunately, I can't access current weather data, but I recommend checking your local weather service.",
        "I can discuss weather topics in general, but for current conditions, I'd suggest checking a reliable weather service."
    ],
    'time': [
        f"The current time is {datetime.now().strftime('%H:%M:%S')}",
        f"It's currently {datetime.now().strftime('%I:%M %p')}",
        f"Right now it's {datetime.now().strftime('%H:%M')}"
    ],
    'date': [
        f"Today's date is {datetime.now().strftime('%B %d, %Y')}",
        f"It's {datetime.now().strftime('%A, %B %d, %Y')}",
        f"Today is {datetime.now().strftime('%m/%d/%Y')}"
    ],
    'ai_features': [
        "I'm powered by AI and can help with creative writing, problem-solving, and complex questions!",
        "As an AI assistant, I can help you with a wide range of topics and tasks.",
        "I use advanced AI to provide intelligent and contextual responses to your questions."
    ],
    'default': [
        "That's interesting! Tell me more about that.",
        "I see! Can you elaborate on that?",
        "That's a great point! What else would you like to discuss?",
        "I understand. Is there anything specific you'd like to know?",
        "Thanks for sharing! How can I help you further?",
        "That's fascinating! I'd love to learn more about your perspective."
    ]
}

def get_conversation_id():
    """Generate or retrieve conversation ID for session"""
    if 'conversation_id' not in session:
        session['conversation_id'] = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
    return session['conversation_id']

def save_message(conversation_id, role, message):
    """Save message to conversation history"""
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    conversations[conversation_id].append({
        'role': role,
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

def get_bot_response(user_message, conversation_id=None):
    """Generate intelligent bot response based on user input"""
    # Try AI response first if available
    if AI_GENERATOR and AI_GENERATOR.is_available():
        try:
            # Get conversation history for context
            conversation_history = conversations.get(conversation_id, []) if conversation_id else []
            
            # Add context
            context = {
                'current_time': datetime.now().strftime('%H:%M:%S'),
                'current_date': datetime.now().strftime('%B %d, %Y')
            }
            
            # Generate AI response
            ai_response = AI_GENERATOR.generate_response_with_context(user_message, context)
            return ai_response
        except Exception as e:
            print(f"AI response failed, falling back to pattern matching: {e}")
    
    # Fallback to pattern matching
    message_lower = user_message.lower().strip()
    
    # Greeting patterns
    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
        return random.choice(RESPONSE_PATTERNS['greetings'])
    
    # Goodbye patterns
    elif any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell', 'later']):
        return random.choice(RESPONSE_PATTERNS['goodbye'])
    
    # Help patterns
    elif any(word in message_lower for word in ['help', 'what can you do', 'assist', 'support']):
        return random.choice(RESPONSE_PATTERNS['help'])
    
    # AI features patterns
    elif any(word in message_lower for word in ['ai', 'artificial intelligence', 'smart', 'intelligent']):
        return random.choice(RESPONSE_PATTERNS['ai_features'])
    
    # Weather patterns
    elif any(word in message_lower for word in ['weather', 'temperature', 'rain', 'sunny', 'cloudy']):
        return random.choice(RESPONSE_PATTERNS['weather'])
    
    # Time patterns
    elif any(word in message_lower for word in ['time', 'what time', 'clock']):
        return random.choice(RESPONSE_PATTERNS['time'])
    
    # Date patterns
    elif any(word in message_lower for word in ['date', 'today', 'what day']):
        return random.choice(RESPONSE_PATTERNS['date'])
    
    # Question patterns
    elif '?' in user_message:
        return "That's a great question! While I don't have access to real-time data, I'd be happy to discuss general topics or help in other ways."
    
    # Default response
    else:
        return random.choice(RESPONSE_PATTERNS['default'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        conversation_id = get_conversation_id()
        
        # Save user message
        save_message(conversation_id, 'user', user_message)
        
        # Generate bot response
        bot_response = get_bot_response(user_message, conversation_id)
        
        # Save bot response
        save_message(conversation_id, 'bot', bot_response)
        
        return jsonify({
            'response': bot_response,
            'conversation_id': conversation_id,
            'ai_enabled': AI_GENERATOR is not None and AI_GENERATOR.is_available()
        })
        
    except Exception as e:
        return jsonify({'error': 'An error occurred processing your message'}), 500

@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id in conversations:
        return jsonify(conversations[conversation_id])
    return jsonify([])

@app.route('/conversation/<conversation_id>', methods=['DELETE'])
def clear_conversation(conversation_id):
    """Clear conversation history"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return jsonify({'message': 'Conversation cleared successfully'})
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/conversations', methods=['GET'])
def list_conversations():
    """List all conversations"""
    return jsonify(list(conversations.keys()))

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_conversations': len(conversations),
        'ai_enabled': AI_GENERATOR is not None and AI_GENERATOR.is_available(),
        'ai_available': AI_AVAILABLE
    })

@app.route('/ai/status', methods=['GET'])
def ai_status():
    """Get AI integration status"""
    return jsonify({
        'ai_available': AI_AVAILABLE,
        'ai_enabled': AI_GENERATOR is not None and AI_GENERATOR.is_available(),
        'use_ai': USE_AI
    })

@app.route('/ai/toggle', methods=['POST'])
def toggle_ai():
    """Toggle AI integration (requires restart)"""
    global USE_AI
    USE_AI = not USE_AI
    return jsonify({
        'ai_enabled': USE_AI,
        'message': 'AI setting updated. Restart the application to apply changes.'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 AI Chatbot Server Starting...")
    print("=" * 50)
    print(f"AI Integration Available: {AI_AVAILABLE}")
    print(f"AI Integration Enabled: {AI_GENERATOR is not None and AI_GENERATOR.is_available()}")
    print(f"Server URL: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
