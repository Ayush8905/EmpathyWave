#!/usr/bin/env python3
"""
Emergency Email Service for EmpathyWave
Sends emergency notifications to parents when high-risk depression is detected
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyEmailService:
    """Service for sending emergency email notifications to parents"""
    
    def __init__(self):
        """Initialize email service with configuration"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'empathywave.support@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.app_name = "EmpathyWave Mental Health Support"
        
        # Check if we should use demo mode or real email
        self.demo_mode = os.getenv('EMAIL_DEMO_MODE', 'true').lower() == 'true'
        self.force_real_email = os.getenv('FORCE_REAL_EMAIL', 'false').lower() == 'true'
        
        # If password is provided or real email is forced, disable demo mode
        if self.sender_password and self.sender_password.strip() != '':
            self.demo_mode = False
        if self.force_real_email:
            self.demo_mode = False
            
        # Log configuration
        logger.info(f"Email Service Configuration:")
        logger.info(f"  SMTP Server: {self.smtp_server}:{self.smtp_port}")
        logger.info(f"  Sender Email: {self.sender_email}")
        logger.info(f"  Demo Mode: {'✅ ENABLED' if self.demo_mode else '❌ DISABLED (REAL EMAILS)'}")
        logger.info(f"  Password Configured: {'✅ YES' if self.sender_password else '❌ NO'}")
        
        # Email templates
        self.emergency_template = self._get_emergency_template()
        
    def _get_emergency_template(self) -> str:
        """Get HTML template for emergency email"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EmpathyWave Emergency Alert</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                    margin: -30px -30px 30px -30px;
                    text-align: center;
                }}
                .alert-badge {{
                    background: #dc3545;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                    display: inline-block;
                    margin-bottom: 15px;
                }}
                .content {{
                    margin: 20px 0;
                }}
                .risk-level {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .risk-level.high {{
                    background: #f8d7da;
                    border-color: #f5c6cb;
                    color: #721c24;
                }}
                .risk-level.critical {{
                    background: #d1ecf1;
                    border-color: #bee5eb;
                    color: #0c5460;
                }}
                .recommendations {{
                    background: #e8f5e8;
                    border-left: 4px solid #28a745;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .contact-info {{
                    background: #f8f9fa;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .emergency-contacts {{
                    background: #dc354530;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                    border: 2px solid #dc3545;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 14px;
                }}
                .button {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 25px;
                    margin: 10px 0;
                    font-weight: bold;
                }}
                .highlight {{
                    background: #fff3cd;
                    padding: 2px 6px;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌊 {app_name}</h1>
                    <div class="alert-badge">🚨 EMERGENCY ALERT</div>
                    <h2>Mental Health Support Notification</h2>
                </div>
                
                <div class="content">
                    <p><strong>Dear Parent/Guardian,</strong></p>
                    
                    <p>We are reaching out regarding <span class="highlight">{user_email}</span> who has been using our mental health support platform, EmpathyWave.</p>
                    
                    <div class="risk-level {risk_class}">
                        <h3>🚨 Risk Assessment: {risk_level}</h3>
                        <p><strong>Detection Time:</strong> {timestamp}</p>
                        <p><strong>Analysis Summary:</strong> Our AI system has detected indicators suggesting your child may be experiencing significant mental health challenges that require immediate attention.</p>
                    </div>
                    
                    <div class="recommendations">
                        <h3>📋 Immediate Recommendations:</h3>
                        <ul>
                            <li><strong>Talk to your child</strong> - Have an open, non-judgmental conversation about their feelings</li>
                            <li><strong>Seek professional help</strong> - Contact a mental health professional or your family doctor</li>
                            <li><strong>Monitor closely</strong> - Keep a closer eye on their mood and behavior</li>
                            <li><strong>Remove potential risks</strong> - Ensure a safe environment at home</li>
                            <li><strong>Show support</strong> - Let them know you love and support them unconditionally</li>
                        </ul>
                    </div>
                    
                    <div class="emergency-contacts">
                        <h3>🆘 Emergency Contacts (24/7 Support):</h3>
                        <p><strong>National Suicide Prevention Lifeline:</strong> <a href="tel:988">988</a></p>
                        <p><strong>Crisis Text Line:</strong> Text HOME to <a href="sms:741741">741741</a></p>
                        <p><strong>Emergency Services:</strong> <a href="tel:911">911</a></p>
                        <p><strong>SAMHSA National Helpline:</strong> <a href="tel:1-800-662-4357">1-800-662-HELP (4357)</a></p>
                    </div>
                    
                    <div class="contact-info">
                        <h3>📞 Professional Support Options:</h3>
                        <p>• Contact your family physician for a referral to a mental health specialist</p>
                        <p>• Reach out to your school counselor or psychologist</p>
                        <p>• Consider family therapy to address concerns together</p>
                        <p>• Look into local mental health resources and support groups</p>
                    </div>
                    
                    <p><strong>Important Note:</strong> This alert was generated by our AI analysis system based on interactions with our platform. While our technology is advanced, it should not replace professional medical advice. Please consult with qualified mental health professionals for proper assessment and treatment.</p>
                    
                    <p>Your child's wellbeing is our top priority. We encourage you to take this notification seriously and seek appropriate support.</p>
                    
                    <center>
                        <a href="https://suicidepreventionlifeline.org/" class="button">Find Local Resources</a>
                    </center>
                </div>
                
                <div class="footer">
                    <p>This message was sent by {app_name} Emergency Alert System</p>
                    <p>Generated on {timestamp}</p>
                    <p>If you have questions about this alert, please reply to this email.</p>
                    <p><em>Remember: You are not alone. Help is available.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def send_emergency_alert(self, user_data: Dict[str, Any], risk_assessment: Dict[str, Any]) -> bool:
        """
        Send emergency alert to parent when high-risk depression is detected
        
        Args:
            user_data: Dictionary containing user information (email, parent_email, etc.)
            risk_assessment: Dictionary containing risk level and analysis details
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not user_data.get('parent_email'):
                logger.warning(f"No parent email found for user {user_data.get('email', 'unknown')}")
                return False
                
            # Check if we should send real email or simulate
            if self.demo_mode:
                logger.info("🚨 DEMO MODE: Emergency alert simulation")
                logger.info(f"   👤 User: {user_data.get('email', 'unknown')}")
                logger.info(f"   📧 Parent Email: {user_data.get('parent_email', 'unknown')}")
                logger.info(f"   ⚠️  Risk Level: {risk_assessment.get('level', 'HIGH')}")
                logger.info(f"   📊 Risk Score: {risk_assessment.get('score', 'unknown')}")
                logger.info("   � Email Content: Crisis resources + Emergency contacts + Professional guidance")
                logger.info("   💡 To send real emails: Set SENDER_PASSWORD in .env and restart app")
                return True  # Return success for demo mode
            
            # Real email mode - validate credentials
            if not self.sender_password or self.sender_password.strip() == '':
                logger.error("❌ Real email mode requires SENDER_PASSWORD. Set it in .env file.")
                logger.error("   💡 Get Gmail App Password: https://support.google.com/accounts/answer/185833")
                return False
                
            logger.info(f"📧 SENDING REAL EMAIL to {user_data.get('parent_email', 'unknown')}")
            logger.info(f"   Risk Level: {risk_assessment.get('level', 'HIGH')}")
            logger.info(f"   Risk Score: {risk_assessment.get('score', 'unknown')}")
            
            # Prepare email content
            subject = f"🚨 URGENT: Mental Health Alert for {user_data.get('email', 'your child')}"
            
            # Determine risk class for styling
            risk_level = risk_assessment.get('level', 'HIGH')
            risk_class = 'critical' if risk_level == 'CRITICAL' else 'high'
            
            # Format HTML content
            html_content = self.emergency_template.format(
                app_name=self.app_name,
                user_email=user_data.get('email', 'your child'),
                risk_level=risk_level,
                risk_class=risk_class,
                timestamp=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                analysis_summary=risk_assessment.get('summary', 'AI analysis indicates elevated mental health risk')
            )
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = user_data['parent_email']
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, user_data['parent_email'], message.as_string())
            
            logger.info(f"Emergency alert sent successfully to {user_data['parent_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send emergency alert: {str(e)}")
            return False
    
    def send_follow_up_email(self, user_data: Dict[str, Any], resources: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send follow-up email with additional resources and support information
        
        Args:
            user_data: Dictionary containing user information
            resources: Optional dictionary with additional resources
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not user_data.get('parent_email'):
                return False
                
            subject = f"Follow-up Support Resources - {self.app_name}"
            
            # Create follow-up content (simplified for now)
            content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2>Follow-up Mental Health Resources</h2>
                <p>Dear Parent/Guardian,</p>
                <p>This is a follow-up to our previous emergency alert regarding {user_data.get('email', 'your child')}.</p>
                
                <h3>Additional Resources:</h3>
                <ul>
                    <li>Local mental health professionals directory</li>
                    <li>Teen depression support groups</li>
                    <li>Family counseling services</li>
                    <li>Online mental health resources</li>
                </ul>
                
                <p>We hope this information is helpful. Please don't hesitate to seek professional support.</p>
                
                <p>Best regards,<br>{self.app_name} Support Team</p>
            </body>
            </html>
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = user_data['parent_email']
            
            html_part = MIMEText(content, "html")
            message.attach(html_part)
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, user_data['parent_email'], message.as_string())
            
            logger.info(f"Follow-up email sent successfully to {user_data['parent_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send follow-up email: {str(e)}")
            return False

# Global instance for use throughout the application
email_service = EmergencyEmailService()