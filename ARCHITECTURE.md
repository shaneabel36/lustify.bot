# 🏗️ Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              index.html (UI)                         │   │
│  │  - Chat interface                                    │   │
│  │  - Character selector                                │   │
│  │  - Image generation controls                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           script.js (Frontend Logic)                 │   │
│  │  - Captures user input                               │   │
│  │  - Sends API requests                                │   │
│  │  - Displays responses                                │   │
│  │  - Handles image display                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                    FLASK SERVER (Backend)                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              app.py (Main Server)                    │   │
│  │  - Routes HTTP requests                              │   │
│  │  - Manages sessions                                  │   │
│  │  - Coordinates components                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      conversation_manager.py (State)                 │   │
│  │  - Stores message history                            │   │
│  │  - Tracks current character                          │   │
│  │  - Manages image seeds                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        venice_client.py (API Client)                 │   │
│  │  - Sends chat requests                               │   │
│  │  - Generates images                                  │   │
│  │  - Fetches characters                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↕ HTTPS/JSON
┌─────────────────────────────────────────────────────────────┐
│                      VENICE AI API                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         /chat/completions                            │   │
│  │  - Processes chat messages                           │   │
│  │  - Returns AI responses                              │   │
│  │  - Supports character personalities                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         /image/generate                              │   │
│  │  - Generates images with lustify-sdxl                │   │
│  │  - Returns base64 encoded images                     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         /characters                                  │   │
│  │  - Lists available characters                        │   │
│  │  - Filters adult/mature characters                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### Chat Message Flow

```
1. User types: "Tell me about your feet"
   ↓
2. script.js captures input
   ↓
3. POST /api/chat with message
   ↓
4. app.py receives request
   ↓
5. conversation_manager adds to history
   ↓
6. venice_client.chat() sends to Venice AI
   ↓
7. Venice AI processes with character context
   ↓
8. Returns: "My feet are soft and delicate..."
   ↓
9. conversation_manager stores response
   ↓
10. app.py sends JSON back to browser
    ↓
11. script.js displays in chat
```

### Image Generation Flow

```
1. User enters: "Woman in thigh high stockings"
   ↓
2. script.js sends to /api/generate-image
   ↓
3. app.py receives prompt
   ↓
4. conversation_manager provides context
   ↓
5. venice_client enhances prompt:
   "Woman in thigh high stockings, 8K ultra high resolution,
    thigh high stockings, detailed feet, professional photography"
   ↓
6. Sends to Venice AI with:
   - model: lustify-sdxl
   - seed: 123456 (for consistency)
   - style: Hyper-Realistic
   ↓
7. Venice AI generates image
   ↓
8. Returns base64 encoded PNG
   ↓
9. conversation_manager stores image
   ↓
10. app.py sends image data to browser
    ↓
11. script.js displays image in chat
```

## Key Technologies

### Backend
- **Flask**: Python web framework
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: No frameworks, pure JS

### API
- **Venice AI**: Uncensored AI chat and image generation
- **REST API**: JSON over HTTPS

## File Structure

```
lustify.bot/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .env                       # Your API key (not in git)
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick setup guide
├── ARCHITECTURE.md            # This file
├── start.sh                   # Linux/Mac startup
├── start.bat                  # Windows startup
├── src/
│   ├── venice_client.py       # Venice AI API wrapper
│   └── conversation_manager.py # State management
├── templates/
│   └── index.html             # Main web page
└── static/
    ├── style.css              # Styling
    └── script.js              # Frontend logic
```

## Security Considerations

1. **API Key Storage**: Stored in `.env`, never committed to git
2. **Session Management**: Flask sessions with secret key
3. **HTTPS**: Venice AI uses HTTPS for all requests
4. **Input Validation**: Basic validation on both frontend and backend

## Scalability Notes

Current implementation:
- ✅ Single user or small group
- ✅ Conversation stored in memory
- ✅ No database required
- ❌ Not suitable for production with many users

For production:
- Add database (PostgreSQL, MongoDB)
- Implement user authentication
- Add rate limiting
- Use Redis for session storage
- Deploy with Gunicorn + Nginx

## Extension Points

Easy to add:
1. **Text-to-Speech**: gtts library already included
2. **Image Upload**: Add file upload endpoint
3. **Save Conversations**: Add database integration
4. **Multiple Chats**: Add conversation switching
5. **Custom Characters**: Create character management UI