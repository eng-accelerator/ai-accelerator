"""
Example 3: Building Modern Chat Interfaces

Key Teaching Points:
- st.chat_message creates professional chat bubbles
- st.chat_input provides a modern input experience
- Chat history pattern using session state
- Role-based message display (user vs assistant)
"""

import streamlit as st
import time
import random

st.title("💬 Chat Interface Components")

st.write("""
Modern AI applications need chat-style interfaces. Streamlit provides
specialized components that make this easy and professional-looking.
""")

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I'm your demo assistant. Try sending me a message!"}
    ]

# Display existing chat messages
st.subheader("Chat Display")
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    # Display user message immediately
    with st.chat_message("user"):
        st.write(prompt)

    # Simulate assistant response
    with st.chat_message("assistant"):
        # Show typing indicator
        with st.spinner("Assistant is typing..."):
            time.sleep(1)  # Simulate processing time

        # Generate a simple demo response
        responses = [
            f"I received your message: '{prompt}' - that's interesting!",
            f"You said: '{prompt}'. I'm just a demo, but that sounds great!",
            f"Thanks for the message: '{prompt}'. In a real app, I'd give you a smart response!",
            f"'{prompt}' - I hear you! This is how chat interfaces work in Streamlit."
        ]
        response = random.choice(responses)
        st.write(response)

        # Add assistant response to history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})

# Chat controls
st.write("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Clear Chat"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Chat cleared! Send me a new message."}
        ]

with col2:
    message_count = len([msg for msg in st.session_state.chat_messages if msg["role"] == "user"])
    st.metric("Messages Sent", message_count)

with col3:
    total_chars = sum(len(msg["content"]) for msg in st.session_state.chat_messages)
    st.metric("Total Characters", total_chars)

# Component showcase
st.write("---")
st.subheader("Component Showcase")

# Different message types
with st.chat_message("user"):
    st.write("This is how user messages appear")

with st.chat_message("assistant"):
    st.write("This is how assistant messages appear")

with st.chat_message("user"):
    st.write("Messages can contain **markdown** and `code`!")

with st.chat_message("assistant"):
    st.code("""
# Even code blocks work great
def hello_world():
    return "Hello from the chat!"
    """)

# Teaching notes
with st.expander("🎓 Teaching Notes"):
    st.write("""
    **Key Components & Patterns:**

    1. **st.chat_message(role):** Creates styled message bubbles
       - "user" for human messages (typically right-aligned, blue)
       - "assistant" for AI responses (typically left-aligned, gray)

    2. **st.chat_input():** Modern input field with submit handling
       - Returns None until user submits
       - Use walrus operator: `if prompt := st.chat_input():`

    3. **Chat History Pattern:**
    ```python
    # Store messages in session state
    messages = [{"role": "user/assistant", "content": "text"}]

    # Display all messages
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle new input
    if prompt := st.chat_input():
        messages.append({"role": "user", "content": prompt})
        # Process and respond...
    ```

    4. **Best Practices:**
    - Always store chat history in session state
    - Use consistent message format (role + content)
    - Display messages before processing new input
    - Provide clear feedback during processing
    """)
