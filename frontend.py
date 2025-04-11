import streamlit as st
import requests
from streamlit_chat import message

st.set_page_config(page_title="SSF Scholarship Assistant", page_icon="🎓", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
    }
    .main {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .css-1aumxhk {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #2a9d8f;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #21867a;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🎓 SSF AI Assistant")
st.markdown("#### Helping you with your scholarship application or renewal")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input box
user_input = st.chat_input("Type your message...")

# Display existing conversation
for msg in st.session_state.chat_history:
    message(
        msg["content"],
        is_user=(msg["role"] == "user"),
        avatar_style="thumbs" if msg["role"] == "user" else "big-smile"
    )

# Handle new message
if user_input:
    # Append user's message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, avatar_style="thumbs")

    # Send message to backend
    with st.spinner("SSF AI is typing..."):
        try:
            res = requests.post("https://scholarship-assistant.onrender.com/ask-llama", json={"user_message": user_input})
            result = res.json()

            # Check for error response from backend
            if "response" in result:
                assistant_reply = result["response"]
            else:
                assistant_reply = f"⚠️ Error from AI: {result.get('error', 'Unknown error')}"
        
        except Exception as e:
            assistant_reply = f"❌ Failed to connect to backend: {e}"

    # Append assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    message(assistant_reply, is_user=False, avatar_style="big-smile")
