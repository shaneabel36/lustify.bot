"""
Lustify Bot - NSFW Roleplay Chatbot with Image Generation
"""

from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import secrets
import random

from src.venice_client import VeniceClient
from src.conversation_manager import ConversationManager

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# Initialize Venice AI client with single API key
VENICE_API_KEY = os.getenv('VENICE_ADMIN_KEY') or os.getenv('VENICE_API_KEY')

if not VENICE_API_KEY:
    print("WARNING: No API key found!")
    print("Set VENICE_ADMIN_KEY or VENICE_API_KEY in .env file")

venice_client = VeniceClient(VENICE_API_KEY) if VENICE_API_KEY else None

conversations = {}


def get_conversation(session_id: str) -> ConversationManager:
    """Get or create a conversation for a session"""
    if session_id not in conversations:
        system_prompt = """You are a flirty, playful AI companion who naturally incorporates foot fetish elements into roleplay.

Your personality:
- Engaging and natural conversationalist who builds genuine connection
- Subtly incorporates mentions of feet, stockings, hosiery, sandals, and lingerie into descriptions
- Describes outfits, poses, and scenes with attention to legs and feet
- Responds enthusiastically when users show interest in feet/stockings/hosiery
- Balances fetish content with overall engaging roleplay - never forced or awkward

When describing yourself or scenes:
- Mention what you're wearing on your feet/legs (stockings, heels, sandals, etc.)
- Describe how you're positioned (crossed legs, dangling shoes, etc.)
- Include sensory details (texture of nylons, arch of feet, painted toes, etc.)
- Keep it natural and woven into the conversation flow"""
        
        conversations[session_id] = ConversationManager(system_prompt)
    
    return conversations[session_id]


@app.route('/')
def index():
    """Main page"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    return render_template('index.html')


@app.route('/characters', methods=['GET'])
def get_characters():
    """API endpoint to fetch available characters"""
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    characters = venice_client.get_characters(adult_only=True)
    return jsonify({"characters": characters})


@app.route('/chat', methods=['POST'])
def chat():
    """API endpoint for sending chat messages"""
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    data = request.json
    user_message = data.get('message', '')
    character_slug = data.get('character_slug')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    if character_slug:
        conversation.set_character(character_slug)
    
    conversation.add_user_message(user_message)
    
    response = venice_client.chat(
        messages=conversation.get_messages(),
        character_slug=conversation.character_slug,
        temperature=0.9,
        max_tokens=500
    )
    
    conversation.add_assistant_message(response)
    
    return jsonify({
        "response": response,
        "message_count": conversation.get_message_count()
    })


@app.route('/generate-image', methods=['POST'])
def generate_image():
    """API endpoint for generating images"""
    if not venice_client:
        return jsonify({"error": "Venice AI client not initialized"}), 500
    
    data = request.json
    user_prompt = data.get('prompt', '')
    use_context = data.get('use_context', True)
       
    
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    if use_context and conversation.get_message_count() > 0:
        context = conversation.get_context_summary()
        enhanced_prompt = f"{user_prompt}. Context: {context}"
    else:
        enhanced_prompt = user_prompt
    
    if conversation.current_seed is None:
        conversation.set_seed(random.randint(1, 999999999))
    
    image_data = venice_client.generate_image(
        prompt=enhanced_prompt,
        seed=conversation.current_seed,
        style_preset="Hyperrealism",
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
    """API endpoint to generate a new seed"""
    session_id = session.get('session_id')
    conversation = get_conversation(session_id)
    
    new_seed_value = random.randint(1, 999999999)
    conversation.set_seed(new_seed_value)
    
    return jsonify({"seed": new_seed_value})


@app.route('/clear', methods=['POST'])
def clear_conversation():
    """API endpoint to clear conversation history"""
    session_id = session.get('session_id')
    if session_id in conversations:
        conversations[session_id].clear()
    
    return jsonify({"message": "Conversation cleared"})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🔥 Lustify Bot Starting...")
    print(f"{'='*60}")
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔑 API Key: {'✓ Configured' if VENICE_API_KEY else '✗ Missing'}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)