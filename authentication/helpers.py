import environ
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

env = environ.Env()


def sendVerificationMail(toEmail, otpCode):
    message = Mail(
        from_email="speedyparth04@gmail.com",
        to_emails=toEmail,
        subject='Verify Eventory Account with OTP',
        html_content=f'<strong>Otp Verification Code {otpCode}</strong>')
    try:
        sg = SendGridAPIClient(env('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        return e.message


def sendVerificationSMS(toNumber, otpCode):
    account_sid = env('TWILLO_ACCOUNT_SID')
    auth_token = env('TWILLO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Verify Your Eventory account with the Otp:- '+otpCode,
        from_=env("TWILLO_PHONE_NUMBER"),
        to="+91"+toNumber
    )
    return message.sid
