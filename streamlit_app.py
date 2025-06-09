import streamlit as st
import json
import os
import time
from datetime import datetime
import uuid

CHAT_FILE = "chat.json"

# Initialize chat file if not exists
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump({}, f)

# Function to load messages
def load_messages():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

# Function to save a message
def save_message(username, message):
    messages = load_messages()
    msg_id = str(uuid.uuid4())
    messages[msg_id] = {
        "user": username,
        "message": message,
        "timestamp": time.time()
    }
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# UI
st.set_page_config("PQ Chatting")
st.title("PQ Chatting")

username = st.text_input("Your name", max_chars=20)
message = st.text_input("Enter your message", max_chars=200)

if st.button("Send") and username and message:
    save_message(username, message)
    st.experimental_rerun()

# Load and show messages
messages = load_messages()
sorted_msgs = sorted(messages.values(), key=lambda x: x["timestamp"])

st.subheader("📜 Chat History")
for msg in sorted_msgs:
    timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
    st.markdown(f"**[{timestamp}] {msg['user']}**: {msg['message']}")

# Auto-refresh every 5 seconds
st.rerun()