# ChatGPT-Style Application

This folder contains the main workshop application that participants will build during the 2-hour session.

## Files Structure

- **app.py** - The main application file (complete implementation)
- **requirements.txt** - Python dependencies
- **instructor_script.md** - Step-by-step presentation script
- **deployment_guide.md** - Hugging Face Spaces deployment instructions

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Deployment
Follow the instructions in `deployment_guide.md` to deploy to Hugging Face Spaces.

## API Key Setup

### For Local Development
- Get your OpenRouter API key from [openrouter.ai](https://openrouter.ai)
- Enter it in the sidebar when running the app

### For Production Deployment
- Add your API key to Hugging Face Spaces secrets as `OPENROUTER_API_KEY`
- The app will automatically use it from the secrets

## Features Included

✅ Modern chat interface with Streamlit components
✅ OpenRouter API integration (free Mistral model)
✅ Session state management for chat history
✅ Streaming responses for better UX
✅ Error handling and user feedback
✅ Production-ready deployment configuration

This application serves as the foundation for the breakout session challenges where participants will add translation, personality selection, and export features.