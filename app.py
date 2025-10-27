from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import json
import os
from datetime import datetime
import random
from college_data import (
    get_college_by_name, get_all_colleges, search_colleges_by_program,
    search_colleges_by_location, compare_colleges, get_admission_calculator
)
from college_admin import add_college_to_database, validate_college_data, get_college_statistics

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-change-this-in-production'

# In-memory storage for conversation history (use database in production)
conversations = {}

# Enhanced response patterns for college information chatbot
RESPONSE_PATTERNS = {
    'greetings': [
        "Hello! I'm your college information assistant. I can help you explore universities, compare programs, and find the perfect college for you!",
        "Hi there! Welcome to the college information center. What college would you like to learn about?",
        "Hey! I'm here to help you with college information. I have details about Harvard, MIT, Stanford, Berkeley, Yale, Princeton, and Caltech!",
        "Greetings! I can help you find information about top universities, their programs, admission requirements, and more!"
    ],
    'goodbye': [
        "Goodbye! Good luck with your college search!",
        "See you later! I hope I helped you find the right college!",
        "Farewell! Feel free to come back anytime for more college information!",
        "Bye! Best wishes for your academic journey!"
    ],
    'help': [
        "I can help you with college information! Try asking me about:\n• Specific colleges (Harvard, MIT, Stanford, etc.)\n• Programs of study\n• Admission requirements\n• Tuition and fees\n• Campus life\n• College comparisons",
        "I'm your college information assistant! I have details about 7 top universities. You can ask me about:\n• College details and rankings\n• Academic programs\n• Admission statistics\n• Financial information\n• Campus features",
        "I can help you explore colleges! Ask me about:\n• 'Tell me about Harvard'\n• 'What programs does MIT offer?'\n• 'Compare Harvard and Stanford'\n• 'What are the admission requirements for Berkeley?'"
    ],
    'college_list': [
        "Here are the colleges I have information about:\n🏛️ Harvard University (#1)\n🔬 MIT (#2)\n🌲 Stanford University (#3)\n🏛️ UC Berkeley (#4)\n🎓 Yale University (#5)\n🏛️ Princeton University (#6)\n🔬 Caltech (#7)\n🏛️ Columbia University (#8)\n🏛️ University of Pennsylvania (#9)\n🏛️ Duke University (#10)\n🏛️ Northwestern University (#11)\n🏥 Johns Hopkins University (#12)\n🏛️ Cornell University (#13)\n🏛️ Rice University (#14)\n🏛️ Vanderbilt University (#15)\n\nAsk me about any of these colleges!",
        "I have detailed information about these top 15 universities:\n• Harvard University (Cambridge, MA) - #1\n• MIT (Cambridge, MA) - #2\n• Stanford University (Stanford, CA) - #3\n• UC Berkeley (Berkeley, CA) - #4\n• Yale University (New Haven, CT) - #5\n• Princeton University (Princeton, NJ) - #6\n• Caltech (Pasadena, CA) - #7\n• Columbia University (New York, NY) - #8\n• University of Pennsylvania (Philadelphia, PA) - #9\n• Duke University (Durham, NC) - #10\n• Northwestern University (Evanston, IL) - #11\n• Johns Hopkins University (Baltimore, MD) - #12\n• Cornell University (Ithaca, NY) - #13\n• Rice University (Houston, TX) - #14\n• Vanderbilt University (Nashville, TN) - #15\n\nWhich one interests you?"
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
    'default': [
        "That's interesting! I'd be happy to help you with college information. What would you like to know?",
        "I see! I can help you explore colleges and their programs. What college are you interested in?",
        "That's a great question! I have information about top universities. Which college would you like to learn about?",
        "I understand! I can help you with college details, programs, admission requirements, and more. What would you like to explore?",
        "Thanks for sharing! I'm here to help with college information. What college or program interests you?"
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

def get_bot_response(user_message):
    """Generate intelligent bot response based on user input"""
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
    
    # College list patterns
    elif any(word in message_lower for word in ['colleges', 'universities', 'list', 'show me colleges', 'what colleges']):
        return random.choice(RESPONSE_PATTERNS['college_list'])
    
    # Specific college queries
    elif any(college in message_lower for college in ['harvard', 'mit', 'stanford', 'berkeley', 'yale', 'princeton', 'caltech', 'columbia', 'upenn', 'penn', 'duke', 'northwestern', 'jhu', 'johns', 'cornell', 'rice', 'vanderbilt']):
        return handle_college_query(user_message)
    
    # Program search queries
    elif any(word in message_lower for word in ['program', 'major', 'study', 'degree', 'course']):
        return handle_program_query(user_message)
    
    # Comparison queries
    elif any(word in message_lower for word in ['compare', 'comparison', 'vs', 'versus', 'difference']):
        return handle_comparison_query(user_message)
    
    # Admission queries
    elif any(word in message_lower for word in ['admission', 'requirements', 'gpa', 'sat', 'act', 'acceptance']):
        return handle_admission_query(user_message)
    
    # Tuition/financial queries
    elif any(word in message_lower for word in ['tuition', 'cost', 'price', 'fee', 'financial', 'money']):
        return handle_financial_query(user_message)
    
    # Location queries
    elif any(word in message_lower for word in ['location', 'where', 'city', 'state', 'address']):
        return handle_location_query(user_message)
    
    # Time patterns
    elif any(word in message_lower for word in ['time', 'what time', 'clock']):
        return random.choice(RESPONSE_PATTERNS['time'])
    
    # Date patterns
    elif any(word in message_lower for word in ['date', 'today', 'what day']):
        return random.choice(RESPONSE_PATTERNS['date'])
    
    # Question patterns
    elif '?' in user_message:
        return "That's a great question! I'd be happy to help you with college information. What specific college or topic are you interested in?"
    
    # Default response
    else:
        return random.choice(RESPONSE_PATTERNS['default'])

def handle_college_query(user_message):
    """Handle queries about specific colleges"""
    message_lower = user_message.lower().strip()
    
    # Extract college name
    college = None
    for college_name in ['harvard', 'mit', 'stanford', 'berkeley', 'yale', 'princeton', 'caltech', 'columbia', 'upenn', 'penn', 'duke', 'northwestern', 'jhu', 'johns', 'cornell', 'rice', 'vanderbilt']:
        if college_name in message_lower:
            college = get_college_by_name(college_name)
            break
    
    if not college:
        return "I couldn't identify which college you're asking about. Please specify: Harvard, MIT, Stanford, Berkeley, Yale, Princeton, or Caltech."
    
    # Format college information
    info = f"🏛️ **{college['name']}**\n"
    info += f"📍 Location: {college['location']}\n"
    info += f"🏫 Type: {college['type']}\n"
    info += f"📅 Founded: {college['founded']}\n"
    info += f"🏆 Ranking: #{college['ranking']}\n"
    info += f"📊 Acceptance Rate: {college['acceptance_rate']}%\n\n"
    
    info += f"💰 **Tuition (2023-2024):**\n"
    if 'undergraduate_in_state' in college['tuition']:
        info += f"• In-state: ${college['tuition']['undergraduate_in_state']:,}\n"
        info += f"• Out-of-state: ${college['tuition']['undergraduate_out_state']:,}\n"
    else:
        info += f"• Undergraduate: ${college['tuition']['undergraduate']:,}\n"
    info += f"• Room & Board: ${college['tuition']['room_board']:,}\n\n"
    
    info += f"🎓 **Popular Programs:**\n"
    for program in college['programs']['undergraduate'][:5]:
        info += f"• {program}\n"
    
    info += f"\n📞 Contact: {college['contact']['phone']}\n"
    info += f"🌐 Website: {college['website']}"
    
    return info

def handle_program_query(user_message):
    """Handle queries about academic programs"""
    message_lower = user_message.lower().strip()
    
    # Extract program name
    program_keywords = ['computer science', 'engineering', 'business', 'medicine', 'law', 'art', 'music', 'biology', 'chemistry', 'physics', 'mathematics', 'economics', 'psychology', 'history', 'english']
    
    program = None
    for keyword in program_keywords:
        if keyword in message_lower:
            program = keyword
            break
    
    if not program:
        return "What program are you interested in? I can help you find colleges that offer programs in Computer Science, Engineering, Business, Medicine, Law, and many more!"
    
    # Search for colleges with this program
    colleges = search_colleges_by_program(program)
    
    if not colleges:
        return f"I couldn't find any colleges offering {program.title()} programs in my database."
    
    info = f"🎓 **Colleges offering {program.title()} programs:**\n\n"
    for college in colleges[:5]:  # Show top 5
        info += f"🏛️ **{college['name']}**\n"
        info += f"📍 {college['location']}\n"
        info += f"🏆 Ranking: #{college['ranking']}\n"
        info += f"📊 Acceptance Rate: {college['acceptance_rate']}%\n\n"
    
    return info

def handle_comparison_query(user_message):
    """Handle college comparison queries"""
    message_lower = user_message.lower().strip()
    
    # Extract college names
    college_names = []
    for college_name in ['harvard', 'mit', 'stanford', 'berkeley', 'yale', 'princeton', 'caltech', 'columbia', 'upenn', 'penn', 'duke', 'northwestern', 'jhu', 'johns', 'cornell', 'rice', 'vanderbilt']:
        if college_name in message_lower:
            college_names.append(college_name)
    
    if len(college_names) < 2:
        return "Please specify which colleges you'd like to compare. For example: 'Compare Harvard and MIT' or 'Harvard vs Stanford'"
    
    comparison = compare_colleges(college_names)
    
    if 'error' in comparison:
        return comparison['error']
    
    info = f"📊 **College Comparison:**\n\n"
    
    for college in comparison['colleges']:
        info += f"🏛️ **{college['name']}**\n"
        info += f"📍 {college['location']}\n"
        info += f"🏆 Ranking: #{college['ranking']}\n"
        info += f"📊 Acceptance Rate: {college['acceptance_rate']}%\n"
        info += f"👥 Student Population: {college['campus_life']['student_population']:,}\n"
        info += f"💰 Tuition: ${college['tuition']['undergraduate']:,}\n\n"
    
    return info

def handle_admission_query(user_message):
    """Handle admission requirements queries"""
    message_lower = user_message.lower().strip()
    
    # Extract college name
    college = None
    for college_name in ['harvard', 'mit', 'stanford', 'berkeley', 'yale', 'princeton', 'caltech', 'columbia', 'upenn', 'penn', 'duke', 'northwestern', 'jhu', 'johns', 'cornell', 'rice', 'vanderbilt']:
        if college_name in message_lower:
            college = get_college_by_name(college_name)
            break
    
    if not college:
        return "Which college's admission requirements would you like to know about? I have information about Harvard, MIT, Stanford, Berkeley, Yale, Princeton, and Caltech."
    
    req = college['admission_requirements']
    info = f"📋 **{college['name']} Admission Requirements:**\n\n"
    info += f"📊 **Academic Requirements:**\n"
    info += f"• GPA: {req['gpa']}+ (recommended)\n"
    info += f"• SAT Score: {req['sat_score']}+ (recommended)\n"
    info += f"• ACT Score: {req['act_score']}+ (recommended)\n"
    info += f"• TOEFL: {req['toefl']}+ (international students)\n"
    info += f"• IELTS: {req['ielts']}+ (international students)\n\n"
    
    info += f"📝 **Application Requirements:**\n"
    info += f"• Essays: {req['essays']}\n"
    info += f"• Recommendations: {req['recommendations']}\n"
    info += f"• Application Deadline: {req['deadline']}\n\n"
    
    info += f"📊 **Current Statistics:**\n"
    info += f"• Acceptance Rate: {college['acceptance_rate']}%\n"
    info += f"• Student-Faculty Ratio: {college['campus_life']['student_faculty_ratio']}:1\n"
    
    return info

def handle_financial_query(user_message):
    """Handle tuition and financial queries"""
    message_lower = user_message.lower().strip()
    
    # Extract college name
    college = None
    for college_name in ['harvard', 'mit', 'stanford', 'berkeley', 'yale', 'princeton', 'caltech', 'columbia', 'upenn', 'penn', 'duke', 'northwestern', 'jhu', 'johns', 'cornell', 'rice', 'vanderbilt']:
        if college_name in message_lower:
            college = get_college_by_name(college_name)
            break
    
    if not college:
        return "Which college's tuition information would you like to know about? I have details about Harvard, MIT, Stanford, Berkeley, Yale, Princeton, and Caltech."
    
    tuition = college['tuition']
    info = f"💰 **{college['name']} Financial Information (2023-2024):**\n\n"
    
    if 'undergraduate_in_state' in tuition:
        info += f"📚 **Undergraduate Tuition:**\n"
        info += f"• In-state: ${tuition['undergraduate_in_state']:,}\n"
        info += f"• Out-of-state: ${tuition['undergraduate_out_state']:,}\n"
    else:
        info += f"📚 **Undergraduate Tuition:** ${tuition['undergraduate']:,}\n"
    
    info += f"🏠 **Room & Board:** ${tuition['room_board']:,}\n"
    
    if 'graduate' in tuition:
        info += f"🎓 **Graduate Tuition:** ${tuition['graduate']:,}\n"
    
    info += f"\n📊 **Acceptance Rate:** {college['acceptance_rate']}%\n"
    info += f"🏆 **Ranking:** #{college['ranking']}\n"
    
    return info

def handle_location_query(user_message):
    """Handle location-based queries"""
    message_lower = user_message.lower().strip()
    
    # Extract location
    locations = ['california', 'massachusetts', 'connecticut', 'new jersey', 'pasadena', 'cambridge', 'stanford', 'berkeley', 'new haven', 'princeton']
    
    location = None
    for loc in locations:
        if loc in message_lower:
            location = loc
            break
    
    if not location:
        return "What location are you interested in? I have colleges in California, Massachusetts, Connecticut, and New Jersey."
    
    colleges = search_colleges_by_location(location)
    
    if not colleges:
        return f"I couldn't find any colleges in {location.title()} in my database."
    
    info = f"📍 **Colleges in {location.title()}:**\n\n"
    for college in colleges:
        info += f"🏛️ **{college['name']}**\n"
        info += f"📍 {college['location']}\n"
        info += f"🏆 Ranking: #{college['ranking']}\n"
        info += f"📊 Acceptance Rate: {college['acceptance_rate']}%\n\n"
    
    return info

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
        bot_response = get_bot_response(user_message)
        
        # Save bot response
        save_message(conversation_id, 'bot', bot_response)
        
        return jsonify({
            'response': bot_response,
            'conversation_id': conversation_id
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
        'active_conversations': len(conversations)
    })

@app.route('/colleges', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    return jsonify(get_all_colleges())

@app.route('/colleges/<college_name>', methods=['GET'])
def get_college(college_name):
    """Get specific college information"""
    college = get_college_by_name(college_name)
    if college:
        return jsonify(college)
    return jsonify({'error': 'College not found'}), 404

@app.route('/colleges/search/program', methods=['GET'])
def search_by_program():
    """Search colleges by program"""
    program = request.args.get('program', '')
    if not program:
        return jsonify({'error': 'Program parameter required'}), 400
    
    colleges = search_colleges_by_program(program)
    return jsonify(colleges)

@app.route('/colleges/search/location', methods=['GET'])
def search_by_location():
    """Search colleges by location"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({'error': 'Location parameter required'}), 400
    
    colleges = search_colleges_by_location(location)
    return jsonify(colleges)

@app.route('/colleges/compare', methods=['POST'])
def compare_colleges_endpoint():
    """Compare multiple colleges"""
    data = request.get_json()
    college_names = data.get('colleges', [])
    
    if len(college_names) < 2:
        return jsonify({'error': 'At least 2 colleges required for comparison'}), 400
    
    comparison = compare_colleges(college_names)
    return jsonify(comparison)

@app.route('/admission/calculator', methods=['POST'])
def admission_calculator():
    """Calculate admission chances"""
    data = request.get_json()
    college_name = data.get('college', '')
    gpa = data.get('gpa', 0)
    sat = data.get('sat', 0)
    act = data.get('act', 0)
    
    if not college_name or not gpa:
        return jsonify({'error': 'College name and GPA are required'}), 400
    
    result = get_admission_calculator(college_name, gpa, sat, act)
    return jsonify(result)

# Admin routes
@app.route('/admin')
def admin_interface():
    """Admin interface for managing colleges"""
    return render_template('admin_interface.html')

@app.route('/admin/statistics', methods=['GET'])
def admin_statistics():
    """Get college database statistics"""
    try:
        stats = get_college_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/add-college', methods=['POST'])
def admin_add_college():
    """Add a new college to the database"""
    try:
        data = request.get_json()
        
        # Validate the data
        errors = validate_college_data(data)
        if errors:
            return jsonify({'success': False, 'error': 'Validation failed: ' + '; '.join(errors)}), 400
        
        # Add the college
        success = add_college_to_database(data)
        
        if success:
            return jsonify({'success': True, 'message': 'College added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add college'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("COLLEGE INFORMATION CHATBOT STARTING...")
    print("=" * 60)
    print("Available Colleges:")
    colleges = get_all_colleges()
    for college in colleges:
        print(f"   • {college['name']} (#{college['ranking']})")
    print("=" * 60)
    print("Server URL: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
    