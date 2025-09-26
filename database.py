import sqlite3
import hashlib
import secrets
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='empathy_wave.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                parent_phone TEXT NOT NULL,
                parent_email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Create sessions table for user sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                risk_level TEXT,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create emergency alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score REAL NOT NULL,
                alert_sent BOOLEAN DEFAULT FALSE,
                parent_email TEXT,
                email_sent_timestamp TIMESTAMP,
                message_content TEXT,
                risk_indicators TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create risk assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message_id INTEGER,
                risk_level TEXT NOT NULL,
                risk_score REAL NOT NULL,
                critical_indicators TEXT,
                high_risk_indicators TEXT,
                medium_risk_indicators TEXT,
                positive_indicators TEXT,
                severity_factors TEXT,
                recommendations TEXT,
                emergency_alert_triggered BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (message_id) REFERENCES chat_history (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return password_hash.hex(), salt
    
    def verify_password(self, password, password_hash, salt):
        """Verify password against hash"""
        test_hash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)
        return test_hash.hex() == password_hash
    
    def create_user(self, email, password, parent_phone, parent_email):
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "User with this email already exists"
            
            # Hash password
            password_hash, salt = self.hash_password(password)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, password_hash, salt, parent_phone, parent_email)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password_hash, salt, parent_phone, parent_email))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, user_id
            
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, password_hash, salt, is_active 
                FROM users WHERE email = ?
            ''', (email,))
            
            user_data = cursor.fetchone()
            
            if not user_data:
                conn.close()
                return False, "Invalid email or password"
            
            user_id, password_hash, salt, is_active = user_data
            
            if not is_active:
                conn.close()
                return False, "Account is deactivated"
            
            if self.verify_password(password, password_hash, salt):
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (user_id,))
                conn.commit()
                conn.close()
                return True, user_id
            else:
                conn.close()
                return False, "Invalid email or password"
                
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def create_session(self, user_id):
        """Create a new session for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            session_token = secrets.token_urlsafe(32)
            
            # Session expires in 24 hours
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, datetime('now', '+1 day'))
            ''', (user_id, session_token))
            
            conn.commit()
            conn.close()
            
            return session_token
            
        except sqlite3.Error as e:
            return None
    
    def validate_session(self, session_token):
        """Validate user session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT us.user_id, u.email, u.parent_phone, u.parent_email
                FROM user_sessions us
                JOIN users u ON us.user_id = u.id
                WHERE us.session_token = ? 
                AND us.is_active = TRUE 
                AND us.expires_at > CURRENT_TIMESTAMP
            ''', (session_token,))
            
            session_data = cursor.fetchone()
            conn.close()
            
            if session_data:
                return True, {
                    'user_id': session_data[0],
                    'email': session_data[1],
                    'parent_phone': session_data[2],
                    'parent_email': session_data[3]
                }
            else:
                return False, None
                
        except sqlite3.Error as e:
            return False, None
    
    def end_session(self, session_token):
        """End user session (logout)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            return False
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, parent_phone, parent_email, created_at, last_login
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                return {
                    'id': user_data[0],
                    'email': user_data[1],
                    'parent_phone': user_data[2],
                    'parent_email': user_data[3],
                    'created_at': user_data[4],
                    'last_login': user_data[5]
                }
            return None
            
        except sqlite3.Error as e:
            return None
    
    def save_chat_message(self, user_id, message, response, risk_level=None, confidence_score=None):
        """Save chat message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (user_id, message, response, risk_level, confidence_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, message, response, risk_level, confidence_score))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            return False
    
    def get_user_chat_history(self, user_id, limit=50):
        """Get user's chat history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT message, response, risk_level, confidence_score, created_at
                FROM chat_history 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            history = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'message': row[0],
                    'response': row[1],
                    'risk_level': row[2],
                    'confidence_score': row[3],
                    'created_at': row[4]
                }
                for row in history
            ]
            
        except sqlite3.Error as e:
            return []
    
    def save_risk_assessment(self, user_id, message_id, risk_assessment):
        """Save risk assessment to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert indicators to JSON strings
            import json
            
            cursor.execute('''
                INSERT INTO risk_assessments (
                    user_id, message_id, risk_level, risk_score,
                    critical_indicators, high_risk_indicators, medium_risk_indicators,
                    positive_indicators, severity_factors, recommendations,
                    emergency_alert_triggered
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                message_id,
                risk_assessment['risk_level'],
                risk_assessment['risk_score'],
                json.dumps(risk_assessment['indicators']['critical']),
                json.dumps(risk_assessment['indicators']['high']),
                json.dumps(risk_assessment['indicators']['moderate']),
                json.dumps(risk_assessment['indicators']['positive']),
                json.dumps(risk_assessment['severity_factors']),
                json.dumps(risk_assessment['recommendations']),
                risk_assessment['emergency_alert_required']
            ))
            
            assessment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return assessment_id
            
        except sqlite3.Error as e:
            return None
    
    def create_emergency_alert(self, user_id, risk_level, risk_score, parent_email, message_content, risk_indicators):
        """Create emergency alert record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO emergency_alerts (
                    user_id, risk_level, risk_score, parent_email, 
                    message_content, risk_indicators
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, risk_level, risk_score, parent_email, message_content, risk_indicators))
            
            alert_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return alert_id
            
        except sqlite3.Error as e:
            return None
    
    def update_emergency_alert_sent(self, alert_id, email_sent_timestamp):
        """Update emergency alert as sent"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE emergency_alerts 
                SET alert_sent = TRUE, email_sent_timestamp = ?
                WHERE id = ?
            ''', (email_sent_timestamp, alert_id))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            return False
    
    def get_recent_emergency_alerts(self, user_id, hours=24):
        """Get recent emergency alerts for user (to prevent spam)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, risk_level, alert_sent, email_sent_timestamp, created_at
                FROM emergency_alerts 
                WHERE user_id = ? 
                AND created_at > datetime('now', '-{} hours')
                ORDER BY created_at DESC
            '''.format(hours), (user_id,))
            
            alerts = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'risk_level': row[1],
                    'alert_sent': row[2],
                    'email_sent_timestamp': row[3],
                    'created_at': row[4]
                }
                for row in alerts
            ]
            
        except sqlite3.Error as e:
            return []
    
    def get_user_risk_history(self, user_id, limit=20):
        """Get user's risk assessment history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT risk_level, risk_score, emergency_alert_triggered, created_at
                FROM risk_assessments 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            history = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'risk_level': row[0],
                    'risk_score': row[1],
                    'emergency_alert_triggered': row[2],
                    'created_at': row[3]
                }
                for row in history
            ]
            
        except sqlite3.Error as e:
            return []