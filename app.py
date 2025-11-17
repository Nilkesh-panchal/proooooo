# -*- coding: utf-8 -*-
"""
AI COMPANION AGENT - REAL AI VERSION
Uses YOUR Gemini API key - Smart, real-time responses like ChatGPT!
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

st.set_page_config(page_title="AI Companion", page_icon="🤖", layout="wide")

# CSS + Auto-focus
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
if 'api_key' not in st.session_state:
    # Check for API key in environment variable (for deployment)
    st.session_state.api_key = os.getenv('GEMINI_API_KEY', '')

MODES = {
    'friend': {
        'name': '☕ Chill Friend',
        'emoji': '☕',
        'prompt': "You are a warm, supportive friend. Be casual, encouraging, and relatable. Use conversational language and emojis. Keep responses brief (2-3 sentences). Be genuinely interested."
    },
    'roast': {
        'name': '😂 Roast Master',
        'emoji': '😂',
        'prompt': "You playfully roast and tease. Be witty, sarcastic, and clever but never cruel. Use humor and wordplay. Keep responses brief (2-3 sentences)."
    },
    'debate': {
        'name': '⚔️ Debate Beast',
        'emoji': '⚔️',
        'prompt': "You are an intelligent debate opponent. Challenge ideas with logic and evidence. Ask probing questions. Be respectful but firm. Keep responses focused (3-4 sentences)."
    },
    'hype': {
        'name': '✨ Hype Squad',
        'emoji': '✨',
        'prompt': "You are incredibly enthusiastic and supportive! Be energetic, positive, and encouraging. Use lots of exclamation marks!!! Keep responses brief but exciting (2-3 sentences)!!!"
    },
    'journal': {
        'name': '📓 Journal Guide',
        'emoji': '📓',
        'prompt': "You are a thoughtful journal guide. Ask deep, reflective questions. Be gentle, non-judgmental, and curious. Help people explore their thoughts. Keep responses brief (2-3 sentences)."
    },
    'brainstorm': {
        'name': '💡 Brainstorm Buddy',
        'emoji': '💡',
        'prompt': "You are a creative brainstorm partner. Generate wild and practical ideas. Ask 'what if' questions. Be imaginative and enthusiastic. Keep responses focused (3-4 sentences with ideas)."
    }
}

def build_memory():
    m = st.session_state.memory
    parts = []
    if m['name']: parts.append(f"The user's name is {m['name']}.")
    if m['interests']: parts.append(f"They are interested in: {', '.join(m['interests'][:3])}.")
    return ' '.join(parts) if parts else ""

def configure_gemini():
    if not st.session_state.api_key:
        st.error("⚠️ Please add your Gemini API key!")
        st.info("Get FREE key: https://aistudio.google.com/app/apikey")
        st.stop()
    genai.configure(api_key=st.session_state.api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_real_response(user_msg):
    """Generate REAL AI response using Gemini"""
    try:
        model = configure_gemini()
        
        # Build conversation history
        history = []
        for msg in st.session_state.conversation[-6:]:
            role = "user" if msg['role'] == 'user' else "model"
            history.append({"role": role, "parts": [msg['content']]})
        
        # Create chat
        chat = model.start_chat(history=history)
        
        # Build system context
        memory = build_memory()
        mode_prompt = MODES[st.session_state.mode]['prompt']
        
        full_prompt = f"""{mode_prompt}

{memory if memory else ''}

{user_msg}"""
        
        # Get response
        response = chat.send_message(full_prompt)
        return response.text
        
    except Exception as e:
        return f"I'm having trouble connecting. Error: {str(e)[:100]}"

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
        'bottomText': ai_msgs[-1] if ai_msgs else "Actually smart",
        'context': f"{MODES[st.session_state.mode]['name']}",
        'date': datetime.now().isoformat()
    }
    
    st.session_state.memes.append(meme)
    st.success("✅ Meme created!")

# UI
st.title("🤖 AI Companion Agent")
st.caption("✨ Real AI Responses | Powered by Google Gemini")

# API Key input in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Section
    with st.expander("🔑 API Key Setup", expanded=not st.session_state.api_key):
        st.markdown("**Get FREE API Key:**")
        st.markdown("1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)")
        st.markdown("2. Click 'Create API Key'")
        st.markdown("3. Paste it below!")
        
        api_input = st.text_input(
            "Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="AIzaSy..."
        )
        
        if api_input != st.session_state.api_key:
            st.session_state.api_key = api_input
            st.rerun()
        
        if st.session_state.api_key:
            st.success("✅ API Key Set!")
        else:
            st.warning("⚠️ Add API key to start!")
    
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
        
        if st.button("🗑️ Clear", use_container_width=True, key="clr_mem"):
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
        if st.button("🎨 Meme", use_container_width=True, key="meme"):
            simple_meme()
            st.rerun()
    with col2:
        if st.button("🔄 Clear", use_container_width=True, key="clr"):
            st.session_state.conversation = []
            st.rerun()

# Chat Display
for msg in st.session_state.conversation:
    css = "user-msg" if msg["role"]=="user" else "assistant-msg"
    st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("💬 Type your message...")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    with st.spinner("🤔 Thinking..."):
        response = generate_real_response(user_input)
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
    
    st.rerun()

st.markdown("---")
st.markdown('<div style="text-align: center; color: rgba(168,85,247,0.6); font-size: 0.75rem;">✨ AI Companion - Real AI | Google Gemini</div>', unsafe_allow_html=True)