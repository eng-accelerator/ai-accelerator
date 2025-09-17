 !pip install huggingface_hub

from huggingface_hub import whoami
from google.colab import userdata

# Get your Hugging Face token from Colab Secrets
hf_token = userdata.get('HF_TOKEN')

# Verify the token by checking your identity
try:
    user_info = whoami(token=hf_token)
    print(f"Logged in as: {user_info['name']}")
except Exception as e:
    print(f"Could not log in: {e}")
    print("Please make sure you have added your Hugging Face token to Colab Secrets with the name 'HF_TOKEN'")
