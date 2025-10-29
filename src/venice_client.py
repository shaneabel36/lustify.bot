"""
Venice AI Client - Handles all API interactions with Venice AI

This module provides a simple interface to interact with Venice AI's chat and image generation APIs.
"""

import requests
import json
import base64
from typing import List, Dict, Optional


class VeniceClient:
    """
    Client for interacting with Venice AI API
    
    This class handles:
    - Chat completions with character support
    - Image generation with lustify-sdxl model
    - Conversation history management
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Venice AI client
        
        Args:
            api_key: Your Venice AI bearer token
        """
        self.api_key = api_key
        self.base_url = "https://api.venice.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def get_characters(self, adult_only: bool = True) -> List[Dict]:
        """
        Fetch available characters from Venice AI
        
        Args:
            adult_only: If True, only return adult/mature characters
            
        Returns:
            List of character dictionaries with name, slug, description, etc.
        """
        try:
            response = requests.get(
                f"{self.base_url}/characters",
                headers=self.headers
            )
            response.raise_for_status()
            
            characters = response.json().get("data", [])
            
            # Filter for adult characters if requested
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
        """
        Send a chat message and get a response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            character_slug: Optional character to use (e.g., 'character-name')
            temperature: Creativity level (0.0-2.0, higher = more creative)
            max_tokens: Maximum length of response
            
        Returns:
            The assistant's response text
        """
        try:
            payload = {
                "model": "llama-3.3-70b",  # Good uncensored model for NSFW
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            # Add character if specified
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
        style_preset: str = "Hyper-Realistic",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30
    ) -> Optional[str]:
        """
        Generate an image using Venice AI's lustify-sdxl model
        
        Args:
            prompt: Description of the image to generate
            seed: Random seed for reproducibility (same seed = similar images)
            style_preset: Style to apply (default: Hyper-Realistic)
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            steps: Number of inference steps (default: 30, max: 50)
            
        Returns:
            Base64 encoded image data, or None if error
        """
        try:
            # Enhance prompt with foot fetish theme and thigh high stockings
            enhanced_prompt = f"{prompt}, 8K ultra high resolution, thigh high stockings, detailed feet, professional photography"
            
            payload = {
                "model": "lustify-sdxl",  # The model you specified
                "prompt": enhanced_prompt,
                "width": width,
                "height": height,
                "steps": min(steps, 50),  # lustify-sdxl has max 50 steps
                "style_preset": style_preset,
                "safe_mode": False,  # Disable safe mode for NSFW content
                "hide_watermark": True,
                "format": "png",
                "variants": 1
            }
            
            # Add seed if provided for consistency
            if seed is not None:
                payload["seed"] = seed
            
            response = requests.post(
                f"{self.base_url}/image/generate",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Return the first image (base64 encoded)
            if result.get("images") and len(result["images"]) > 0:
                return result["images"][0]
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def save_image(self, base64_data: str, filename: str) -> bool:
        """
        Save a base64 encoded image to a file
        
        Args:
            base64_data: Base64 encoded image data
            filename: Path to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove data URL prefix if present
            if "," in base64_data:
                base64_data = base64_data.split(",")[1]
            
            # Decode and save
            image_data = base64.b64decode(base64_data)
            with open(filename, "wb") as f:
                f.write(image_data)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False