# 🔥 Lustify Bot - NSFW Roleplay Chatbot

A web-based NSFW roleplay chatbot with AI image generation capabilities, powered by Venice AI.

## Features

- 💬 **NSFW Roleplay Chat**: Engage in adult conversations with foot fetish theme
- 🎭 **Character Selection**: Choose from Venice AI's adult/mature characters
- 🖼️ **Image Generation**: Generate hyper-realistic images using lustify-sdxl model
- 🎨 **Consistent Style**: Uses seed values to maintain character consistency
- 📝 **Context-Aware**: Remembers conversation history for better responses
- 🌐 **Web Interface**: Easy-to-use browser-based interface

## What Each Component Does

### Backend (Python)

1. **app.py** - Main Flask application
   - Handles web server and routing
   - Manages user sessions
   - Coordinates between frontend and Venice AI

2. **src/venice_client.py** - Venice AI API wrapper
   - Sends chat messages to Venice AI
   - Generates images with lustify-sdxl model
   - Fetches available characters
   - Handles API authentication

3. **src/conversation_manager.py** - Conversation state management
   - Stores message history
   - Tracks current character
   - Manages image generation seeds
   - Provides conversation context

### Frontend (HTML/CSS/JavaScript)

1. **templates/index.html** - Main web page structure
   - Chat interface layout
   - Character selection dropdown
   - Image generation controls

2. **static/style.css** - Visual styling
   - Modern gradient design
   - Responsive layout
   - Message bubbles and animations

3. **static/script.js** - Interactive functionality
   - Sends messages to backend
   - Displays responses
   - Handles image generation
   - Updates UI dynamically

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Venice AI API key (bearer token)
- Internet connection

### Step 1: Install Dependencies

```bash
cd lustify.bot
pip install -r requirements.txt
```

This installs:
- **Flask**: Web framework for the server
- **requests**: For making API calls to Venice AI
- **python-dotenv**: For managing environment variables
- **gtts**: Text-to-speech (optional)
- **pillow**: Image handling

### Step 2: Configure API Key

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Venice AI bearer token:
```
VENICE_API_KEY=your_bearer_token_here
```

### Step 3: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## How to Use

### Basic Chat

1. Type your message in the text box at the bottom
2. Press Enter or click "Send"
3. The AI will respond based on the conversation context

### Character Selection

1. Click the dropdown in the sidebar
2. Select an adult/mature character
3. The AI will adopt that character's personality

### Image Generation

**Method 1: Using the sidebar**
1. Type an image description in the "Image Generation" box
2. Click "Generate Image"
3. The image will appear in the chat

**Method 2: During conversation**
1. Ask the AI to generate an image in your message
2. Use the sidebar to generate based on the conversation

### Image Variations

- Images use a "seed" value for consistency
- Same seed = similar style/character
- Click "New Variation" to get a different seed
- This creates variations while maintaining quality

### Clear Chat

Click "Clear Chat" to start a new conversation and reset history.

## Understanding the Code

### How Messages Flow

```
User types message
    ↓
JavaScript (script.js) captures it
    ↓
Sends to Flask backend (app.py)
    ↓
Backend adds to conversation history
    ↓
Sends to Venice AI API (venice_client.py)
    ↓
Venice AI responds
    ↓
Backend stores response
    ↓
Sends back to frontend
    ↓
JavaScript displays in chat
```

### How Image Generation Works

```
User requests image
    ↓
Frontend sends prompt to backend
    ↓
Backend enhances prompt with:
  - Conversation context
  - "8K ultra high resolution"
  - "thigh high stockings"
  - "detailed feet"
    ↓
Sends to Venice AI image API
    ↓
Venice generates with lustify-sdxl model
    ↓
Returns base64 encoded image
    ↓
Frontend displays image in chat
```

### Key Concepts

**Sessions**: Each browser tab gets a unique session ID to keep conversations separate

**Conversation History**: All messages are stored in memory (cleared when server restarts)

**Seeds**: Random numbers that control image generation style. Same seed = similar results

**Character Slugs**: Unique identifiers for Venice AI characters (e.g., "character-name")

**Base64 Encoding**: Images are sent as text strings that browsers can display

## Customization

### Change System Prompt

Edit `app.py`, line 42-47 to modify the AI's personality:

```python
system_prompt = """Your custom instructions here"""
```

### Adjust Image Settings

Edit `src/venice_client.py`, line 120-130 to change:
- Image size (width/height)
- Number of steps (quality)
- Style preset
- Prompt enhancements

### Modify UI Colors

Edit `static/style.css` to change colors, fonts, and layout.

## Troubleshooting

### "Venice AI client not initialized"
- Check that your API key is set in `.env`
- Verify the key is correct

### Images not generating
- Ensure you have credits in your Venice AI account
- Check that lustify-sdxl model is available
- Try reducing image size or steps

### Characters not loading
- Verify API key has access to characters endpoint
- Check internet connection
- Look for errors in browser console (F12)

### Chat not responding
- Check browser console for errors
- Verify Flask server is running
- Check API rate limits

## API Endpoints

The application exposes these endpoints:

- `GET /` - Main chat interface
- `GET /api/characters` - List available characters
- `POST /api/chat` - Send chat message
- `POST /api/generate-image` - Generate image
- `POST /api/new-seed` - Get new seed value
- `POST /api/clear` - Clear conversation

## Security Notes

- Never commit your `.env` file with real API keys
- This is for personal use only
- Keep your API key private
- Be aware of Venice AI's usage policies

## Future Enhancements

Potential features to add:
- Text-to-speech for responses
- User image upload and analysis
- Save/load conversations
- Multiple conversation threads
- Custom character creation
- Image editing/inpainting

## Support

For Venice AI API issues, visit: https://docs.venice.ai

For code issues, check the browser console (F12) and server logs.

## License

This is a personal project. Use responsibly and in accordance with Venice AI's terms of service.