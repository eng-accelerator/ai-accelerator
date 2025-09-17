"""
Example 2: Session State Deep Dive

Key Teaching Points:
- st.session_state acts like a dictionary that persists across reruns
- Essential for maintaining application state
- Foundation for chat history, user preferences, and complex interactions
"""

import streamlit as st

st.title("🧠 Session State Mastery")

st.write("""
Session state is your persistence layer. Think of it as a dictionary that
survives script reruns - essential for any stateful application.
""")

# Initialize different types of session state variables
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
    # session_state = {
    #     "message_count": 0
    # }

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []

if "user_settings" not in st.session_state:
    st.session_state.user_settings = {
        "theme": "light",
        "notifications": True
    }

# Counter demonstration
col1, col2 = st.columns(2)

with col1:
    st.subheader("Counter Example")
    if st.button("Increment Counter"):
        st.session_state.message_count += 1

    st.write(f"Current count: {st.session_state.message_count}")

    if st.button("Reset Counter"):
        st.session_state.message_count = 0

with col2:
    st.subheader("List Example")
    new_message = st.text_input("Add a message:")

    if st.button("Add Message") and new_message:
        st.session_state.user_messages.append(new_message)

    st.write("Messages:")
    for i, msg in enumerate(st.session_state.user_messages):
        st.write(f"{i+1}. {msg}")

    if st.button("Clear Messages"):
        st.session_state.user_messages = []

# Settings demonstration
st.subheader("Settings Dictionary Example")
theme = st.selectbox(
    "Choose theme:",
    ["light", "dark"],
    index=0 if st.session_state.user_settings["theme"] == "light" else 1
)

notifications = st.checkbox(
    "Enable notifications",
    value=st.session_state.user_settings["notifications"]
)

# Update settings in session state
st.session_state.user_settings["theme"] = theme
st.session_state.user_settings["notifications"] = notifications

st.write("Current settings:", st.session_state.user_settings)

# Show the raw session state
st.write("---")
with st.expander("🔍 Raw Session State Contents"):
    st.write("Here's everything in your session state:")
    st.json(dict(st.session_state))

# Teaching notes
with st.expander("🎓 Teaching Notes"):
    st.write("""
    **Key Patterns Demonstrated:**

    1. **Initialization Pattern:**
    ```python
    if "key" not in st.session_state:
        st.session_state.key = initial_value
    ```

    2. **Common Data Types:**
    - Counters (integers)
    - Lists (for chat history, user inputs)
    - Dictionaries (for complex settings)

    3. **Best Practices:**
    - Always check if key exists before using
    - Use descriptive key names
    - Group related data in dictionaries
    - Clear state when needed for reset functionality
    """)
