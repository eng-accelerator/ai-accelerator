# Open router API key for using a free model , paid models
# How can we mimic the streaming behavior of ChatGPT in Streamlit?
# How can we have all the session_state stored for our conversation. 


import streamlit as st
from openai import OpenAI

# Configure the page
st.set_page_config(page_title="My ChatBot", page_icon="🤖")

# Initialize the OpenAI client with OpenRouter
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")

if not api_key:
    st.warning("Please enter your OpenRouter API key to continue.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "http://localhost:8501",  # Optional: shows on OpenRouter rankings
        "X-Title": "My ChatBot",                  # Optional: shows on OpenRouter rankings
    }
)

# App title
st.title("🤖 My ChatBot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)



# Training models on your inputs or prompts - Open router consent or privacy page
# Retention - How much time you'd want to store your input prompts to these models.

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct:free",  # safer free model
                messages=st.session_state.messages,
                stream=True,
                extra_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "My ChatBot"
                },
                extra_body={
                    "provider": {
                        "data_collection": "deny"  # or "allow" if you permit retention
                    }
                }
            )
# Hello how can I help you today ? 
# Hello how can I help you today ?


            # Stream the response
            response_text = ""
            response_placeholder = st.empty()

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    # Clean up unwanted tokens
                    content = chunk.choices[0].delta.content
                    content = (
                        content.replace('<s>', '')
                        .replace('<|im_start|>', '')
                        .replace('<|im_end|>', '')
                        .replace("<|OUT|>", "")
                    )
                    response_text += content
                    response_placeholder.markdown(response_text + "▌")

            # Final cleanup of response text
            response_text = (
                response_text.replace('<s>', '')
                .replace('<|im_start|>', '')
                .replace('<|im_end|>', '')
                .replace("<|OUT|>", "")
                .strip()
            )
            response_placeholder.markdown(response_text)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please check your API key and try again.")
