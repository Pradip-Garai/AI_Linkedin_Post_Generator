import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_password_email(receiver_email,password):
    
    # Email credentialss
    sender_email = "studytimes116@gmail.com"
    app_password = "iujh ojvd cnkz lkkw"
    
    # Create the email
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Reset Your Password 🔐"
    
    # HTML Email Template
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          <h2 style="color: #333333;">Linkedin Post Generator</h2>
          <p>Hi 👋,</p>
          <p>We received a request to reset your password.</p>
          <h1 style="color: #1a73e8; letter-spacing: 2px;">{password}</h1>
          <p style="color: #555555;">This OTP is valid for <strong>2 minutes</strong>. Do not share it with anyone.</p>
          <hr>
          <p style="font-size: 12px; color: #888888;">If you did not request this, please ignore this email.</p>
        </div>
      </body>
    </html>
    """
    
    # Attach HTML content
    msg.attach(MIMEText(html, "html"))
    
    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Enable security
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()
    
    print("OTP sent successfully via email!")
    return password

