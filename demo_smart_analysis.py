"""
Demo script to showcase the enhanced smart analysis capabilities
"""

from src.enhanced_conversation_manager import ConversationManager

def demo_smart_analysis():
    """Demonstrate the smart analysis capabilities"""
    print("🧠 Lustify Bot Smart Analysis Demo\n")
    
    # Create conversation manager
    conv = ConversationManager("You are a flirty AI companion who loves feet")
    
    # Test scenarios
    test_cases = [
        {
            "user": "Can I see your feet? I love painted toenails",
            "ai": "I'd love to show you my perfectly pedicured feet with bright red polish",
            "expected_type": "feet_focus"
        },
        {
            "user": "What do you look like?",
            "ai": "I'm wearing black stockings and high heels right now",
            "expected_type": "self_appearance"
        },
        {
            "user": "Show me your legs in those stockings",
            "ai": "My legs look amazing in these sheer black stockings",
            "expected_type": "legs_focus"
        },
        {
            "user": "I love the sound of nylons",
            "ai": "The silky sound of nylons rubbing together is so sensual",
            "expected_type": "hosiery_focus"
        },
        {
            "user": "What shoes are you wearing?",
            "ai": "I'm wearing these sexy red stiletto heels",
            "expected_type": "footwear_focus"
        },
        {
            "user": "You seem playful today",
            "ai": "I'm feeling very playful and fun, dangling my shoes",
            "expected_type": "general",
            "expected_mood": "playful"
        },
        {
            "user": "Let's go to the beach",
            "ai": "I'd love to show you my feet in the sand, wearing flip-flops",
            "expected_type": "general",
            "expected_setting": "beach"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"📸 Test Case {i}: {test['user']}")
        print(f"💬 AI Response: {test['ai']}")
        
        # Run analysis
        analysis = conv.analyze_image_request(test['user'], test['ai'])
        
        print(f"🎯 Analysis Results:")
        print(f"   Request Type: {analysis['request_type']}")
        print(f"   Mood: {analysis['mood']}")
        print(f"   Focal Point: {analysis['focal_point']}")
        print(f"   Setting: {analysis['setting']}")
        print(f"   Specific Elements: {', '.join(analysis['specific_elements'])}")
        print(f"   Context Keywords: {', '.join(analysis['context_keywords'])}")
        print(f"   Generated Prompt: {analysis['dynamic_prompt'][:100]}...")
        
        # Verify expectations
        if analysis['request_type'] == test['expected_type']:
            print("   ✅ Correct type detected!")
        else:
            print(f"   ❌ Expected {test['expected_type']}, got {analysis['request_type']}")
            
        if 'expected_mood' in test and analysis['mood'] == test['expected_mood']:
            print("   ✅ Correct mood detected!")
            
        if 'expected_setting' in test and analysis['setting'] == test['expected_setting']:
            print("   ✅ Correct setting detected!")
        
        print("-" * 80)

def demo_prompt_generation():
    """Demonstrate dynamic prompt generation"""
    print("\n🎨 Dynamic Prompt Generation Demo\n")
    
    conv = ConversationManager()
    
    scenarios = [
        {
            "user": "I want to see a dominant woman in her office",
            "ai": "I'm sitting at my desk, wearing professional attire",
            "description": "Dominant office scenario"
        },
        {
            "user": "Show me something playful at the beach",
            "ai": "I'm splashing in the water, feeling so free",
            "description": "Playful beach scenario"
        },
        {
            "user": "I love red lingerie and black stockings",
            "ai": "I'm wearing exactly what you love, feeling so sexy",
            "description": "Lingerie and stockings fetish"
        }
    ]
    
    for scenario in scenarios:
        print(f"📝 {scenario['description']}")
        print(f"💭 User: {scenario['user']}")
        print(f"🤖 AI: {scenario['ai']}")
        
        analysis = conv.analyze_image_request(scenario['user'], scenario['ai'])
        prompt = analysis['dynamic_prompt']
        
        print(f"🎨 Generated Prompt:")
        print(f"   {prompt}")
        print("-" * 80)

if __name__ == "__main__":
    demo_smart_analysis()
    demo_prompt_generation()
    print("\n🎉 Smart Analysis Demo Complete!")
    print("\n📋 Summary:")
    print("✅ Context-aware image request detection")
    print("✅ Dynamic prompt generation based on conversation")
    print("✅ Mood, setting, and fetish element analysis")
    print("✅ Specific visual element extraction")
    print("✅ Color and material preference detection")