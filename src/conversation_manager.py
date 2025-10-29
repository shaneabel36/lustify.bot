"""
Conversation Manager - Handles conversation history and context

This module manages the conversation state, including:
- Message history
- Character selection
- Image generation tracking
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