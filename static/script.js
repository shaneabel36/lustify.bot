/**
 * Lustify Bot - Enhanced Frontend JavaScript with Smart Context Analysis
 * 
 * This script handles:
 * - Chat message sending and receiving
 * - Character selection
 * - Smart image generation requests with context analysis
 * - UI updates and interactions
 */

// Global state
let currentCharacter = null;
let currentSeed = null;
let lastUserMessage = '';
let lastAiResponse = '';

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
    
    console.log('Lustify Bot Enhanced initialized!');
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
        const response = await fetch('/characters');
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
    
    // Store user message for context
    lastUserMessage = message;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input
    chatInput.value = '';
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/chat', {
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
            // Store AI response for context
            lastAiResponse = data.response;
            
            // Add assistant response
            addMessage('assistant', data.response);
            
            // Check for image generation triggers
            checkForImageTriggers(data.response);
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
        const response = await fetch('/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                use_context: false,
                user_message: lastUserMessage,
                ai_response: lastAiResponse,
                smart_analysis: true
            })
        });
        
        const data = await response.json();
        
        if (data.image) {
            // Update current seed
            currentSeed = data.seed;
            currentSeedDisplay.textContent = currentSeed;
            
            // Add image to chat with enhanced info
            addEnhancedImageMessage(data.image, data.prompt, data.analysis);
            
            // Show analysis info to user
            if (data.analysis && data.analysis.request_type) {
                const analysisText = generateAnalysisSummary(data.analysis);
                addSystemMessage(`Smart Analysis: ${analysisText} 🧠✨`);
            }
            
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
        const response = await fetch('/new-seed', {
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
        await fetch('/clear', {
            method: 'POST'
        });
        
        // Clear chat messages
        chatMessages.innerHTML = '';
        
        // Reset seed
        currentSeed = null;
        currentSeedDisplay.textContent = 'Not set';
        
        // Clear context
        lastUserMessage = '';
        lastAiResponse = '';
        
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
 * Add an enhanced image message to the chat with analysis info
 */
function addEnhancedImageMessage(base64Image, prompt, analysis) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = 'Smart Generated Image';
    
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
    
    // Build info text with analysis details
    let infoText = `Generated for: ${prompt}`;
    if (analysis && analysis.request_type) {
        infoText += ` | Type: ${analysis.request_type.replace('_', ' ')}`;
        if (analysis.mood && analysis.mood !== 'seductive') {
            infoText += ` | Mood: ${analysis.mood}`;
        }
        if (analysis.focal_point && analysis.focal_point !== 'feet') {
            infoText += ` | Focus: ${analysis.focal_point}`;
        }
    }
    infoText += ` | Seed: ${currentSeed}`;
    
    info.textContent = infoText;
    
    // Add analysis details if available
    if (analysis && analysis.detected_elements && analysis.detected_elements.length > 0) {
        const elementsInfo = document.createElement('div');
        elementsInfo.className = 'analysis-details';
        elementsInfo.innerHTML = `<strong>Detected:</strong> ${analysis.detected_elements.join(', ')}`;
        imageContainer.appendChild(elementsInfo);
    }
    
    if (analysis && analysis.context_keywords && analysis.context_keywords.length > 0) {
        const keywordsInfo = document.createElement('div');
        keywordsInfo.className = 'analysis-details';
        keywordsInfo.innerHTML = `<strong>Keywords:</strong> ${analysis.context_keywords.join(', ')}`;
        imageContainer.appendChild(keywordsInfo);
    }
    
    imageContainer.appendChild(img);
    imageContainer.appendChild(info);
    contentDiv.appendChild(imageContainer);
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add a basic image message to the chat
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
 * Generate a summary of the analysis for user display
 */
function generateAnalysisSummary(analysis) {
    const parts = [];
    
    if (analysis.request_type) {
        const typeMap = {
            'self_appearance': 'Full Appearance',
            'feet_focus': 'Feet Focus',
            'legs_focus': 'Legs Focus',
            'hosiery_focus': 'Hosiery Focus',
            'footwear_focus': 'Footwear Focus',
            'general': 'General Scene'
        };
        parts.push(typeMap[analysis.request_type] || analysis.request_type);
    }
    
    if (analysis.mood && analysis.mood !== 'seductive') {
        parts.push(analysis.mood);
    }
    
    if (analysis.setting && analysis.setting !== 'intimate') {
        parts.push(analysis.setting);
    }
    
    return parts.join(', ') || 'Context-Aware';
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

/**
 * Check for image generation triggers in AI response
 */
function checkForImageTriggers(response) {
    // Define trigger phrases for image generation
    const triggers = [
        'pics', 'picture', 'photo', 'image', 'selfie', 'snap',
        'can i see', 'send me a pic', 'show me', 'let me see',
        'what do you look like', 'describe yourself', 'picture of'
    ];

    // Check if response contains any triggers
    const lowerResponse = response.toLowerCase();
    const hasTrigger = triggers.some(trigger => lowerResponse.includes(trigger));

    if (hasTrigger) {
        // Generate an image based on the conversation context
        setTimeout(() => {
            generateContextImage();
        }, 1000); // Delay for natural conversation flow
    }
}

/**
 * Generate an image based on conversation context with smart analysis
 */
async function generateContextImage() {
    showLoading();
    
    try {
        const response = await fetch('/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: 'Contextual image generation',
                use_context: false,
                user_message: lastUserMessage,
                ai_response: lastAiResponse,
                smart_analysis: true
            })
        });

        const data = await response.json();
        
        if (data.image) {
            // Update current seed
            currentSeed = data.seed;
            currentSeedDisplay.textContent = currentSeed;
            
            // Add image to chat with enhanced info
            addEnhancedImageMessage(data.image, data.prompt, data.analysis);
            
            // Show analysis info to user
            if (data.analysis && data.analysis.request_type) {
                const analysisText = generateAnalysisSummary(data.analysis);
                addSystemMessage(`Smart Analysis: ${analysisText} 🧠✨`);
            } else {
                addSystemMessage('Image generated based on our conversation! 📸');
            }
        } else if (data.error) {
            addSystemMessage(`Image generation error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error generating context image:', error);
        addSystemMessage('Sorry, I had trouble generating an image for you.');
    } finally {
        hideLoading();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);