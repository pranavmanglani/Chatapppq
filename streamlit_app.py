import streamlit as st
import json
import os
import time
from datetime import datetime
import uuid

# Constants
CHAT_FILE = "chat.json"
RESERVED_NAMES = ["PQ:ADMIN"]
ADMIN_PASSWORD = "pranav1875"  # 👈 Change this to your own secret password

# Initialize chat file if not exists
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump({}, f)

# Load messages
def load_messages():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

# Save a message
def save_message(username, message, recipient=None):
    messages = load_messages()
    msg_id = str(uuid.uuid4())
    messages[msg_id] = {
        "user": username,
        "message": message,
        "timestamp": time.time(),
        "recipient": recipient
    }
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# Delete a message
def delete_message(msg_id):
    messages = load_messages()
    if msg_id in messages:
        del messages[msg_id]
        with open(CHAT_FILE, "w") as f:
            json.dump(messages, f)

# Streamlit UI
st.set_page_config("Local Chat Room")
st.title("💬 CMS Local Chat Room")
st.text('''https://youtu.be/G8A-sRPsHxw?feature=shared''')

# Sidebar for navigation
page = st.sidebar.radio("Select a Page", ["Chat Room", "Rules"])

if page == "Rules":
    st.subheader("📜 Chat Rules")
    st.markdown("""
    1. **Respect Others**: Be kind and respectful in your messages.

    2. **No Spam**: Avoid sending irrelevant or excessive messages.

    3. **Report Issues**: If you face any issues, contact an admin.

    4. **Admins Have the Final Say**: Admins can remove inappropriate content.
    5. Saying PQ without a verified 7q student will result in ban of 3 days

Abusive language is allowed to an extent and roasting others is allowed 

Creted by student of 8th C.

if u want the code dm PQ:ADMIN
    """)

else:
    # User input
    username = st.text_input("Your name", max_chars=20)
    message = st.text_input("Enter your message", max_chars=200)

    # Admin password (only needed if using reserved name)
    admin_password = ""
    is_admin = False
    if username.strip().upper() == "PQ:ADMIN":
        admin_password = st.text_input("Admin Password", type="password")
        if admin_password == ADMIN_PASSWORD:
            is_admin = True

    # Direct message (DM) feature
    users = [msg["user"] for msg in load_messages().values()]
    users = list(set(users))  # Unique users
    dm_recipient = st.selectbox("Send DM to", [""] + users)

    # Send message logic
    if st.button("Send"):
        if not username or not message:
            st.warning("Please enter both name and message.")
        elif username.strip().upper() in [name.upper() for name in RESERVED_NAMES]:
            if not is_admin:
                st.error("Username 'PQ:ADMIN' is reserved. Invalid password.")
            else:
                save_message(username, message)
                st.rerun()
        else:
            save_message(username, message, recipient=dm_recipient)
            st.rerun()

    # Load and sort messages
    messages = load_messages()
    sorted_msgs = sorted(messages.items(), key=lambda x: x[1]["timestamp"])

    # Display chat
    st.subheader("📜 Chat History")
    for msg_id, msg in sorted_msgs:
        timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
        user = msg["user"]
        text = msg["message"]
        recipient = msg.get("recipient")

        col1, col2 = st.columns([10, 1])
        with col1:
            if user.strip().upper() == "PQ:ADMIN":
                st.markdown(
                    f"<span style='color:red; font-weight:bold;'>[{timestamp}] {user}: {text}</span>",
                    unsafe_allow_html=True
                )
            elif recipient and recipient == username:
                st.markdown(f"**[DM - {timestamp}] {user}**: {text}")
            else:
                st.markdown(f"**[{timestamp}] {user}**: {text}")
        with col2:
            if is_admin:
                if st.button("🗑️", key=msg_id):
                    delete_message(msg_id)
                    st.rerun()