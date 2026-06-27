import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# Email Send Karne Ki Function
# ============================================
def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Search answer ko email kar do
    """
    try:
        # Gmail connection
        yag = yagmail.SMTP(
            user=os.getenv("SENDER_EMAIL"),
            password=os.getenv("EMAIL_APP_PASSWORD")
        )

        # Email send karo
        yag.send(
            to=to_email,
            subject=subject,
            contents=body
        )

        print(f"✅ Email successfully sent to: {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email send karne mein error: {e}")
        return False


# ============================================
# Test Karo
# ============================================
if __name__ == "__main__":
    # Test email
    test_result = """
    Search Query: What is latest AI news in 2025?
    
    Answer: The latest news about artificial intelligence in 2025 
    includes advancements in natural language processing, the expansion 
    of AI beyond screens, and its impact on national policy, global 
    trade relations, and the stock market.
    """

    send_email(
        to_email=os.getenv("SENDER_EMAIL"),  # Apne aap ko email
        subject="🤖 AI Search Agent - Results",
        body=test_result
    )