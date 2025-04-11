import streamlit as st
import requests
from streamlit_chat import message

st.set_page_config(page_title="SSF Scholarship Assistant", page_icon="🎓")
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🎓 SSF Scholarship Assistant</h1>",
    unsafe_allow_html=True
)

# Background image using CSS (optional styling)
st.markdown(
    """
    <style>
        .stApp {
            background-image: url('https://source.unsplash.com/featured/?student,books,education');
            background-size: cover;
        }
        .stTextInput > div > div > input {
            background-color: #fff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input box
user_input = st.chat_input("How can I help you with your scholarship application or renewal?")

# Display chat history
for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
    message(user_msg, is_user=True, avatar_style="thumbs", key=f"user-{i}")
    message(bot_msg, is_user=False, avatar_style="fun-emoji", key=f"bot-{i}")

# Send new message to backend and get response
if user_input:
    st.session_state.chat_history.append((user_input, "⏳ Thinking..."))
    
    # Render the user's message immediately
    message(user_input, is_user=True, avatar_style="thumbs", key=f"user-{len(st.session_state.chat_history)}")

    try:
        response = requests.post(
            "https://scholarship-assistant.onrender.com/chat",  # Your Render backend
            json={"user_input": user_input},
            timeout=20
        )

        if response.status_code == 200:
            bot_response = response.json().get("response", "Something went wrong.")
        else:
            bot_response = "❌ Failed to reach the assistant. Please try again later."

    except Exception as e:
        bot_response = f"⚠️ Error: {e}"

    # Replace temporary bot message with actual one
    st.session_state.chat_history[-1] = (user_input, bot_response)

    # Show updated bot message
    message(bot_response, is_user=False, avatar_style="fun-emoji", key=f"bot-{len(st.session_state.chat_history)}")
