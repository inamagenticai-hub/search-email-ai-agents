import streamlit as st
import os
from dotenv import load_dotenv

# ============================================
# Keys Load Karo - Local aur Cloud dono ke liye
# ============================================
load_dotenv()

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
st.markdown("**Internet par search karo aur result email par bhi pao!**")
st.divider()

# ============================================
# Search Input
# ============================================
st.subheader("🔍 Apna Sawal Likho")
query = st.text_input(
    label="Search Query",
    placeholder="Jaise: What is latest AI news in 2025?",
    label_visibility="collapsed"
)

# ============================================
# Email Input - Optional
# ============================================
st.subheader("📧 Email Address (Optional)")
st.caption("Agar result email par chahiye to email likho, warna khali chhod do")
email = st.text_input(
    label="Email Address",
    placeholder="apki_email@gmail.com (optional)",
    label_visibility="collapsed"
)

st.divider()

# ============================================
# Search Button
# ============================================
if st.button("🔍 Search Karo", type="primary", use_container_width=True):

    # Sirf query check karo - email optional hai
    if not query:
        st.error("❌ Pehle koi sawal likho!")

    else:
        # ----------------------------------------
        # Search Karo
        # ----------------------------------------
        with st.spinner("🔍 Internet par search ho rahi hai... Thoda wait karo..."):
            answer = search_and_answer(query)

        # Answer Screen Par Dikhao
        st.success("✅ Answer mil gaya!")
        st.divider()
        st.subheader("📋 Search Result:")
        st.write(answer)
        st.divider()

        # ----------------------------------------
        # Email - Sirf Tab Bhejo Jab Email Di Ho
        # ----------------------------------------
        if email:
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
                st.success(f"📧 Email successfully **{email}** par bhej di gayi!")
            else:
                st.error("❌ Email bhejne mein masla hua. Keys check karo.")

        else:
            # Email nahi di to sirf yeh message dikhao
            st.info("ℹ️ Email provide nahi ki — Result sirf screen par show kiya gaya!")

# ============================================
# Footer
# ============================================
st.divider()
st.markdown(
    "<center>Made with ❤️ using LangChain, LangGraph, Groq & Streamlit</center>",
    unsafe_allow_html=True
)