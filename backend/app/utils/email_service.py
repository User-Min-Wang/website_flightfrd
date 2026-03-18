from flask_mail import Mail
import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

mail = Mail()

def init_app(app):
    """Initialize mail extension"""
    mail.init_app(app)


def generate_verification_token(email):
    """Generate email verification token"""
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='email-verify-salt')


def verify_verification_token(token, expiration=3600):
    """Verify email verification token"""
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-verify-salt', max_age=expiration)
        return email
    except:
        return None


def send_verification_email(user_email, username, token):
    """Send email verification email"""
    from flask_mail import Message
    
    # Create verification link (frontend URL should be configured)
    frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5173')
    verification_link = f"{frontend_url}/verify-email/{token}"
    
    msg = Message(
        subject='FlightFRD - 验证您的邮箱地址',
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[user_email]
    )
    
    # HTML content
    msg.html = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2c3e50;">欢迎加入 FlightFRD!</h2>
        <p>亲爱的 {username}，</p>
        <p>感谢您注册 FlightFRD 航班追踪系统。请点击以下链接验证您的邮箱地址：</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_link}" 
               style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                验证邮箱
            </a>
        </div>
        <p>或者复制以下链接到浏览器：</p>
        <p style="word-break: break-all; color: #3498db;">{verification_link}</p>
        <p>此链接将在 1 小时后失效。</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="color: #7f8c8d; font-size: 12px;">如果您没有注册此账户，请忽略此邮件。</p>
        <p style="color: #7f8c8d; font-size: 12px;">© 2024 FlightFRD. All rights reserved.</p>
    </div>
    '''
    
    # Plain text content
    msg.body = f'''
欢迎加入 FlightFRD!

亲爱的 {username}，

感谢您注册 FlightFRD 航班追踪系统。请点击以下链接验证您的邮箱地址：

{verification_link}

此链接将在 1 小时后失效。

如果您没有注册此账户，请忽略此邮件。

© 2024 FlightFRD. All rights reserved.
    '''
    
    mail.send(msg)
