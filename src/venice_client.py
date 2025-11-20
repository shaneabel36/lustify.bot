"""
Venice AI Client - Handles all API interactions with Venice AI
"""

import requests
import json
import base64
from typing import List, Dict, Optional


class VeniceClient:
    """Client for interacting with Venice AI API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the Venice AI client
        
        Args:
            api_key: Your Venice AI API key (use ADMIN key for everything)
        """
        self.api_key = api_key
        self.base_url = "https://api.venice.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def get_characters(self, adult_only: bool = True) -> List[Dict]:
        """Fetch available characters from Venice AI"""
        try:
            response = requests.get(
                f"{self.base_url}/characters",
                headers=self.headers
            )
            response.raise_for_status()
            
            characters = response.json().get("data", [])
            
            if adult_only:
                characters = [c for c in characters if c.get("adult", False)]
                
            return characters
        except Exception as e:
            print(f"Error fetching characters: {e}")
            return []
    
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        character_slug: Optional[str] = None,
        temperature: float = 0.9,
        max_tokens: int = 500
    ) -> str:
        """Send a chat message and get a response"""
        try:
            payload = {
                "model": "llama-3.3-70b",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            if character_slug:
                payload["venice_parameters"] = {
                    "character_slug": character_slug
                }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_image(
        self,
        prompt: str,
        seed: Optional[int] = None,
        style_preset: str = "Hyperrealism",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30
    ) -> Optional[str]:
        """Generate an image using Venice AI's lustify-sdxl model"""
        try:
            enhanced_prompt = f"{prompt}, 8K ultra high resolution, beautiful feet, stockings, detailed, professional photography, hyper-realistic"
            
            payload = {
                "model": "lustify-sdxl",
                "prompt": enhanced_prompt,
                "width": width,
                "height": height,
                "steps": min(steps, 50),
                "style_preset": style_preset,
                "safe_mode": False,
                "hide_watermark": True,
                "format": "png",
                "variants": 1,
                "cfg_scale": 7,
                "negative_prompt": "bad feet, ugly feet, bad anatomy, too many toes, blurry, cartoon, fake, vague"
            }
            
            if seed is not None:
                payload["seed"] = seed
            
            response = requests.post(
                f"{self.base_url}/image/generate",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("images") and len(result["images"]) > 0:
                return result["images"][0]
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def save_image(self, base64_data: str, filename: str) -> bool:
        """Save a base64 encoded image to a file"""
        try:
            if "," in base64_data:
                base64_data = base64_data.split(",")[1]
            
            image_data = base64.b64decode(base64_data)
            with open(filename, "wb") as f:
                f.write(image_data)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False