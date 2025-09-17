# Deployment Guide: Hugging Face Spaces

This guide walks you through deploying your ChatGPT-style application to Hugging Face Spaces for free hosting.

## Prerequisites

- Completed chatbot application (app.py and requirements.txt)
- OpenRouter API key
- Hugging Face account (free at huggingface.co)

## Step-by-Step Deployment

### 1. Create a Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure your Space:
   - **Space name**: Choose a unique name (e.g., "my-awesome-chatbot")
   - **License**: Apache 2.0 (recommended)
   - **SDK**: Select **"Streamlit"**
   - **Visibility**: Public (so others can use your chatbot)
   - **Hardware**: CPU basic (free tier)

4. Click **"Create Space"**

### 2. Upload Your Application Files

You'll now see a Git-style interface. Upload these files:

**Upload app.py:**
- Click "Add file" → "Upload file"
- Select your `app.py` file
- Commit message: "Add main application file"
- Click "Commit changes to main"

**Upload requirements.txt:**
- Click "Add file" → "Upload file"
- Select your `requirements.txt` file
- Commit message: "Add requirements file"
- Click "Commit changes to main"

### 3. Configure API Key Security

**IMPORTANT**: Never put your API key directly in your code when deploying to public repositories.

1. In your Space, click **"Settings"** tab
2. Scroll to **"Repository secrets"**
3. Click **"Add a new secret"**
4. Configure:
   - **Name**: `OPENROUTER_API_KEY`
   - **Value**: Your OpenRouter API key (paste it exactly)
5. Click **"Add secret"**

### 4. Update Your Code for Production

Your app.py needs to handle both local development and production. Replace the API key section with:

```python
# Initialize the OpenAI client with OpenRouter
if "OPENROUTER_API_KEY" in st.secrets:
    # Production: Use Hugging Face Spaces secrets
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    # Local development: Use sidebar input
    api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
    if not api_key:
        st.warning("Please enter your OpenRouter API key to continue.")
        st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)
```

### 5. Upload the Updated Code

1. Upload your modified `app.py` file
2. Commit message: "Update for production deployment"
3. Click "Commit changes to main"

### 6. Monitor the Build Process

1. Go to the **"App"** tab to see your Space
2. You'll see a build log showing the deployment progress
3. The build process:
   - Installs Python dependencies
   - Starts the Streamlit server
   - Makes your app available at the Space URL

**Build time**: Usually 2-3 minutes for the initial deployment

### 7. Test Your Deployed Application

Once the build completes:

1. Your chatbot will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Test the functionality:
   - Send a few messages
   - Verify streaming responses work
   - Check that conversation history persists
   - Ensure no API key errors

### 8. Share Your Chatbot

Your chatbot is now publicly accessible! Share the URL with:
- Colleagues and friends
- Social media
- Your portfolio or resume
- Workshop participants

## Troubleshooting Common Issues

### Build Fails - Dependencies
**Problem**: Build fails with package installation errors
**Solution**: Check your `requirements.txt` format:
```
streamlit
openai
```
(No version numbers needed for basic deployment)

### API Key Not Found
**Problem**: "API key not found" error in production
**Solution**:
1. Verify the secret name is exactly `OPENROUTER_API_KEY`
2. Check that you added it in Settings → Repository secrets
3. Restart the Space (Settings → Factory reboot)

### App Won't Start
**Problem**: Space shows "Building" forever or crashes
**Solutions**:
1. Check the build logs in the App tab
2. Ensure your `app.py` file is valid Python code
3. Verify all imports are in `requirements.txt`

### Slow Performance
**Problem**: App is slow or times out
**Solutions**:
1. Free tier has limitations - consider Hugging Face Pro
2. Optimize your code to reduce API calls
3. Add error handling for timeouts

### Streamlit Errors
**Problem**: Streamlit-specific errors in production
**Solution**: Add this at the top of your `app.py`:
```python
import streamlit as st

# Configure the page (must be first Streamlit command)
st.set_page_config(page_title="My ChatBot", page_icon="🤖")
```

## Advanced Configuration

### Custom Domain (Pro Feature)
Hugging Face Pro users can configure custom domains for their Spaces.

### Hardware Upgrades
For high-traffic applications:
1. Go to Settings → Hardware
2. Upgrade to CPU or GPU instances
3. Note: This requires Hugging Face Pro subscription

### Environment Variables
For additional configuration:
1. Settings → Repository secrets
2. Add other environment variables as needed
3. Access in code with `st.secrets["VARIABLE_NAME"]`

## Updating Your Deployed App

To update your deployed application:

1. Modify your local files
2. Upload the updated files to your Space
3. The Space will automatically rebuild and redeploy
4. Changes are live within 2-3 minutes

## Space Management

### Monitoring Usage
- View usage statistics in your Space settings
- Monitor API costs through OpenRouter dashboard
- Set up alerts for high usage

### Backup and Version Control
- Hugging Face Spaces uses Git under the hood
- All changes are versioned automatically
- You can roll back to previous versions if needed

### Collaboration
- Add collaborators in Settings → Collaboration
- Multiple team members can edit the Space
- Perfect for team projects and workshops

## Cost Considerations

### Hugging Face Spaces
- **Free tier**: Sufficient for personal projects and demos
- **Pro tier** ($9/month): Better performance, custom domains, priority support

### OpenRouter API
- **Mistral 7B**: Completely free
- **Monitor usage**: Check OpenRouter dashboard regularly
- **Rate limits**: Free models have reasonable rate limits for demos

## Next Steps

Once your chatbot is deployed:

1. **Enhance the UI**: Add custom CSS, logos, and branding
2. **Add Features**: Implement the breakout session challenges
3. **Monitor Performance**: Watch usage and optimize as needed
4. **Share and Iterate**: Get user feedback and improve

Your chatbot is now live on the internet! This is a significant achievement that demonstrates your ability to build, deploy, and maintain modern AI applications.

## Support Resources

- **Hugging Face Documentation**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **OpenRouter Documentation**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **Workshop Materials**: All code examples and solutions included in your workshop folder