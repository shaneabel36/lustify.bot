/**
 * Lustify Bot - Frontend JavaScript
 * 
 * This script handles:
 * - Chat message sending and receiving
 * - Character selection
 * - Image generation requests
 * - UI updates and interactions
 */

// Global state
let currentCharacter = null;
let currentSeed = null;

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const characterSelect = document.getElementById('character-select');
const imagePrompt = document.getElementById('image-prompt');
const generateImageBtn = document.getElementById('generate-image-btn');
const newSeedBtn = document.getElementById('new-seed-btn');
const clearChatBtn = document.getElementById('clear-chat-btn');
const loadingOverlay = document.getElementById('loading-overlay');
const currentSeedDisplay = document.getElementById('current-seed');

/**
 * Initialize the application
 */
async function init() {
    // Load characters
    await loadCharacters();
    
    // Set up event listeners
    setupEventListeners();
    
    console.log('Lustify Bot initialized!');
}

/**
 * Set up all event listeners
 */
function setupEventListeners() {
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key (Shift+Enter for new line)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Character selection
    characterSelect.addEventListener('change', (e) => {
        currentCharacter = e.target.value;
        if (currentCharacter) {
            addSystemMessage(`Character changed to: ${e.target.options[e.target.selectedIndex].text}`);
        }
    });
    
    // Image generation
    generateImageBtn.addEventListener('click', generateImage);
    
    // New seed
    newSeedBtn.addEventListener('click', getNewSeed);
    
    // Clear chat
    clearChatBtn.addEventListener('click', clearChat);
}

/**
 * Load available characters from the API
 */
async function loadCharacters() {
    try {
        const response = await fetch('/api/characters');
        const data = await response.json();
        
        if (data.characters && data.characters.length > 0) {
            characterSelect.innerHTML = '<option value="">No character (default)</option>';
            
            data.characters.forEach(char => {
                const option = document.createElement('option');
                option.value = char.slug;
                option.textContent = char.name;
                characterSelect.appendChild(option);
            });
        } else {
            characterSelect.innerHTML = '<option value="">No adult characters available</option>';
        }
    } catch (error) {
        console.error('Error loading characters:', error);
        characterSelect.innerHTML = '<option value="">Error loading characters</option>';
    }
}

/**
 * Send a chat message
 */
async function sendMessage() {
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input
    chatInput.value = '';
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                character_slug: currentCharacter
            })
        });
        
        const data = await response.json();
        
        if (data.response) {
            // Add assistant response
            addMessage('assistant', data.response);
        } else if (data.error) {
            addSystemMessage(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addSystemMessage('Error: Failed to send message. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Generate an image based on prompt
 */
async function generateImage() {
    const prompt = imagePrompt.value.trim();
    
    if (!prompt) {
        alert('Please enter an image description');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                use_context: true
            })
        });
        
        const data = await response.json();
        
        if (data.image) {
            // Update current seed
            currentSeed = data.seed;
            currentSeedDisplay.textContent = currentSeed;
            
            // Add image to chat
            addImageMessage(data.image, data.prompt);
            
            // Clear prompt input
            imagePrompt.value = '';
        } else if (data.error) {
            addSystemMessage(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error generating image:', error);
        addSystemMessage('Error: Failed to generate image. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Get a new seed for image variations
 */
async function getNewSeed() {
    try {
        const response = await fetch('/api/new-seed', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.seed) {
            currentSeed = data.seed;
            currentSeedDisplay.textContent = currentSeed;
            addSystemMessage(`New seed generated: ${currentSeed}. Next images will have a different style.`);
        }
    } catch (error) {
        console.error('Error getting new seed:', error);
    }
}

/**
 * Clear the chat history
 */
async function clearChat() {
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    try {
        await fetch('/api/clear', {
            method: 'POST'
        });
        
        // Clear chat messages
        chatMessages.innerHTML = '';
        
        // Reset seed
        currentSeed = null;
        currentSeedDisplay.textContent = 'Not set';
        
        addSystemMessage('Chat history cleared.');
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

/**
 * Add a message to the chat
 */
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = role === 'user' ? 'You' : 'Lustify Bot';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    if (role === 'user') {
        messageDiv.appendChild(label);
        messageDiv.appendChild(contentDiv);
    } else {
        messageDiv.appendChild(label);
        messageDiv.appendChild(contentDiv);
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add an image message to the chat
 */
function addImageMessage(base64Image, prompt) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = 'Generated Image';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const imageContainer = document.createElement('div');
    imageContainer.className = 'message-image';
    
    const img = document.createElement('img');
    img.src = `data:image/png;base64,${base64Image}`;
    img.alt = 'Generated image';
    img.onclick = () => openImageInNewTab(img.src);
    
    const info = document.createElement('div');
    info.className = 'image-info';
    info.textContent = `Prompt: ${prompt} | Seed: ${currentSeed}`;
    
    imageContainer.appendChild(img);
    imageContainer.appendChild(info);
    contentDiv.appendChild(imageContainer);
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add a system message to the chat
 */
function addSystemMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.style.textAlign = 'center';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.background = '#f0f0f0';
    contentDiv.style.color = '#666';
    contentDiv.style.fontSize = '13px';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Open image in new tab
 */
function openImageInNewTab(src) {
    window.open(src, '_blank');
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Show loading overlay
 */
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);