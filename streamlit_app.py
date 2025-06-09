import streamlit as st
import json
import os
import time
from datetime import datetime
import uuid

# Constants
CHAT_FILE = "chat.json"
RESERVED_NAMES = ["PQ:ADMIN"]
ADMIN_PASSWORD = "pranav1875"  # 👈 Change this to your secret admin password

# Initialize chat file if not exists
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump({}, f)

# Load messages
def load_messages():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

# Save a message
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

# Streamlit UI
st.set_page_config("Local Chat Room")
st.title("💬 Local Chat Room")

# User inputs
username = st.text_input("Your name", max_chars=20)
message = st.text_input("Enter your message", max_chars=200)

# Admin password field (only if trying to use PQ:ADMIN)
admin_password = ""
if username.strip().upper() == "PQ:ADMIN":
    admin_password = st.text_input("Admin Password", type="password")

# Send button logic
if st.button("Send"):
    if not username or not message:
        st.warning("Please enter both name and message.")
    elif username.strip().upper() in [name.upper() for name in RESERVED_NAMES]:
        if admin_password != ADMIN_PASSWORD:
            st.error("Username 'PQ:ADMIN' is reserved. Invalid password.")
        else:
            save_message(username, message)
            st.rerun()
    else:
        save_message(username, message)
        st.rerun()

# Load and sort messages
messages = load_messages()
sorted_msgs = sorted(messages.values(), key=lambda x: x["timestamp"])

# Display chat
st.subheader("📜 Chat History")
for msg in sorted_msgs:
    timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
    user = msg["user"]
    text = msg["message"]

    if user.strip().upper() == "PQ:ADMIN":
        st.markdown(
            f"<span style='color:red; font-weight:bold;'>[{timestamp}] {user}: {text}</span>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"**[{timestamp}] {user}**: {text}")