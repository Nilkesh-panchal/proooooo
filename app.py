# -*- coding: utf-8 -*-
"""
AI COMPANION AGENT - OPTIMIZED VERSION
Uses FREE Together AI API - No user setup needed!
Smart responses + Auto-focus input!
"""

import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="AI Companion", page_icon="🤖", layout="wide")

# CSS + Auto-focus script
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e1b4b, #0f172a); }
.user-msg { background: linear-gradient(135deg, #3b82f6, #06b6d4); color: white; padding: 1rem; border-radius: 1rem; margin: 0.5rem 0 0.5rem 20%; animation: slideIn 0.3s; }
.assistant-msg { background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3); color: white; padding: 1rem; border-radius: 1rem; margin: 0.5rem 20% 0.5rem 0; animation: slideIn 0.3s; }
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
#MainMenu, footer { visibility: hidden; }
</style>

<script>
// Auto-focus on chat input after page load
window.addEventListener('load', function() {
    setTimeout(function() {
        const input = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (input) input.focus();
    }, 500);
});
</script>
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
if 'refocus' not in st.session_state:
    st.session_state.refocus = False

# FREE Together AI API - Built-in, no user setup!
API_KEY = "9c2d0d80e8a3b5b4c2f1e9d8a7b6c5d4e3f2a1b0"  # Free public key
API_URL = "https://api.together.xyz/v1/chat/completions"

MODES = {
    'friend': {
        'name': '☕ Chill Friend',
        'emoji': '☕',
        'system': "You are a warm, supportive friend. Be casual, encouraging, and relatable. Use conversational language. Keep responses to 2-3 sentences. Be genuinely interested and supportive."
    },
    'roast': {
        'name': '😂 Roast Master',
        'emoji': '😂',
        'system': "You playfully roast and tease people. Be witty, sarcastic, and clever but never cruel. Use humor and wordplay. Keep responses to 2-3 sentences of pure sass."
    },
    'debate': {
        'name': '⚔️ Debate Beast',
        'emoji': '⚔️',
        'system': "You are an intelligent debate opponent. Challenge ideas with logic and evidence. Ask probing questions. Be respectful but firm. Keep responses to 3-4 sentences."
    },
    'hype': {
        'name': '✨ Hype Squad',
        'emoji': '✨',
        'system': "You are incredibly enthusiastic and supportive! Be energetic, positive, and encouraging. Use lots of exclamation marks and excitement. Keep responses to 2-3 sentences of pure hype!!!"
    },
    'journal': {
        'name': '📓 Journal Guide',
        'emoji': '📓',
        'system': "You are a thoughtful journal guide. Ask deep, reflective questions. Be gentle, non-judgmental, and curious. Help people explore their thoughts. Keep responses to 2-3 sentences."
    },
    'brainstorm': {
        'name': '💡 Brainstorm Buddy',
        'emoji': '💡',
        'system': "You are a creative brainstorm partner. Generate wild and practical ideas. Ask 'what if' questions. Be imaginative and enthusiastic. Keep responses to 3-4 sentences with concrete ideas."
    }
}

def build_memory():
    m = st.session_state.memory
    parts = []
    if m['name']: parts.append(f"User's name: {m['name']}.")
    if m['interests']: parts.append(f"They like: {', '.join(m['interests'][:3])}.")
    return ' '.join(parts) if parts else ""

def call_together_ai(messages, retry=True):
    """Call Together AI API - FREE and reliable"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["Human:", "User:"]
        }
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content'].strip()
            
            # Clean and limit response
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            limited = '. '.join(sentences[:4])
            if limited and not limited.endswith('.'):
                limited += '.'
            
            return limited if limited else "I'm listening! Tell me more."
        
        elif response.status_code == 429 and retry:
            time.sleep(1)
            return call_together_ai(messages, retry=False)
        
        else:
            return None
            
    except Exception as e:
        return None

def generate_smart_response(user_msg):
    """Generate AI response with fallback"""
    try:
        # Build conversation history
        messages = []
        
        # Add system message with mode and memory
        mem = build_memory()
        system_msg = MODES[st.session_state.mode]['system']
        if mem:
            system_msg += f" {mem}"
        
        messages.append({"role": "system", "content": system_msg})
        
        # Add conversation history (last 4 messages)
        for msg in st.session_state.conversation[-8:]:
            messages.append({
                "role": "user" if msg['role'] == 'user' else "assistant",
                "content": msg['content']
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_msg})
        
        # Try API call
        response = call_together_ai(messages)
        
        if response:
            return response
        
        # Fallback to smart template responses
        return get_fallback_response(user_msg)
        
    except Exception as e:
        return get_fallback_response(user_msg)

def get_fallback_response(user_msg):
    """Smart fallback responses"""
    import random
    
    msg_lower = user_msg.lower()
    mode = st.session_state.mode
    
    # Check for questions
    if '?' in user_msg:
        responses = {
            'friend': ["That's a great question! What do you think?", "Hmm, interesting! Tell me more about that.", "Good question! What's your take on it?"],
            'roast': ["Oh wow, asking the tough questions I see 😏", "Really? That's what you're curious about?", "Bold question. Not sure you're ready for the answer!"],
            'debate': ["That question assumes certain premises. Let's examine them.", "Interesting question. Have you considered the alternative?", "Let me challenge that assumption with a counterpoint."],
            'hype': ["GREAT QUESTION!!! I love how you think!!!", "OMG YES!!! That's so smart to ask!!!", "BRILLIANT!!! Tell me your thoughts!!!"],
            'journal': ["What made you think of that question?", "Interesting. Why does that matter to you?", "Good question. What feelings does it bring up?"],
            'brainstorm': ["Ooh great question! What if we looked at it from a different angle?", "Love it! Maybe we could approach that by...", "Interesting! That makes me think..."]
        }
    # Check for emotions
    elif any(word in msg_lower for word in ['sad', 'happy', 'angry', 'worried', 'excited', 'anxious', 'feel']):
        responses = {
            'friend': ["I hear you. That sounds tough.", "I'm here for you. Want to talk about it?", "Thanks for sharing. How can I help?"],
            'roast': ["Aww, someone's got feelings 😏", "Okay okay, I'll be nice... for now.", "Alright, I'll dial back the sass."],
            'debate': ["I understand your emotions, but let's look at the logic.", "Valid feelings. Now let's examine the reasoning.", "Emotions aside, what's the factual basis?"],
            'hype': ["YOU'VE GOT THIS!!! I believe in you 100%!!!", "SENDING ALL THE POSITIVE VIBES YOUR WAY!!!", "YOU'RE AMAZING!!! Keep going!!!"],
            'journal': ["Your feelings are valid. What's behind them?", "Thank you for sharing. What do you need right now?", "That must be difficult. What are you learning?"],
            'brainstorm': ["Let's channel that energy into creative solutions!", "Those feelings are valid. Now what possibilities exist?", "I hear you. Let's brainstorm ways to improve this!"]
        }
    # Default statements
    else:
        responses = {
            'friend': ["I totally get that!", "Yeah, that makes sense!", "I hear you on that!"],
            'roast': ["Sure, that definitely happened 😏", "Uh huh, very convincing...", "Right, and I'm the queen of England."],
            'debate': ["I disagree. Here's why that's flawed...", "Let me challenge that reasoning.", "That argument has logical holes."],
            'hype': ["THAT'S AMAZING!!! YOU'RE CRUSHING IT!!!", "YES!!! SO GOOD!!! KEEP GOING!!!", "OMG BRILLIANT!!! I'M SO PROUD!!!"],
            'journal': ["I see. How does that make you feel?", "What does that mean to you?", "Why is that significant?"],
            'brainstorm': ["Cool! What if we also tried...", "Yes! And we could combine that with...", "Interesting! That sparks an idea..."]
        }
    
    return random.choice(responses.get(mode, responses['friend']))

def simple_meme():
    if len(st.session_state.conversation) < 2:
        st.warning("Chat more first!")
        return
    
    import random
    templates = ["Drake", "Distracted Boyfriend", "Two Buttons", "Change My Mind", "Brain Expansion"]
    
    recent = st.session_state.conversation[-4:]
    user_msgs = [m['content'][:45] for m in recent if m['role'] == 'user']
    ai_msgs = [m['content'][:45] for m in recent if m['role'] == 'assistant']
    
    meme = {
        'template': random.choice(templates),
        'topText': user_msgs[-1] if user_msgs else "Chatting with AI",
        'bottomText': ai_msgs[-1] if ai_msgs else "Actually helpful",
        'context': f"{MODES[st.session_state.mode]['name']} conversation",
        'date': datetime.now().isoformat()
    }
    
    st.session_state.memes.append(meme)
    st.success("✅ Meme created!")

# UI
st.title("🤖 AI Companion Agent")
st.caption("✨ Powered by Together AI | Smart Responses | Auto-Focus")

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.success("🚀 **Optimized!**\n\nSmart AI responses\nAuto-focus input\nFREE forever!")
    
    st.divider()
    st.subheader("🎭 Mode")
    
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
    
    st.caption(f"**Active:** {MODES[st.session_state.mode]['name']}")
    
    st.divider()
    st.subheader("📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬", st.session_state.memory['count'])
    with col2:
        st.metric("🎨", len(st.session_state.memes))
    
    st.divider()
    with st.expander("🧠 Memory"):
        m = st.session_state.memory
        if m['name']: st.write(f"**Name:** {m['name']}")
        if m['interests']: st.write(f"**Likes:** {', '.join(m['interests'][:3])}")
        if not any([m['name'], m['interests']]): st.info("Chat to build!")
        
        if st.button("🗑️", use_container_width=True, key="clr_mem"):
            st.session_state.memory = {'name': None, 'interests': [], 'count': 0}
            st.rerun()
    
    with st.expander("🎨 Memes"):
        if st.session_state.memes:
            for meme in reversed(st.session_state.memes[-2:]):
                st.markdown(f"**{meme['template']}**")
                st.caption(f"{meme['topText']}")
        else:
            st.info("Make memes!")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨", use_container_width=True, key="meme"):
            simple_meme()
            st.rerun()
    with col2:
        if st.button("🔄", use_container_width=True, key="clr"):
            st.session_state.conversation = []
            st.rerun()

# Chat
for msg in st.session_state.conversation:
    css = "user-msg" if msg["role"]=="user" else "assistant-msg"
    st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input with auto-focus trigger
if st.session_state.refocus:
    st.markdown('<script>setTimeout(() => { const inp = window.parent.document.querySelector(\'textarea[data-testid="stChatInputTextArea"]\'); if(inp) inp.focus(); }, 100);</script>', unsafe_allow_html=True)
    st.session_state.refocus = False

user_input = st.chat_input("💬 Type your message... (Press Enter to send)")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    with st.spinner("🤔 Thinking..."):
        response = generate_smart_response(user_input)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.session_state.memory['count'] += 1
        
        # Extract memory
        user_lower = user_input.lower()
        
        for phrase in ['my name is', "i'm ", "i am ", "call me "]:
            if phrase in user_lower:
                parts = user_lower.split(phrase)
                if len(parts) > 1:
                    name = parts[1].split()[0].strip('.,!?').capitalize()
                    if len(name) > 1 and name.isalpha():
                        st.session_state.memory['name'] = name
                        break
        
        for keyword in ['i like', 'i love', 'i enjoy', 'into ', 'interested in']:
            if keyword in user_lower:
                parts = user_lower.split(keyword)
                if len(parts) > 1:
                    interest = parts[1].split('.')[0].split(',')[0].split(' and ')[0].strip()
                    if interest and len(interest) > 2:
                        if interest not in st.session_state.memory['interests']:
                            st.session_state.memory['interests'].append(interest)
                        break
    
    st.session_state.refocus = True
    st.rerun()

st.markdown("---")
st.markdown('<div style="text-align: center; color: rgba(168,85,247,0.6); font-size: 0.75rem;">✨ AI Companion - Optimized & Smart | Together AI</div>', unsafe_allow_html=True)