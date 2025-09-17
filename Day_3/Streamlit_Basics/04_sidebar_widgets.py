"""
Example 4: Sidebar Controls and Configuration

Key Teaching Points:
- st.sidebar creates a collapsible side panel for controls
- Perfect for settings, configuration, and secondary actions
- Doesn't interfere with main content area
- Essential for professional app layouts
"""

import streamlit as st

# Configure page
st.set_page_config(page_title="Sidebar Demo", page_icon="⚙️", layout="wide")

st.title("⚙️ Sidebar Controls & Configuration")

st.write("""
The sidebar is perfect for app configuration, settings, and controls that don't
belong in your main content area. It's collapsible and stays consistent across
different pages in multi-page apps.
""")

# Initialize session state for settings
if "app_settings" not in st.session_state:
    st.session_state.app_settings = {
        "theme": "Light",
        "model": "GPT-3.5",
        "temperature": 0.7,
        "max_tokens": 150,
        "show_debug": False
    }

# Sidebar configuration
with st.sidebar:
    st.header("🎛️ App Configuration")

    # Model selection
    model_choice = st.selectbox(
        "Choose AI Model:",
        ["GPT-3.5", "GPT-4", "Claude", "Llama 2"],
        index=["GPT-3.5", "GPT-4", "Claude", "Llama 2"].index(st.session_state.app_settings["model"])
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature (creativity):",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.app_settings["temperature"],
        step=0.1,
        help="Higher values make output more creative but less focused"
    )

    # Max tokens
    max_tokens = st.number_input(
        "Max Tokens:",
        min_value=50,
        max_value=500,
        value=st.session_state.app_settings["max_tokens"],
        step=50
    )

    # Theme selection
    theme = st.radio(
        "App Theme:",
        ["Light", "Dark", "Auto"],
        index=["Light", "Dark", "Auto"].index(st.session_state.app_settings["theme"])
    )

    # Debug mode
    show_debug = st.checkbox(
        "Show Debug Info",
        value=st.session_state.app_settings["show_debug"]
    )

    st.divider()

    # Action buttons
    if st.button("💾 Save Settings", type="primary"):
        st.session_state.app_settings.update({
            "theme": theme,
            "model": model_choice,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "show_debug": show_debug
        })
        st.success("Settings saved!")

    if st.button("🔄 Reset to Defaults"):
        st.session_state.app_settings = {
            "theme": "Light",
            "model": "GPT-3.5",
            "temperature": 0.7,
            "max_tokens": 150,
            "show_debug": False
        }
        st.success("Settings reset!")
        st.rerun()

    # Info section
    with st.expander("ℹ️ About"):
        st.write("""
        This demo shows how to use the sidebar for:
        - App configuration
        - User preferences
        - Secondary controls
        - Information panels
        """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Current Configuration")

    # Display current settings in a nice format
    settings_df = {
        "Setting": list(st.session_state.app_settings.keys()),
        "Value": list(st.session_state.app_settings.values())
    }

    st.table(settings_df)

    # Simulated chat based on settings
    st.subheader("💬 Simulated Chat Response")
    st.write("Here's how your current settings would affect AI responses:")

    with st.chat_message("user"):
        st.write("Tell me about artificial intelligence")

    with st.chat_message("assistant"):
        if st.session_state.app_settings["temperature"] < 0.5:
            response = "Artificial intelligence (AI) refers to the simulation of human intelligence in machines programmed to think and learn."
        elif st.session_state.app_settings["temperature"] < 1.0:
            response = "AI is like giving computers a brain! It's the fascinating field where we teach machines to think, reason, and solve problems just like humans do."
        else:
            response = "🤖 Ah, artificial intelligence! It's the magical realm where silicon dreams meet algorithmic poetry, creating digital minds that dance with data!"

        st.write(f"[Using {st.session_state.app_settings['model']} at temperature {st.session_state.app_settings['temperature']}]")
        st.write(response)

with col2:
    st.subheader("📊 Settings Impact")

    # Visual indicators based on settings
    if st.session_state.app_settings["temperature"] < 0.5:
        st.info("🎯 **Focused Mode**: Responses will be precise and factual")
    elif st.session_state.app_settings["temperature"] < 1.0:
        st.info("⚖️ **Balanced Mode**: Mix of creativity and accuracy")
    else:
        st.warning("🎨 **Creative Mode**: Responses will be very creative but potentially less accurate")

    # Model info
    model_info = {
        "GPT-3.5": "Fast, efficient, good for most tasks",
        "GPT-4": "Most capable, slower, higher cost",
        "Claude": "Great for analysis and reasoning",
        "Llama 2": "Open source, good performance"
    }

    st.info(f"**{st.session_state.app_settings['model']}**: {model_info[st.session_state.app_settings['model']]}")

    # Token usage estimate
    estimated_cost = {
        "GPT-3.5": st.session_state.app_settings["max_tokens"] * 0.002,
        "GPT-4": st.session_state.app_settings["max_tokens"] * 0.06,
        "Claude": st.session_state.app_settings["max_tokens"] * 0.01,
        "Llama 2": 0
    }

    cost = estimated_cost[st.session_state.app_settings['model']]
    if cost > 0:
        st.metric("Est. Cost per Response", f"${cost:.4f}")
    else:
        st.metric("Est. Cost per Response", "Free")

# Debug panel (conditional)
if st.session_state.app_settings["show_debug"]:
    st.write("---")
    st.subheader("🐛 Debug Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Session State Keys:**")
        st.code(list(st.session_state.keys()))

    with col2:
        st.write("**App Settings JSON:**")
        st.json(st.session_state.app_settings)

# Teaching notes
with st.expander("🎓 Teaching Notes"):
    st.write("""
    **Sidebar Best Practices:**

    1. **Use for Configuration:** Settings, preferences, API keys
    2. **Keep it Organized:** Group related controls, use dividers
    3. **Provide Help Text:** Use the `help` parameter for complex options
    4. **Save State:** Store sidebar values in session_state
    5. **Visual Feedback:** Show impact of settings in main area

    **Key Patterns:**

    ```python
    # Sidebar creation
    with st.sidebar:
        setting = st.selectbox("Option", choices)

    # Direct sidebar calls
    st.sidebar.selectbox("Option", choices)

    # Responsive layout
    col1, col2 = st.columns([2, 1])  # Main content wider
    ```

    **When to Use Sidebar:**
    - App configuration and settings
    - Model parameters (temperature, tokens, etc.)
    - User authentication
    - Navigation (in multi-page apps)
    - Secondary actions that don't fit main flow
    """)
