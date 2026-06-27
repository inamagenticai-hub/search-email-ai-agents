import streamlit as st
import os
from dotenv import load_dotenv

# ============================================
# Keys Load Karo - Local aur Cloud dono ke liye
# ============================================
# Pehle .env se try karo (local machine ke liye)
load_dotenv()

# Agar Streamlit Cloud par hai to st.secrets se lo
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["SERPAPI_API_KEY"] = st.secrets["SERPAPI_API_KEY"]
    os.environ["SENDER_EMAIL"] = st.secrets["SENDER_EMAIL"]
    os.environ["EMAIL_APP_PASSWORD"] = st.secrets["EMAIL_APP_PASSWORD"]

from agent import search_and_answer
from email_sender import send_email

# ============================================
# Page Config
# ============================================
st.set_page_config(
    page_title="🤖 AI Search Agent",
    page_icon="🤖",
    layout="centered"
)

# ============================================
# Header
# ============================================
st.title("🤖 AI Search & Email Agent")
st.markdown("**Internet par search karo aur result email par pao!**")
st.divider()

# ============================================
# Search Section
# ============================================
st.subheader("🔍 Apna Sawal Likho")

query = st.text_input(
    label="Search Query",
    placeholder="Jaise: What is latest AI news in 2025?",
    label_visibility="collapsed"
)

email = st.text_input(
    label="Email Address",
    placeholder="Apni email likho jahan result bhejni hai...",
    label_visibility="collapsed"
)

# ============================================
# Search Button
# ============================================
if st.button("🔍 Search Karo & Email Bhejo", type="primary", use_container_width=True):
    if not query:
        st.error("❌ Pehle koi sawal likho!")
    elif not email:
        st.error("❌ Email address zaroor likho!")
    else:
        with st.spinner("🔍 Internet par search ho rahi hai..."):
            answer = search_and_answer(query)

        st.success("✅ Answer mil gaya!")
        st.divider()
        st.subheader("📋 Search Result:")
        st.write(answer)
        st.divider()

        with st.spinner("📧 Email bhej raha hai..."):
            email_body = f"""
🤖 AI Search Agent - Result

Aapka Sawal:
{query}

Jawab:
{answer}

---
Yeh email AI Search Agent ne automatically bheji hai.
            """
            success = send_email(
                to_email=email,
                subject=f"🤖 AI Search Result: {query[:50]}",
                body=email_body
            )

        if success:
            st.success(f"📧 Email successfully {email} par bhej di gayi!")
        else:
            st.error("❌ Email bhejne mein masla hua. Keys check karo.")

# ============================================
# Footer
# ============================================
st.divider()
st.markdown(
    "<center>Made with ❤️ using LangChain, LangGraph, Groq & Streamlit</center>",
    unsafe_allow_html=True
)