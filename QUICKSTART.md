# 🚀 Quick Start Guide

## Get Your Chatbot Running in 3 Steps!

### Step 1: Get Your Venice AI API Key

1. Go to https://venice.ai
2. Sign up or log in
3. Navigate to API settings
4. Copy your bearer token (API key)

### Step 2: Set Up the Bot

**On Windows:**
```bash
# Double-click start.bat
# Or run in command prompt:
start.bat
```

**On Mac/Linux:**
```bash
# In terminal:
chmod +x start.sh
./start.sh
```

The script will:
- Create a `.env` file if it doesn't exist
- Ask you to add your API key
- Install all required packages
- Start the server

### Step 3: Add Your API Key

1. Open the `.env` file in a text editor
2. Replace `your_bearer_token_here` with your actual API key:
   ```
   VENICE_API_KEY=your_actual_key_here
   ```
3. Save the file
4. Run the start script again

### Step 4: Use the Bot!

1. Open your browser to: http://localhost:5000
2. Start chatting!
3. Select a character (optional)
4. Request images by describing what you want

## Example Conversations

**Basic Chat:**
```
You: Hey there, tell me about yourself
Bot: [Responds in character with foot fetish theme]
```

**Image Generation:**
```
You: Show me a beautiful woman in stockings
[Then click "Generate Image" button or use the sidebar]
```

**With Character:**
```
1. Select a character from dropdown
2. You: Let's roleplay
3. Bot: [Responds as that character]
```

## Troubleshooting

**"Venice AI client not initialized"**
- Make sure you added your API key to `.env`
- Restart the server after adding the key

**Port already in use**
- Another program is using port 5000
- Edit `app.py` and change the port number

**Images not generating**
- Check you have credits in Venice AI account
- Verify lustify-sdxl model is available

## Need Help?

Check the full README.md for detailed documentation!