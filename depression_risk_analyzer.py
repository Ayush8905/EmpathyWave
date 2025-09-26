#!/usr/bin/env python3
"""
Depression Risk Analyzer for EmpathyWave
Analyzes user messages to determine depression risk levels and trigger emergency alerts
"""

import re
import logging
from typing import Dict, List, Tuple, Any
from datetime import datetime
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DepressionRiskAnalyzer:
    """Analyzes user messages to determine depression risk levels"""
    
    def __init__(self):
        """Initialize the risk analyzer with keywords and patterns"""
        
        # Critical risk indicators - immediate emergency alert
        self.critical_keywords = [
            # Self-harm indicators with variations
            'kill myself', 'kill my self', 'going to kill myself', 'going to kill my self',
            'kill me', 'end my life', 'end my own life', 'suicide', 'suicidal', 
            'want to die', 'going to die', 'planning to die', 'better off dead', 
            'end it all', 'harm myself', 'harm my self', 'hurt myself', 'hurt my self',
            'cut myself', 'cut my self', 'self harm', 'self-harm', 'self injury',
            'take my own life', 'take my life', 'gonna kill myself', 'gonna kill my self',
            'want to be dead', 'wish i was dead', 'wish i were dead',
            
            # Method-specific indicators
            'overdose', 'pills to die', 'taking pills', 'jumping off', 'hanging myself',
            'hang myself', 'gun to kill', 'knife to hurt', 'razor blade', 'razor to cut',
            'bridge to jump', 'cliff to jump', 'poison myself',
            
            # Planning and finality indicators
            'goodbye forever', 'final goodbye', 'farewell', 'last time talking',
            'final message', 'won\'t be here tomorrow', 'won\'t be here much longer',
            'leaving forever', 'can\'t go on', 'nothing left to live for',
            'nobody will miss me', 'world better without me', 'ready to die',
            'made peace with dying', 'planning my death', 'writing suicide note'
        ]
        
        # High risk indicators - emergency alert
        self.high_risk_keywords = [
            # Severe depression indicators
            'severe depression', 'major depression', 'clinical depression',
            'deep depression', 'severe anxiety', 'panic attacks', 'mental breakdown',
            
            # Hopelessness indicators
            'no hope', 'hopeless', 'helpless', 'pointless', 'meaningless',
            'no future', 'no point', 'give up', 'giving up', 'lost cause',
            
            # Isolation indicators
            'completely alone', 'nobody cares', 'no friends', 'isolated',
            'abandoned', 'rejected', 'unwanted', 'burden',
            
            # Severe mood indicators
            'extremely sad', 'devastated', 'destroyed', 'broken inside',
            'empty inside', 'numb', 'dead inside', 'soul crushing'
        ]
        
        # Medium risk indicators - monitoring required
        self.medium_risk_keywords = [
            # Depression indicators
            'depressed', 'depression', 'sad', 'sadness', 'grief', 'sorrow',
            'melancholy', 'blue', 'down', 'low mood', 'mood swings',
            
            # Anxiety indicators
            'anxious', 'anxiety', 'worried', 'stress', 'stressed', 'overwhelmed',
            'panic', 'fear', 'scared', 'terrified', 'nervous breakdown',
            
            # Sleep/appetite issues
            'can\'t sleep', 'insomnia', 'nightmares', 'no appetite', 'eating disorder',
            'weight loss', 'weight gain', 'fatigue', 'exhausted', 'tired',
            
            # Social withdrawal
            'don\'t want to see anyone', 'avoiding people', 'staying in bed',
            'missing school', 'skipping classes', 'don\'t care anymore'
        ]
        
        # Positive indicators - lower risk
        self.positive_keywords = [
            'better', 'improving', 'good day', 'feeling good', 'happy', 'joy',
            'excited', 'hopeful', 'optimistic', 'grateful', 'thankful',
            'support', 'help', 'therapy', 'counseling', 'medication working',
            'friends', 'family', 'love', 'care', 'future plans'
        ]
        
        # Pattern matching for severity
        self.severity_patterns = {
            'intensity_words': ['extremely', 'severely', 'deeply', 'very', 'really', 'so', 'too'],
            'frequency_words': ['always', 'constantly', 'every day', 'all the time', 'never stops'],
            'duration_words': ['weeks', 'months', 'years', 'long time', 'forever']
        }
        
        # Scoring weights
        self.weights = {
            'critical': 100,
            'high': 25,
            'medium': 5,
            'positive': -10,
            'intensity_multiplier': 1.5,
            'frequency_multiplier': 1.3,
            'duration_multiplier': 1.2
        }
        
        # Risk thresholds
        self.thresholds = {
            'critical': 80,    # Immediate emergency alert
            'high': 40,        # Emergency alert within 1 hour
            'medium': 15,      # Monitoring and follow-up
            'low': 5           # Regular support
        }
        
        # User risk history tracking
        self.user_risk_history = {}
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better keyword matching"""
        import re
        
        # Convert to lowercase
        text = text.lower()
        
        # Handle common contractions and variations
        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"can't", "cannot", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"gonna", "going to", text)
        text = re.sub(r"wanna", "want to", text)
        
        # Handle spacing variations
        text = re.sub(r"\s+", " ", text)  # Multiple spaces to single space
        text = re.sub(r"myself", "my self", text)  # Handle "myself" vs "my self"
        
        # Remove punctuation for better matching
        text = re.sub(r"[^\w\s]", " ", text)
        
        return text.strip()
    
    def _flexible_keyword_match(self, text: str, keywords: List[str]) -> List[str]:
        """Flexible keyword matching that handles variations and partial matches"""
        normalized_text = self._normalize_text(text)
        found_keywords = []
        
        for keyword in keywords:
            normalized_keyword = self._normalize_text(keyword)
            
            # Exact match
            if normalized_keyword in normalized_text:
                found_keywords.append(keyword)
                continue
            
            # Check for key phrases that might be split
            keyword_words = normalized_keyword.split()
            if len(keyword_words) > 1:
                # Check if all words are present (order doesn't matter for critical keywords)
                if all(word in normalized_text for word in keyword_words):
                    found_keywords.append(keyword)
                    continue
            
            # For critical suicide-related keywords, be extra sensitive
            if any(critical_word in keyword for critical_word in ['kill', 'die', 'suicide', 'harm', 'hurt']):
                # Check for partial matches with high confidence
                keyword_core = normalized_keyword.replace(' ', '')
                text_no_spaces = normalized_text.replace(' ', '')
                
                if keyword_core in text_no_spaces:
                    found_keywords.append(keyword)
        
        return found_keywords
    
    def analyze_message(self, user_id: str, message: str, user_history: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a single message for depression risk indicators
        
        Args:
            user_id: Unique identifier for the user
            message: User's message to analyze
            user_history: List of previous messages for context
            
        Returns:
            Dict containing risk assessment results
        """
        message_lower = message.lower()
        
        # Initialize risk assessment
        risk_assessment = {
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.now(),
            'risk_score': 0,
            'risk_level': 'LOW',
            'indicators': {
                'critical': [],
                'high': [],
                'moderate': [],
                'positive': []
            },
            'severity_factors': {
                'intensity': False,
                'frequency': False,
                'duration': False
            },
            'emergency_alert_required': False,
            'recommendations': []
        }
        
        # Check for critical risk indicators using flexible matching
        critical_matches = self._flexible_keyword_match(message, self.critical_keywords)
        for keyword in critical_matches:
            risk_assessment['risk_score'] += self.weights['critical']
            risk_assessment['indicators']['critical'].append(keyword)
        
        # Check for high risk indicators using flexible matching
        high_risk_matches = self._flexible_keyword_match(message, self.high_risk_keywords)
        for keyword in high_risk_matches:
            risk_assessment['risk_score'] += self.weights['high']
            risk_assessment['indicators']['high'].append(keyword)
        
        # Check for moderate risk indicators using flexible matching
        moderate_risk_matches = self._flexible_keyword_match(message, self.medium_risk_keywords)
        for keyword in moderate_risk_matches:
            risk_assessment['risk_score'] += self.weights['medium']
            risk_assessment['indicators']['moderate'].append(keyword)
        
        # Check for positive indicators using flexible matching
        positive_matches = self._flexible_keyword_match(message, self.positive_keywords)
        for keyword in positive_matches:
            risk_assessment['risk_score'] += self.weights['positive']
            risk_assessment['indicators']['positive'].append(keyword)
        
        # Apply severity multipliers
        risk_assessment = self._apply_severity_multipliers(risk_assessment, message_lower)
        
        # Consider historical context
        if user_history:
            risk_assessment = self._analyze_historical_context(risk_assessment, user_history)
        
        # Determine final risk level
        risk_assessment = self._determine_risk_level(risk_assessment)
        
        # Generate recommendations
        risk_assessment['recommendations'] = self._generate_recommendations(risk_assessment)
        
        # Update user risk history
        self._update_user_history(user_id, risk_assessment)
        
        logger.info(f"Risk analysis completed for user {user_id}: {risk_assessment['risk_level']} risk (score: {risk_assessment['risk_score']})")
        
        return risk_assessment
    
    def _apply_severity_multipliers(self, risk_assessment: Dict[str, Any], message_lower: str) -> Dict[str, Any]:
        """Apply severity multipliers based on intensity, frequency, and duration indicators"""
        
        # Check for intensity words
        for word in self.severity_patterns['intensity_words']:
            if word in message_lower:
                risk_assessment['severity_factors']['intensity'] = True
                risk_assessment['risk_score'] *= self.weights['intensity_multiplier']
                break
        
        # Check for frequency words
        for word in self.severity_patterns['frequency_words']:
            if word in message_lower:
                risk_assessment['severity_factors']['frequency'] = True
                risk_assessment['risk_score'] *= self.weights['frequency_multiplier']
                break
        
        # Check for duration words
        for word in self.severity_patterns['duration_words']:
            if word in message_lower:
                risk_assessment['severity_factors']['duration'] = True
                risk_assessment['risk_score'] *= self.weights['duration_multiplier']
                break
        
        return risk_assessment
    
    def _analyze_historical_context(self, risk_assessment: Dict[str, Any], user_history: List[str]) -> Dict[str, Any]:
        """Analyze historical context to adjust risk assessment"""
        
        # Simple historical analysis - count concerning messages in recent history
        recent_concerning_count = 0
        
        for historical_message in user_history[-10:]:  # Last 10 messages
            historical_lower = historical_message.lower()
            
            # Count messages with risk indicators
            has_risk_indicator = any(
                keyword in historical_lower 
                for keyword in (self.critical_keywords + self.high_risk_keywords + self.medium_risk_keywords)
            )
            
            if has_risk_indicator:
                recent_concerning_count += 1
        
        # Adjust risk score based on historical pattern
        if recent_concerning_count >= 3:
            risk_assessment['risk_score'] *= 1.4  # 40% increase for pattern of concerning messages
        elif recent_concerning_count >= 2:
            risk_assessment['risk_score'] *= 1.2  # 20% increase for some concerning messages
        
        return risk_assessment
    
    def _determine_risk_level(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Determine final risk level based on score and indicators"""
        
        score = risk_assessment['risk_score']
        
        # Check for critical indicators first (override score-based assessment)
        if risk_assessment['indicators']['critical']:
            risk_assessment['risk_level'] = 'CRITICAL'
            risk_assessment['emergency_alert_required'] = True
        elif score >= self.thresholds['critical']:
            risk_assessment['risk_level'] = 'CRITICAL'
            risk_assessment['emergency_alert_required'] = True
        elif score >= self.thresholds['high']:
            risk_assessment['risk_level'] = 'HIGH'
            risk_assessment['emergency_alert_required'] = True
        elif score >= self.thresholds['medium']:
            risk_assessment['risk_level'] = 'MODERATE'
            risk_assessment['emergency_alert_required'] = False
        else:
            risk_assessment['risk_level'] = 'LOW'
            risk_assessment['emergency_alert_required'] = False
        
        return risk_assessment
    
    def _generate_recommendations(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on risk level"""
        
        recommendations = []
        risk_level = risk_assessment['risk_level']
        
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "Immediate professional intervention required",
                "Contact emergency services if imminent danger",
                "Ensure user is not alone",
                "Remove potential means of self-harm",
                "Contact parent/guardian immediately"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "Urgent professional mental health assessment needed",
                "Contact parent/guardian within 24 hours",
                "Schedule appointment with mental health professional",
                "Increase monitoring and support",
                "Provide crisis hotline information"
            ])
        elif risk_level == 'MODERATE':
            recommendations.extend([
                "Consider professional mental health support",
                "Monitor mood and behavior changes",
                "Encourage healthy coping strategies",
                "Maintain regular check-ins",
                "Provide mental health resources"
            ])
        else:
            recommendations.extend([
                "Continue supportive conversation",
                "Encourage positive activities",
                "Provide general mental health resources",
                "Regular wellness check-ins"
            ])
        
        return recommendations
    
    def _update_user_history(self, user_id: str, risk_assessment: Dict[str, Any]) -> None:
        """Update user's risk history for tracking patterns"""
        
        if user_id not in self.user_risk_history:
            self.user_risk_history[user_id] = []
        
        # Store simplified risk data
        history_entry = {
            'timestamp': risk_assessment['timestamp'],
            'risk_level': risk_assessment['risk_level'],
            'risk_score': risk_assessment['risk_score'],
            'emergency_alert_sent': risk_assessment['emergency_alert_required']
        }
        
        self.user_risk_history[user_id].append(history_entry)
        
        # Keep only last 50 entries per user
        if len(self.user_risk_history[user_id]) > 50:
            self.user_risk_history[user_id] = self.user_risk_history[user_id][-50:]
    
    def get_user_risk_pattern(self, user_id: str) -> Dict[str, Any]:
        """Get user's risk pattern analysis"""
        
        if user_id not in self.user_risk_history:
            return {'pattern': 'no_data', 'risk_trend': 'unknown'}
        
        history = self.user_risk_history[user_id]
        recent_history = history[-10:]  # Last 10 assessments
        
        # Analyze risk pattern
        high_risk_count = sum(1 for entry in recent_history if entry['risk_level'] in ['HIGH', 'CRITICAL'])
        emergency_alerts_sent = sum(1 for entry in recent_history if entry['emergency_alert_sent'])
        
        pattern_analysis = {
            'total_assessments': len(history),
            'recent_high_risk_count': high_risk_count,
            'emergency_alerts_sent': emergency_alerts_sent,
            'risk_trend': self._calculate_risk_trend(recent_history),
            'last_assessment': history[-1] if history else None
        }
        
        return pattern_analysis
    
    def _calculate_risk_trend(self, recent_history: List[Dict[str, Any]]) -> str:
        """Calculate risk trend (improving, worsening, stable)"""
        
        if len(recent_history) < 3:
            return 'insufficient_data'
        
        # Convert risk levels to numerical values for trend analysis
        risk_values = []
        for entry in recent_history:
            if entry['risk_level'] == 'CRITICAL':
                risk_values.append(4)
            elif entry['risk_level'] == 'HIGH':
                risk_values.append(3)
            elif entry['risk_level'] == 'MODERATE':
                risk_values.append(2)
            else:
                risk_values.append(1)
        
        # Simple trend calculation
        first_half = np.mean(risk_values[:len(risk_values)//2])
        second_half = np.mean(risk_values[len(risk_values)//2:])
        
        if second_half > first_half + 0.5:
            return 'worsening'
        elif first_half > second_half + 0.5:
            return 'improving'
        else:
            return 'stable'

# Global instance for use throughout the application
risk_analyzer = DepressionRiskAnalyzer()