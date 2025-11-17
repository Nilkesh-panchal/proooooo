# -*- coding: utf-8 -*-
"""
AI COMPANION AGENT - RELIABLE PUBLIC VERSION
Works for everyone! Guaranteed deployment success!
"""

import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="AI Companion", page_icon="🤖", layout="wide")

# CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e1b4b, #0f172a); }
.user-msg { background: linear-gradient(135deg, #3b82f6, #06b6d4); color: white; padding: 1rem; border-radius: 1rem; margin: 0.5rem 0 0.5rem 20%; animation: slideIn 0.3s; }
.assistant-msg { background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3); color: white; padding: 1rem; border-radius: 1rem; margin: 0.5rem 20% 0.5rem 0; animation: slideIn 0.3s; }
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'memory' not in st.session_state:
    st.session_state.memory = {'name': None, 'interests': [], 'count': 0}
if 'mode' not in st.session_state:
    st.session_state.mode = 'friend'
if 'memes' not in st.session_state:
    st.session_state.memes = []

# PERSONALITY MODES WITH RESPONSE TEMPLATES
MODES = {
    'friend': {
        'name': '☕ Chill Friend',
        'emoji': '☕',
        'responses': {
            'greeting': ["Hey! How's it going?", "Hi there! What's up?", "Hey friend! What's on your mind?"],
            'question': ["That's interesting! Tell me more.", "I hear you. What happened next?", "Totally get that. How do you feel about it?"],
            'statement': ["I understand. That makes sense!", "Yeah, I can see where you're coming from.", "That's a good point!"],
            'emotion': ["I'm here for you! Want to talk about it?", "That sounds tough. How are you holding up?", "I get it. Thanks for sharing that with me."]
        }
    },
    'roast': {
        'name': '😂 Roast Master',
        'emoji': '😂',
        'responses': {
            'greeting': ["Oh look who decided to show up 😏", "Well well well... what do we have here?", "Ah, you again. Lucky me!"],
            'question': ["Really? THAT's what you're asking? 😂", "Oh sure, because that's totally a reasonable question...", "Bold of you to assume I care about that!"],
            'statement': ["Sure, Jan. That definitely happened.", "Oh really? And I'm sure everyone clapped too 🙄", "Wow, fascinating story. Tell it again but better."],
            'emotion': ["Aww, need a tissue? 😏", "Oh no... anyway...", "That's rough buddy. Actually no, it's hilarious."]
        }
    },
    'debate': {
        'name': '⚔️ Debate Beast',
        'emoji': '⚔️',
        'responses': {
            'greeting': ["Let's have an intellectually stimulating discussion.", "Ready for a logical debate?", "I'm prepared to challenge your arguments."],
            'question': ["That assumes a premise that needs examination. Consider this counterpoint...", "Interesting question, but have you considered the alternative?", "Let me challenge that assumption with evidence..."],
            'statement': ["I disagree. Here's why that logic is flawed...", "That argument has several holes. Let me point them out.", "Respectfully, your reasoning overlooks key factors."],
            'emotion': ["Emotions aside, let's focus on the logic here.", "I understand your feelings, but the facts say otherwise.", "Valid emotion, but let's examine the reasoning."]
        }
    },
    'hype': {
        'name': '✨ Hype Squad',
        'emoji': '✨',
        'responses': {
            'greeting': ["OMG HI!!! SO EXCITED TO SEE YOU!!!", "YES!!! YOU'RE HERE!!! THIS IS AMAZING!!!", "YAAAS!!! LET'S GOOOO!!!"],
            'question': ["THAT'S AN INCREDIBLE QUESTION!!! I LOVE IT!!!", "OMG YES!!! BRILLIANT THINKING!!!", "WOW!!! SO SMART!!! TELL ME MORE!!!"],
            'statement': ["THAT'S ABSOLUTELY AMAZING!!! YOU'RE KILLING IT!!!", "YES YES YES!!! SO PROUD OF YOU!!!", "OMG THAT'S SO GOOD!!! KEEP GOING!!!"],
            'emotion': ["YOU'VE GOT THIS!!! I BELIEVE IN YOU 100%!!!", "SENDING ALL THE POSITIVE VIBES YOUR WAY!!!", "YOU'RE AMAZING AND STRONG!!! WE'RE IN THIS TOGETHER!!!"]
        }
    },
    'journal': {
        'name': '📓 Journal Guide',
        'emoji': '📓',
        'responses': {
            'greeting': ["Welcome. What's on your mind today?", "Hello. What would you like to reflect on?", "Hi there. What brings you here today?"],
            'question': ["That's a thoughtful question. What made you think of that?", "Interesting. Why does that matter to you?", "Good question. What feelings does that bring up?"],
            'statement': ["I see. How does that make you feel?", "Thank you for sharing. What does that mean to you?", "That's significant. Why is that important to you?"],
            'emotion': ["Your feelings are valid. What's behind those emotions?", "Thank you for being vulnerable. What do you need right now?", "That must be difficult. What are you learning from this?"]
        }
    },
    'brainstorm': {
        'name': '💡 Brainstorm',
        'emoji': '💡',
        'responses': {
            'greeting': ["Let's get creative! What are we brainstorming today?", "Ooh, idea time! What's the challenge?", "Ready to think outside the box! What's the topic?"],
            'question': ["Great question! Here's a wild idea: what if we...", "Love it! Maybe we could approach it like...", "Hmm, what if we flipped that and tried..."],
            'statement': ["Cool! Building on that, we could also...", "Yes! And what if we combined that with...", "Interesting! That makes me think we could..."],
            'emotion': ["I hear you. Let's channel that energy into creative solutions!", "Those feelings are valid. Now, what possibilities could address them?", "I get it. Let's brainstorm ways to make this better!"]
        }
    }
}

def detect_message_type(message):
    """Simple message classification"""
    msg_lower = message.lower().strip()
    
    # Check for greetings
    greetings = ['hi', 'hello', 'hey', 'sup', 'yo', 'greetings', 'howdy']
    if any(msg_lower.startswith(g) for g in greetings) or len(msg_lower) < 15:
        return 'greeting'
    
    # Check for questions
    if '?' in message or msg_lower.startswith(('what', 'how', 'why', 'when', 'where', 'who', 'can', 'could', 'would', 'should')):
        return 'question'
    
    # Check for emotions
    emotions = ['feel', 'sad', 'happy', 'angry', 'upset', 'excited', 'worried', 'anxious', 'depressed', 'love', 'hate']
    if any(emotion in msg_lower for emotion in emotions):
        return 'emotion'
    
    # Default to statement
    return 'statement'

def generate_response(user_msg):
    """Generate contextual response based on mode and message type"""
    mode_data = MODES[st.session_state.mode]
    msg_type = detect_message_type(user_msg)
    
    # Get appropriate response template
    responses = mode_data['responses'].get(msg_type, mode_data['responses']['statement'])
    base_response = random.choice(responses)
    
    # Add memory context if available
    memory_context = ""
    mem = st.session_state.memory
    if mem['name'] and random.random() > 0.7:  # 30% chance to use name
        memory_context = f" {mem['name']},"
    
    # Combine
    if memory_context:
        base_response = base_response.replace("!", f"{memory_context}!")
        base_response = base_response.replace(".", f"{memory_context}.")
    
    return base_response

def simple_meme_generator():
    if len(st.session_state.conversation) < 2:
        st.warning("Chat more first!")
        return
    
    templates = ["Drake", "Distracted Boyfriend", "Two Buttons", "Change My Mind", "Expanding Brain"]
    
    recent = st.session_state.conversation[-4:]
    user_msgs = [m['content'][:45] for m in recent if m['role'] == 'user']
    ai_msgs = [m['content'][:45] for m in recent if m['role'] == 'assistant']
    
    meme = {
        'template': random.choice(templates),
        'topText': user_msgs[-1] if user_msgs else "Chatting with AI",
        'bottomText': ai_msgs[-1] if ai_msgs else "Actually helpful",
        'context': f"From {MODES[st.session_state.mode]['name']} mode",
        'date': datetime.now().isoformat()
    }
    
    st.session_state.memes.append(meme)
    st.success("✅ Meme created!")

# UI
st.title("🤖 AI Companion Agent")
st.caption("✨ FREE for Everyone | No Setup Needed!")

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.success("🌐 **Public & Free!**\n\nWorks instantly!\nNo API keys needed!")
    
    st.divider()
    st.subheader("🎭 Personality")
    
    cols = st.columns(2)
    for idx, (key, mode) in enumerate(MODES.items()):
        col = cols[idx % 2]
        with col:
            if st.button(mode['emoji'], key=f"m_{key}", 
                        use_container_width=True,
                        help=mode['name'],
                        type="primary" if key==st.session_state.mode else "secondary"):
                st.session_state.mode = key
                st.rerun()
    
    st.caption(f"**Current:** {MODES[st.session_state.mode]['name']}")
    
    st.divider()
    st.subheader("📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", st.session_state.memory['count'])
    with col2:
        st.metric("🎨 Memes", len(st.session_state.memes))
    
    st.divider()
    with st.expander("🧠 Memory"):
        m = st.session_state.memory
        if m['name']: st.write(f"**Name:** {m['name']}")
        if m['interests']: st.write(f"**Interests:** {', '.join(m['interests'][:3])}")
        if not any([m['name'], m['interests']]): st.info("Chat to build memories!")
        
        if st.button("🗑️ Clear", use_container_width=True, key="clear_mem"):
            st.session_state.memory = {'name': None, 'interests': [], 'count': 0}
            st.rerun()
    
    with st.expander("🎨 Memes"):
        if st.session_state.memes:
            for meme in reversed(st.session_state.memes[-2:]):
                st.markdown(f"**{meme['template']}**")
                st.caption(f"{meme['topText']}")
                st.caption(f"{meme['bottomText']}")
        else:
            st.info("Create memes!")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Meme", use_container_width=True, key="meme"):
            simple_meme_generator()
            st.rerun()
    with col2:
        if st.button("🔄 Clear", use_container_width=True, key="clear"):
            st.session_state.conversation = []
            st.rerun()

# Chat Display
for msg in st.session_state.conversation:
    css = "user-msg" if msg["role"]=="user" else "assistant-msg"
    st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("💬 Type your message...")

if user_input:
    # Add user message
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Generate response
    response = generate_response(user_input)
    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.session_state.memory['count'] += 1
    
    # Extract memory
    user_lower = user_input.lower()
    
    # Extract name
    for phrase in ['my name is', "i'm ", "i am ", "call me "]:
        if phrase in user_lower:
            parts = user_lower.split(phrase)
            if len(parts) > 1:
                name = parts[1].split()[0].strip('.,!?').capitalize()
                if len(name) > 1 and name.isalpha():
                    st.session_state.memory['name'] = name
                    break
    
    # Extract interests
    for keyword in ['i like', 'i love', 'i enjoy', 'into ', 'passionate about']:
        if keyword in user_lower:
            parts = user_lower.split(keyword)
            if len(parts) > 1:
                interest = parts[1].split('.')[0].split(',')[0].split(' and ')[0].strip()
                if interest and len(interest) > 2:
                    if interest not in st.session_state.memory['interests']:
                        st.session_state.memory['interests'].append(interest)
                    break
    
    st.rerun()

st.markdown("---")
st.markdown('<div style="text-align: center; color: rgba(168,85,247,0.6); font-size: 0.75rem;">✨ AI Companion - Reliable & Fast | Works for Everyone!</div>', unsafe_allow_html=True)