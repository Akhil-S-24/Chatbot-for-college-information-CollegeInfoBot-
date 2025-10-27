# 🤖 AI Chatbot - Your Intelligent Assistant

A modern, feature-rich chatbot built with Python Flask and HTML/CSS/JavaScript. This chatbot provides an engaging conversational experience with a beautiful, responsive user interface.

![Chatbot Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=AI+Chatbot+Preview)

## ✨ Features

### 🎯 Core Features
- **Intelligent Conversations**: Context-aware responses with multiple conversation patterns
- **Real-time Chat**: Instant messaging with typing indicators
- **Conversation Memory**: Persistent conversation history per session
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Dark/Light Theme**: Customizable themes with user preferences
- **Mobile Responsive**: Works perfectly on all device sizes

### 🛠️ Advanced Features
- **Settings Panel**: Customize font size, theme, and notification sounds
- **Message Timestamps**: See when each message was sent
- **Typing Indicators**: Visual feedback when the bot is "thinking"
- **Suggestion Chips**: Quick-start conversation prompts
- **Clear Chat**: Reset conversation history
- **Error Handling**: Graceful error management and user feedback
- **Accessibility**: Keyboard navigation and screen reader support

### 🔧 Technical Features
- **RESTful API**: Clean API endpoints for chat functionality
- **Session Management**: Secure session handling
- **CORS Support**: Cross-origin resource sharing enabled
- **Health Check**: API health monitoring endpoint
- **Modular Design**: Clean, maintainable code structure

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv chatbot_env
   
   # On Windows
   chatbot_env\Scripts\activate
   
   # On macOS/Linux
   source chatbot_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/
│   └── style.css         # CSS styles and themes
└── templates/
    └── index.html        # Main HTML template
```

## 🎨 Customization

### Themes
The chatbot supports three theme modes:
- **Light Theme**: Clean, bright interface
- **Dark Theme**: Easy on the eyes for low-light usage
- **Auto Theme**: Automatically switches based on system preference

### Response Patterns
The bot includes intelligent response patterns for:
- Greetings (hi, hello, hey, etc.)
- Goodbyes (bye, goodbye, see you, etc.)
- Help requests (help, what can you do, etc.)
- Time queries (time, what time, clock)
- Date queries (date, today, what day)
- Weather questions (weather, temperature, etc.)
- General conversation

### Adding New Features
1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Extend the `ChatBot` class in `index.html`
3. **Styling**: Add CSS rules in `static/style.css`

## 🔌 API Endpoints

### Chat Endpoints
- `POST /chat` - Send a message to the chatbot
- `GET /conversation/<id>` - Get conversation history
- `DELETE /conversation/<id>` - Clear conversation history
- `GET /conversations` - List all conversations

### Utility Endpoints
- `GET /health` - Health check endpoint
- `GET /` - Main application page

### Example API Usage

```javascript
// Send a message
const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello!' })
});
const data = await response.json();
console.log(data.response); // Bot's reply
```

## 🎯 Usage Examples

### Basic Conversation
```
User: Hi there!
Bot: Hello! How can I help you today?

User: What time is it?
Bot: The current time is 14:30:25

User: What's the date?
Bot: Today's date is December 15, 2023

User: Help me
Bot: I can help you with various topics! Try asking me about weather, time, or just have a casual conversation.
```

### Advanced Features
- Click suggestion chips to quickly start conversations
- Use the settings panel to customize your experience
- Clear chat history when starting fresh conversations
- Switch between light and dark themes

## 🔧 Configuration

### Environment Variables
You can customize the application by setting these environment variables:

```bash
# Flask configuration
export FLASK_ENV=development  # or production
export FLASK_DEBUG=True       # Enable debug mode

# Application settings
export CHATBOT_SECRET_KEY=your-secret-key-here
export CHATBOT_HOST=0.0.0.0
export CHATBOT_PORT=5000
```

### Database Integration
For production use, consider integrating with a database:

```python
# Example with SQLite
import sqlite3

def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            messages TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Using Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

3. **Using Heroku**:
   ```bash
   # Add Procfile
   echo "web: gunicorn app:app" > Procfile
   
   # Deploy
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework for the backend
- Font Awesome for icons
- Modern CSS techniques for responsive design
- Web Audio API for notification sounds

## 🔮 Future Enhancements

- [ ] Integration with OpenAI GPT API
- [ ] Voice input/output support
- [ ] File upload and sharing
- [ ] Multi-language support
- [ ] User authentication
- [ ] Conversation export/import
- [ ] Plugin system for custom responses
- [ ] Analytics dashboard
- [ ] WebSocket support for real-time updates

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/chatbot/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Made with ❤️ and Python**
