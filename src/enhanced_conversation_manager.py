"""
Enhanced Conversation Manager - Handles conversation history and intelligent image generation analysis

This module manages the conversation state, including:
- Message history
- Character selection
- Image generation tracking
- Intelligent context analysis for dynamic image generation
"""

from typing import List, Dict, Optional


class ConversationManager:
    """
    Manages conversation state and history
    
    This class keeps track of:
    - All messages in the conversation
    - Current character being used
    - Generated images
    - Seed values for image consistency
    - Intelligent context analysis for better image generation
    """

    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize a new conversation
        
        Args:
            system_prompt: Optional system prompt to set the AI's behavior
        """
        self.messages: List[Dict[str, str]] = []
        self.character_slug: Optional[str] = None
        self.current_seed: Optional[int] = None
        self.generated_images: List[str] = []
        
        # Add system prompt if provided
        if system_prompt:
            self.add_system_message(system_prompt)

    def add_system_message(self, content: str):
        """
        Add a system message (sets AI behavior/personality)
        
        Args:
            content: The system message content
        """
        self.messages.append({
            "role": "system",
            "content": content
        })

    def add_user_message(self, content: str):
        """
        Add a user message to the conversation
        
        Args:
            content: The user's message
        """
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, content: str):
        """
        Add an assistant (AI) message to the conversation
        
        Args:
            content: The AI's response
        """
        self.messages.append({
            "role": "assistant",
            "content": content
        })

    def set_character(self, character_slug: str):
        """
        Set the character for this conversation
        
        Args:
            character_slug: The character's slug (e.g., 'character-name')
        """
        self.character_slug = character_slug

    def set_seed(self, seed: int):
        """
        Set the seed for image generation consistency
        
        Args:
            seed: Random seed value
        """
        self.current_seed = seed

    def add_generated_image(self, image_data: str):
        """
        Track a generated image
        
        Args:
            image_data: Base64 encoded image data
        """
        self.generated_images.append(image_data)

    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get all messages in the conversation
        
        Returns:
            List of message dictionaries
        """
        return self.messages

    def get_context_summary(self) -> str:
        """
        Get a summary of the conversation for image generation prompts
        
        Returns:
            A summary of recent conversation context
        """
        # Get last few messages for context
        recent_messages = self.messages[-5:] if len(self.messages) > 5 else self.messages
        
        context_parts = []
        for msg in recent_messages:
            if msg["role"] in ["user", "assistant"]:
                context_parts.append(msg["content"][:100])  # First 100 chars
        
        return " ".join(context_parts)

    def analyze_image_request(self, user_message: str, ai_response: str) -> dict:
        """
        Analyze the conversation to determine what kind of image should be generated
        
        Args:
            user_message: The user's most recent message
            ai_response: The AI's most recent response
            
        Returns:
            Dictionary with image request analysis including prompt, style, and context
        """
        analysis = {
            "request_type": "general",
            "specific_elements": [],
            "mood": "seductive",
            "focal_point": "feet",
            "clothing": ["stockings", "high heels"],
            "setting": "intimate",
            "context_keywords": [],
            "dynamic_prompt": ""
        }
        
        # Combine both messages for analysis
        combined_text = f"{user_message} {ai_response}".lower()
        
        # Analyze specific requests
        if any(word in combined_text for word in ["what do you look like", "describe yourself", "how do you look"]):
            analysis["request_type"] = "self_appearance"
            analysis["specific_elements"] = ["full_body", "face", "outfit", "posing"]
            
        elif any(word in combined_text for word in ["feet", "toes", "foot"]):
            analysis["request_type"] = "feet_focus"
            analysis["specific_elements"] = ["feet", "toes", "arches", "painted_nails"]
            
        elif any(word in combined_text for word in ["legs", "thighs", "calves"]):
            analysis["request_type"] = "legs_focus"
            analysis["specific_elements"] = ["legs", "thighs", "calves", "tone"]
            
        elif any(word in combined_text for word in ["stocking", "hosiery", "nylon"]):
            analysis["request_type"] = "hosiery_focus"
            analysis["specific_elements"] = ["stockings", "hosiery", "nylons", "sheer_fabric"]
            
        elif any(word in combined_text for word in ["shoes", "heels", "boots", "sandals"]):
            analysis["request_type"] = "footwear_focus"
            analysis["specific_elements"].append("footwear")
            
        # Analyze mood/tone
        if any(word in combined_text for word in ["playful", "cute", "fun", "giggly"]):
            analysis["mood"] = "playful"
        elif any(word in combined_text for word in ["dominant", "strict", "authoritative", "boss"]):
            analysis["mood"] = "dominant"
        elif any(word in combined_text for word in ["shy", "nervous", "blushing", "timid"]):
            analysis["mood"] = "shy"
        elif any(word in combined_text for word in ["professional", "elegant", "sophisticated", "classy"]):
            analysis["mood"] = "elegant"
        elif any(word in combined_text for word in ["bored", "tired", "casual", "relaxed"]):
            analysis["mood"] = "casual"
            
        # Analyze setting preferences
        if any(word in combined_text for word in ["bedroom", "bed", "night", "sleeping"]):
            analysis["setting"] = "bedroom"
        elif any(word in combined_text for word in ["office", "desk", "work", "business"]):
            analysis["setting"] = "office"
        elif any(word in combined_text for word in ["outdoor", "park", "garden", "nature"]):
            analysis["setting"] = "outdoor"
        elif any(word in combined_text for word in ["beach", "sand", "water", "ocean"]):
            analysis["setting"] = "beach"
        elif any(word in combined_text for word in ["party", "club", "dance", "nightclub"]):
            analysis["setting"] = "party"
            
        # Extract context keywords and colors
        keywords = []
        colors = []
        materials = []
        
        # Colors
        color_map = {
            "red": "red", "pink": "pink", "blue": "blue", "green": "green",
            "black": "black", "white": "white", "purple": "purple", "gold": "gold",
            "silver": "silver", "brown": "brown", "beige": "beige", "cream": "cream"
        }
        
        for color in color_map:
            if color in combined_text:
                colors.append(color_map[color])
                
        # Materials
        material_map = {
            "silk": "silk", "lace": "lace", "leather": "leather", "satin": "satin",
            "cotton": "cotton", "denim": "denim", "latex": "latex", "pvc": "pvc"
        }
        
        for material in material_map:
            if material in combined_text:
                materials.append(material_map[material])
        
        # Specific fetish elements
        if "dangling" in combined_text or "dangle" in combined_text:
            keywords.append("dangling_shoes")
        if "crossed" in combined_text and "leg" in combined_text:
            keywords.append("crossed_legs")
        if "pedicure" in combined_text or "painted" in combined_text:
            keywords.append("pedicured_feet")
        if "wrinkled" in combined_text or "soles" in combined_text:
            keywords.append("wrinkled_soles")
            
        analysis["context_keywords"] = keywords + colors + materials
        
        # Generate dynamic prompt based on analysis
        analysis["dynamic_prompt"] = self._generate_dynamic_prompt(analysis)
        
        return analysis

    def _generate_dynamic_prompt(self, analysis: dict) -> str:
        """
        Generate a dynamic prompt based on the analysis
        
        Args:
            analysis: The analysis dictionary
            
        Returns:
            A contextually appropriate image generation prompt
        """
        prompt_parts = []
        
        # Base subject
        if analysis["request_type"] == "self_appearance":
            prompt_parts.append("Beautiful woman showing full body")
        elif analysis["request_type"] == "feet_focus":
            prompt_parts.append("Close-up of woman's feet")
        elif analysis["request_type"] == "legs_focus":
            prompt_parts.append("Woman showing her legs")
        elif analysis["request_type"] == "hosiery_focus":
            prompt_parts.append("Woman wearing stockings and hosiery")
        else:
            prompt_parts.append("Seductive woman")
            
        # Add specific elements
        if analysis["specific_elements"]:
            elements_text = ", ".join(analysis["specific_elements"])
            prompt_parts.append(elements_text)
            
        # Add clothing
        if analysis["clothing"]:
            clothing_text = ", ".join(analysis["clothing"])
            prompt_parts.append(f"wearing {clothing_text}")
            
        # Add mood descriptors
        mood_descriptors = {
            "seductive": "seductive pose, alluring expression",
            "playful": "playful expression, fun pose",
            "dominant": "dominant pose, confident expression",
            "shy": "shy expression, timid pose",
            "elegant": "elegant pose, sophisticated expression",
            "casual": "relaxed pose, natural expression"
        }
        
        if analysis["mood"] in mood_descriptors:
            prompt_parts.append(mood_descriptors[analysis["mood"]])
            
        # Add setting
        setting_descriptors = {
            "intimate": "intimate setting",
            "bedroom": "in bedroom, soft lighting",
            "office": "in office setting",
            "outdoor": "outdoor setting",
            "beach": "at the beach",
            "party": "at a party"
        }
        
        if analysis["setting"] in setting_descriptors:
            prompt_parts.append(setting_descriptors[analysis["setting"]])
            
        # Add context keywords
        if analysis["context_keywords"]:
            keywords_text = ", ".join(analysis["context_keywords"])
            prompt_parts.append(keywords_text)
            
        # Quality descriptors
        prompt_parts.extend([
            "hyper-realistic", "8K ultra high resolution", 
            "professional photography", "detailed", "beautiful feet"
        ])
        
        return ", ".join(prompt_parts)

    def clear(self):
        """
        Clear the conversation history
        """
        self.messages = []
        self.generated_images = []

    def get_message_count(self) -> int:
        """
        Get the number of messages in the conversation
        
        Returns:
            Number of messages
        """
        return len(self.messages)