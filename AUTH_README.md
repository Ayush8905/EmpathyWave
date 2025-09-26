# 🌊 EmpathyWave3 - AI-Powered Mental Health Platform with Authentication

## 🚀 Overview

EmpathyWave3 is a comprehensive mental health support platform that combines artificial intelligence, machine learning, and secure user authentication to provide personalized emotional support and depression detection.

## ✨ Features

### 🔐 Authentication System
- **Secure User Registration**: Email-based signup with password strength validation
- **Parent Contact Integration**: Collects parent phone and email for emergency contacts
- **Session Management**: Secure token-based authentication with SQLite database
- **Password Security**: PBKDF2 hashing with salt for secure password storage
- **Animated UI**: Beautiful, responsive login/signup interfaces with real-time validation

### 🤖 AI Integration
- **Google Gemini Pro API**: Advanced natural language processing for empathetic conversations
- **Custom ML Model**: Trained depression detection using scikit-learn
- **Audio Analysis**: Voice emotion recognition using MFCC features
- **Intelligent Responses**: Context-aware mental health support

### 💬 Chat Features
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Depression Detection**: Automatic analysis of user messages for mental health insights
- **Voice Recording**: Audio message support with speech-to-text conversion
- **Chat History**: Persistent conversation storage in database
- **Personalized Experience**: User-specific greetings and session management

## 🏗️ Architecture

### Backend Components
```
enhanced_chat_app.py    # Main Flask application with authentication
database.py            # SQLite database manager with user auth
config.py             # Configuration settings
```

### Frontend Components
```
templates/
├── login.html         # Animated login interface
├── signup.html        # User registration form
├── chat_interface.html # Main chat application
└── index.html         # Landing page
```

### Model Components
```
app/models/
├── text_model.py      # Depression detection ML model
└── audio_model.py     # Voice emotion analysis
```

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Required packages (see requirements.txt)

### Setup Steps

1. **Clone and Setup Environment**
```bash
cd "path/to/EmpathyWave3"
pip install -r requirements.txt
```

2. **Configure API Keys**
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

3. **Initialize Database**
The SQLite database will be automatically created on first run.

4. **Run Application**
```bash
python enhanced_chat_app.py
```

5. **Access Application**
- Open browser to `http://127.0.0.1:5000`
- Register new account or login with existing credentials

## 🔐 Authentication Flow

### User Registration
1. **Access Signup**: Navigate to `/signup`
2. **Fill Form**: Provide email, password, parent contacts
3. **Validation**: Real-time password strength and email validation
4. **Account Creation**: Secure password hashing and database storage
5. **Auto-Login**: Automatic login after successful registration

### User Login
1. **Access Login**: Navigate to `/login` 
2. **Credentials**: Enter email and password
3. **Authentication**: Verify against hashed passwords in database
4. **Session Creation**: Generate secure session token
5. **Redirect**: Access to protected chat interface

### Session Management
- **Token-based**: Secure session tokens stored in database
- **Auto-expiry**: Sessions expire after inactivity
- **Route Protection**: `@login_required` decorator on protected routes
- **Secure Logout**: Complete session cleanup on logout

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    parent_phone TEXT,
    parent_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Sessions Table
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

## 🛡️ Security Features

### Password Security
- **Strong Hashing**: PBKDF2 with SHA-256
- **Unique Salts**: Per-user salt generation
- **Strength Validation**: Real-time password strength checking
- **Minimum Requirements**: Length, complexity validation

### Session Security
- **Secure Tokens**: Cryptographically secure random tokens
- **Token Expiry**: Automatic session timeout
- **Database Storage**: Server-side session management
- **CSRF Protection**: Flask-WTF form protection

### Data Protection
- **SQLite Security**: Local database with proper permissions
- **Input Validation**: Server-side validation of all inputs
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Template escaping

## 🎨 UI/UX Features

### Responsive Design
- **Bootstrap 5**: Modern, mobile-first framework
- **Custom CSS**: Beautiful animations and transitions
- **Loading States**: Visual feedback during operations
- **Error Handling**: User-friendly error messages

### Interactive Elements
- **Real-time Validation**: Instant feedback on form inputs
- **Password Strength Meter**: Visual password strength indicator
- **Typing Indicators**: Chat typing animations
- **Voice Recording**: Audio message support with visual feedback

## 🧪 Testing

### Manual Testing
1. **Start Application**: `python enhanced_chat_app.py`
2. **Test Registration**: Create new user account
3. **Test Login**: Login with created credentials
4. **Test Chat**: Send messages and receive AI responses
5. **Test Logout**: Verify session cleanup

### Automated Testing
```bash
python test_auth.py
```

## 📁 File Structure

```
EmpathyWave3/
├── enhanced_chat_app.py      # Main Flask application
├── database.py               # Database manager
├── config.py                 # Configuration
├── test_auth.py             # Authentication tests
├── requirements.txt          # Dependencies
├── empathy_wave.db          # SQLite database
├── templates/
│   ├── login.html           # Login interface
│   ├── signup.html          # Registration form
│   ├── chat_interface.html  # Main chat UI
│   └── index.html           # Landing page
├── app/
│   ├── models/              # ML models
│   ├── api/                 # API routes
│   └── static/              # CSS, JS, images
└── data/                    # Training data and models
```

## 🔧 Configuration

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_flask_secret_key
DATABASE_URL=sqlite:///empathy_wave.db
SESSION_TIMEOUT=86400  # 24 hours in seconds
```

### Application Settings
- **Debug Mode**: Enabled for development
- **Session Timeout**: 24 hours default
- **Password Requirements**: Minimum 8 characters, mixed case, numbers, symbols
- **Database**: SQLite for development, PostgreSQL recommended for production

## 🚀 Deployment

### Development
```bash
python enhanced_chat_app.py
```

### Production
- Use WSGI server (Gunicorn, uWSGI)
- Configure reverse proxy (Nginx)
- Use production database (PostgreSQL)
- Enable HTTPS/SSL
- Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request
5. Code review and merge

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact development team
- Check documentation wiki

## 🔮 Future Enhancements

- **Two-Factor Authentication**: SMS/Email 2FA
- **OAuth Integration**: Google/Facebook login
- **Admin Dashboard**: User management interface
- **API Documentation**: Swagger/OpenAPI docs
- **Mobile App**: React Native companion app
- **Advanced Analytics**: Mental health insights dashboard

---

**Built with ❤️ for mental health support and awareness**