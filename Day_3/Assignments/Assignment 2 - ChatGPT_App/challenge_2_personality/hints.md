# Challenge 2: Personality Selector - Progressive Hints

Use these hints if you get stuck, but try to implement as much as possible on your own first!

## Hint 1: Getting Started (5 minutes in)

**If you're not sure where to begin:**

Start by modifying your existing chatbot:
1. Copy your working `app.py` from the main workshop
2. Change the title to "AI Personality Assistant"
3. Add a basic personality selector in the sidebar

**Basic sidebar pattern:**
```python
with st.sidebar:
    personality = st.selectbox(
        "Choose Personality:",
        ["Professional", "Creative", "Technical", "Friendly"]
    )
```

Don't worry about making them different yet - just get the selection working.

---

## Hint 2: Storing Personality in Session State (10 minutes in)

**If your personality selection isn't persisting:**

You need to store the selected personality in session state:

```python
# Initialize
if "current_personality" not in st.session_state:
    st.session_state.current_personality = "Friendly"

# In sidebar
personality = st.selectbox(
    "Choose Personality:",
    ["Professional", "Creative", "Technical", "Friendly"],
    index=["Professional", "Creative", "Technical", "Friendly"].index(st.session_state.current_personality)
)

# Update session state
st.session_state.current_personality = personality
```

---

## Hint 3: Basic System Prompts (15 minutes in)

**If you're not sure how to make personalities different:**

Create different system prompts for each personality:

```python
personality_prompts = {
    "Professional": "You are a professional business assistant. Use formal language and provide structured responses.",
    "Creative": "You are a creative writing helper. Be imaginative, use expressive language and encourage creativity.",
    "Technical": "You are a technical expert. Provide precise, detailed explanations with code examples when relevant.",
    "Friendly": "You are a friendly companion. Be casual, supportive, and conversational."
}

# Use the appropriate prompt
system_prompt = personality_prompts[st.session_state.current_personality]
```

---

## Hint 4: Implementing System Prompts in API Calls (20 minutes in)

**If you're not sure how to use system prompts with the API:**

Modify your API call to include the system prompt:

```python
# Prepare messages with system prompt
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input}
]

response = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct:free",
    messages=messages,
    stream=True
)
```

For conversation history, add the system prompt first, then the conversation:

```python
messages = [{"role": "system", "content": system_prompt}]
messages.extend(st.session_state.messages)  # Add conversation history
```

---

## Hint 5: Showing Current Personality (25 minutes in)

**If you want to display which personality is active:**

Add visual indicators for the current personality:

```python
# In the main area
st.title(f"🤖 AI Assistant - {st.session_state.current_personality} Mode")

# Or in the sidebar
st.sidebar.info(f"Current: {st.session_state.current_personality}")

# Or when responding
with st.chat_message("assistant"):
    st.caption(f"Responding as: {st.session_state.current_personality}")
    st.markdown(response_text)
```

---

## Hint 6: Handling Personality Changes Mid-Conversation (30 minutes in)

**If you want to allow personality switching during chat:**

Detect when the personality changes and optionally add a message:

```python
# Check if personality changed
if personality != st.session_state.current_personality:
    st.session_state.current_personality = personality

    # Add a system message about the change
    change_message = f"🔄 Switched to {personality} mode"
    st.session_state.messages.append({"role": "system", "content": change_message})

    st.rerun()  # Refresh to show the change
```

Display system messages differently:
```python
for message in st.session_state.messages:
    if message["role"] == "system":
        st.info(message["content"])  # Special styling for system messages
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
```

---

## Hint 7: Advanced Personality Details (35 minutes in)

**If you want to add personality descriptions and examples:**

Create a more detailed personality structure:

```python
PERSONALITIES = {
    "Professional": {
        "description": "Formal, business-focused assistant",
        "emoji": "💼",
        "system_prompt": "You are a professional business assistant...",
        "example": "I recommend a structured approach with clear objectives..."
    },
    "Creative": {
        "description": "Imaginative, expressive creative helper",
        "emoji": "🎨",
        "system_prompt": "You are a creative writing helper...",
        "example": "What an inspiring idea! Let's explore this creatively..."
    }
}

# Use in sidebar
selected = PERSONALITIES[st.session_state.current_personality]
st.sidebar.write(f"{selected['emoji']} {selected['description']}")
```

---

## Hint 8: Custom Personality Feature (40+ minutes in)

**If you have extra time and want to add custom personalities:**

Allow users to define their own personality:

```python
if st.session_state.current_personality == "Custom":
    with st.sidebar.expander("Custom Personality Setup"):
        custom_prompt = st.text_area(
            "Define your custom personality:",
            "You are a helpful assistant with...",
            height=100
        )

        if "custom_prompt" not in st.session_state:
            st.session_state.custom_prompt = custom_prompt

        if st.button("Save Custom Personality"):
            st.session_state.custom_prompt = custom_prompt
```

Use the custom prompt when "Custom" is selected.

---

## Common Issues & Solutions

### "The personalities all sound the same"
- Make your system prompts more specific and detailed
- Include explicit style instructions (formal vs casual, etc.)
- Add specific expertise areas for each personality
- Use stronger language like "You MUST respond in a formal manner"

### "Personality doesn't persist across messages"
- Make sure you're including the system prompt in every API call
- Store the personality in session state correctly
- Include recent conversation history with system prompt

### "Switching personalities breaks the conversation"
- Handle personality changes gracefully
- Consider adding system messages when personalities switch
- Preserve conversation history across personality changes

### "Custom personality doesn't work"
- Validate that the custom prompt is being stored and used
- Provide a default custom prompt template
- Add error handling for empty or invalid custom prompts

---

## Testing Your Implementation

Try these test scenarios:
- **Same Question, Different Personalities**: Ask "How do I learn programming?" to each personality
- **Personality Switching**: Start with Professional, ask a question, switch to Creative, ask follow-up
- **Conversation Flow**: Have a longer conversation and see if personality stays consistent
- **Custom Personality**: Create a specialized personality (e.g., "Pirate Assistant") and test it

Compare the responses - they should feel distinctly different!

---

## Advanced Features to Try

If you finish early:
1. **Personality Avatars**: Add different emojis/icons for each personality
2. **Usage Statistics**: Track which personalities are used most
3. **Personality Presets**: Create quick-switch buttons for common personalities
4. **Mood Indicators**: Show the "mood" or energy level of each personality
5. **Conversation Starters**: Suggest different questions based on the active personality

Remember: This challenge is about understanding how system prompts dramatically change AI behavior. Have fun experimenting!