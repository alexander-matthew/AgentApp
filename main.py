import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Union


class BaseAgent:
    """Simple base class for Anthropic API interactions"""

    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=api_key)

    def send_message(self, system_prompt: str, user_message: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_message
                            }
                        ]
                    }
                ]
            )
            return message.content[0].text

        except Exception as e:
            print(f"Error calling Claude: {e}")
            raise


class QuoteGenerator(BaseAgent):
    """Generate daily motivational quotes using Claude"""

    def __init__(self):
        super().__init__()
        self.system_prompt = """You are an agent based model tasked with generating 
        motivational quotes each day. Please only return your quote as the response."""

    def get_quote(self, date=None):
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%A %B %d")
        return self.send_message(
            system_prompt=self.system_prompt,
            user_message=f"It is {date_str}. Please generate me a quote"
        )


class EmailComposer(BaseAgent):
    """Compose and send emails with daily quotes"""

    def __init__(self):
        super().__init__()
        self.quote_generator = QuoteGenerator()
        self.system_prompt = """You are an email composition expert. 
        Create a professional and engaging email that incorporates a motivational quote.
        The email should be warm and professional. Return the email with clear Subject: and Body: sections."""

        # Email configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.sender_password = os.environ.get("SENDER_APP_PASSWORD")

        if not all([self.sender_email, self.sender_password]):
            raise ValueError("Email credentials not found in environment variables")

    def compose_quote_email(self, recipient_name: str = "Team") -> tuple[str, str]:
        """Composes email and returns subject and body separately"""
        quote = self.quote_generator.get_quote()
        date_str = datetime.now().strftime("%A, %B %d, %Y")

        email_request = f"""
        Compose a brief email for {recipient_name} that shares this quote:
        "{quote}"

        The email should:
        1. Be dated {date_str}
        2. Have a subject line
        3. Include a warm greeting
        4. Provide a brief context for the quote
        5. End with a professional signature

        Return the email with 'Subject:' on first line and 'Body:' on second line,
        followed by the content. Keep the subject line brief and engaging.
        """

        response = self.send_message(
            system_prompt=self.system_prompt,
            user_message=email_request
        )

        # Split response into subject and body
        lines = response.split('\n', 2)
        subject = lines[0].replace('Subject:', '').strip()
        body = lines[2].replace('Body:', '').strip()

        return subject, body

    def send_email(self, recipients: Union[str, List[str]], subject: str, body: str):
        """Send email to one or multiple recipients"""
        if isinstance(recipients, str):
            recipients = [recipients]

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"Email sent successfully to {len(recipients)} recipients")

        except Exception as e:
            print(f"Error sending email: {e}")
            raise

    def send_quote_email(self, mailing_list: Union[str, List[str]], recipient_name: str = "Team"):
        """Compose and send quote email to mailing list"""
        subject, body = self.compose_quote_email(recipient_name)
        self.send_email(mailing_list, subject, body)


def main():
    try:
        # Create email composer
        email_composer = EmailComposer()

        # Example mailing list
        mailing_list = [
            "recipient1@example.com",
            "recipient2@example.com"
        ]

        # Send email to the mailing list
        email_composer.send_quote_email(mailing_list, "Team")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()