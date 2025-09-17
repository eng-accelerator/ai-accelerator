"""
Example 1: Hello World - Understanding Script Execution

Key Teaching Points:
- Streamlit runs your script from top to bottom on every interaction
- Each widget interaction triggers a complete rerun
- This is fundamentally different from traditional web frameworks
"""

import streamlit as st

# This runs every time the app loads or user interacts
st.title("🌍 Hello Streamlit World!")

st.write("This text appears every time the script runs.")

# Add a button to demonstrate reruns
if st.button("Click Me!"):
    st.write("🎉 Button was clicked! The entire script just ran again.")
    st.balloons()

# Add a text input to show interactive reruns
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! Notice how this updates as you type.")

# Add a counter to visualize reruns
st.write("---")
st.write("**Script Execution Counter:**")
st.write("Every time you see this number change, the entire script ran from top to bottom.")

# This would reset to 0 every time without session_state!
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
st.write(f"Script has run {st.session_state.counter} times")

# Teaching note box
with st.expander("🎓 Teaching Notes"):
    st.write("""
    **Key Concepts Demonstrated:**
    - Script reruns on every interaction
    - Widgets trigger reruns when their values change
    - Session state preserves data across reruns
    - Without session_state, variables would reset every time
    """)
