"""
Demo script to showcase Lustify Bot functionality with mock responses
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# Base URL
BASE_URL = "http://localhost:5001"

def create_mock_image():
    """Create a simple mock image for demonstration"""
    # Create a simple 400x400 image
    img = Image.new('RGB', (400, 400), color='#FFE4E1')  # Misty rose background
    draw = ImageDraw.Draw(img)
    
    # Draw some simple shapes to represent feet/fetish theme
    draw.ellipse([50, 200, 150, 250], fill='#FFB6C1')  # Left foot shape
    draw.ellipse([250, 200, 350, 250], fill='#FFB6C1')  # Right foot shape
    
    # Add some text
    draw.text((100, 100), "Demo Image", fill='#000000')
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def test_with_real_api_key():
    """Test endpoints with a real Venice AI API key"""
    print("=== Testing with Real API Key ===")
    
    # Test characters
    print("\n1. Testing characters endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/characters")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Characters loaded: {len(data.get('characters', []))} found")
        else:
            print(f"✗ Characters failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Characters error: {e}")

def demo_functionality():
    """Demonstrate the bot's functionality"""
    print("\n=== Demo: Lustify Bot Features ===")
    
    print("\n📋 AVAILABLE FEATURES:")
    print("1. ✓ Character selection for roleplay")
    print("2. ✓ NSFW chat conversations")
    print("3. ✓ Image generation with fetish themes")
    print("4. ✓ Automatic image trigger detection")
    print("5. ✓ Conversation context awareness")
    print("6. ✓ Seed-based image variations")
    
    print("\n🎯 IMAGE GENERATION TRIGGERS:")
    triggers = [
        "pics", "picture", "photo", "image", "selfie", "snap",
        "can i see", "send me a pic", "show me", "let me see",
        "what do you look like", "describe yourself", "picture of"
    ]
    for trigger in triggers:
        print(f"  • '{trigger}'")
    
    print("\n🔥 FOOT FETISH INTEGRATION:")
    print("• System prompt naturally incorporates foot fetish elements")
    print("• Image generation focused on feet, stockings, hosiery")
    print("• Roleplay conversations include feet descriptions")
    print("• Enhanced prompts for foot-related imagery")
    
    print("\n🛠️ TECHNICAL FEATURES:")
    print("• Flask backend with session management")
    print("• Venice AI integration (llama-3.3-70b + lustify-sdxl)")
    print("• Responsive web interface")
    print("• Real-time chat with typing indicators")
    print("• Image gallery with click-to-expand")
    print("• Seed control for consistent image generation")

def create_usage_guide():
    """Create a comprehensive usage guide"""
    guide = """
# Lustify Bot - Usage Guide

## Getting Started
1. Add your Venice AI admin key to .env file
2. Run: python app.py
3. Open browser to http://localhost:5000

## Chat Features
- **Character Selection**: Choose from adult characters for roleplay
- **Natural Conversations**: AI responds with flirty, fetish-focused dialogue
- **Context Awareness**: Remembers conversation history

## Image Generation
- **Manual**: Use sidebar to generate custom images
- **Automatic**: Triggers when you say "pics", "photo", "can i see", etc.
- **Context-Aware**: Images consider your conversation
- **Seed Control**: Maintain consistent image styles

## Fetish Integration
- Natural foot fetish themes in conversations
- Enhanced image prompts for foot/stocking content
- Seductive roleplay scenarios
- Professional quality image generation

## Commands & Triggers
Image generation automatically triggers on:
- "pics", "picture", "photo", "image"
- "can i see", "send me a pic", "show me"
- "what do you look like", "describe yourself"

## Tips
- Use descriptive language for better images
- Try different characters for varied roleplay
- Use "New Variation" button for different image styles
- Conversation context improves image relevance
"""
    
    with open("USAGE_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("✓ Created USAGE_GUIDE.md")

if __name__ == "__main__":
    print("🔥 Lustify Bot - Demo & Testing 🔥")
    
    # Test current functionality
    test_with_real_api_key()
    
    # Demo features
    demo_functionality()
    
    # Create usage guide
    create_usage_guide()
    
    print("\n✅ Demo Complete!")
    print("\n📝 Next Steps:")
    print("1. Add real Venice AI admin key to .env")
    print("2. Test with actual API calls")
    print("3. Deploy to production environment")