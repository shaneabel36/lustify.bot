"""
Lustify Bot - NSFW Roleplay Chatbot with Image Generation

This is the main Flask application that provides a web interface for:
- NSFW roleplay conversations
- Character selection from Venice AI
- Image generation with lustify-sdxl model
- Conversation history management
"""

from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import secrets
import random

# Import our custom modules
from src.venice_client import VeniceClient
from src.conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# Initialize Venice AI client
VENICE_API_KEY = os.getenv('VENICE_API_KEY')
if not VENICE_API_KEY:
    print("WARNING: VENICE_API_KEY not found in environment variables!")
    print("Please create a .env file with your API key")

venice_client = VeniceClient(VENICE_API_KEY) if VENICE_API_KEY else None

# Store conversations in memory (in production, use a database)
conversations = {}


def get_conversation(session_id: str) -> ConversationManager:
    """
    Get or create a conversation for a session
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        ConversationManager instance
    """
    if session_id not in conversations:
        # Create new conversation with foot fetish roleplay system prompt
        system_prompt = """You are a flirty, playful AI companion specializing in foot fetish roleplay. 
You are open, uninhibited, and enjoy detailed, sensual descriptions. 
You love discussing and describing feet, stockings, and related topics in an engaging, immersive way.
Be creative, descriptive, and responsive to the user's desires and requests.
When the user asks for images, acknowledge their request and describe what you'd like to show them."""
        
        conversations[session_id] = ConversationManager(system_prompt)
    
    return conversations[session_id]


@app.route('/')
def index():
    """
    Main page - displays the chat interface
    """
    # Create session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    return render_template('index.html')


@app.route('/characters', methods=['GET'])
def get_characters():
    """
    API endpoint to fetch available characters
    
    Returns:
        JSON list of adult/mature characters
    """
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    characters = venice_client.get_characters(adult_only=True)
    return jsonify({"characters": characters})


@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint for sending chat messages
    
    Expects JSON:
        {
            "message": "user message",
            "character_slug": "optional-character-slug"
        }
    
    Returns:
        JSON with AI response
    """
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    data = request.json
    user_message = data.get('message', '')
    character_slug = data.get('character_slug')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get conversation for this session
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    # Update character if provided
    if character_slug:
        conversation.set_character(character_slug)
    
    # Add user message to conversation
    conversation.add_user_message(user_message)
    
    # Get AI response
    response = venice_client.chat(
        messages=conversation.get_messages(),
        character_slug=conversation.character_slug,
        temperature=0.9,  # High creativity for roleplay
        max_tokens=500
    )
    
    # Add assistant response to conversation
    conversation.add_assistant_message(response)
    
    return jsonify({
        "response": response,
        "message_count": conversation.get_message_count()
    })


@app.route('/generate-image', methods=['POST'])
def generate_image():
    """
    API endpoint for generating images
    
    Expects JSON:
        {
            "prompt": "image description",
            "use_context": true/false (whether to use conversation context)
        }
    
    Returns:
        JSON with base64 encoded image
    """
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    data = request.json
    user_prompt = data.get('prompt', '')
    use_context = data.get('use_context', True)
    
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Get conversation for this session
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    # Enhance prompt with conversation context if requested
    if use_context and conversation.get_message_count() > 0:
        context = conversation.get_context_summary()
        enhanced_prompt = f"{user_prompt}. Context: {context}"
    else:
        enhanced_prompt = user_prompt
    
    # Generate or reuse seed for consistency
    if conversation.current_seed is None:
        conversation.set_seed(random.randint(1, 999999999))
    
    # Generate image
    image_data = venice_client.generate_image(
        prompt=enhanced_prompt,
        seed=conversation.current_seed,
        style_preset="Hyper-Realistic",
        steps=30
    )
    
    if image_data:
        conversation.add_generated_image(image_data)
        return jsonify({
            "image": image_data,
            "seed": conversation.current_seed,
            "prompt": enhanced_prompt
        })
    else:
        return jsonify({"error": "Failed to generate image"}), 500


@app.route('/new-seed', methods=['POST'])
def new_seed():
    """
    API endpoint to generate a new seed for different image variations
    
    Returns:
        JSON with new seed value
    """
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    new_seed_value = random.randint(1, 999999999)
    conversation.set_seed(new_seed_value)
    
    return jsonify({"seed": new_seed_value})


@app.route('/clear', methods=['POST'])
def clear_conversation():
    """
    API endpoint to clear conversation history
    
    Returns:
        JSON success message
    """
    session_id = session.get('session_id')
    if session_id in conversations:
        conversations[session_id].clear()
    
    return jsonify({"message": "Conversation cleared"})


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🔥 Lustify Bot Starting...")
    print(f"{'='*60}")
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔑 API Key: {'✓ Configured' if VENICE_API_KEY else '✗ Missing'}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)