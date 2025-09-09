import smtplib
from email.mime.text import MIMEText

mail_server = "smtp.gmail.com"
server_port = 587
sender_address = "adityaaryan151@gmail.com"
app_password = "kuoifqwzhtyapwnq"
recipient_address = "adityaaryan2135@gmail.com"

email_content = MIMEText("Test message generated using Python SMTP implementation.")
email_content["Subject"] = "Email Protocol Testing"
email_content["From"] = sender_address
email_content["To"] = recipient_address

try:
    smtp_connection = smtplib.SMTP(mail_server, server_port)
    smtp_connection.set_debuglevel(1)
    smtp_connection.starttls()
    smtp_connection.login(sender_address, app_password)
    smtp_connection.sendmail(sender_address, recipient_address, email_content.as_string())
    print("\nFantastic! The email was sent successfully to the recipient!")
except Exception as email_error:
    print(f"Unfortunately, I couldn't send the email because: {email_error}")
finally:
    if 'smtp_connection' in locals():
        smtp_connection.quit()
