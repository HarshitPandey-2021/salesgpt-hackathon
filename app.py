import streamlit as st
from main import SalesGPT
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SalesGPT - AI with Memory",
    page_icon="🧠",
    layout="wide"
)

# Initialize
if 'agent' not in st.session_state:
    st.session_state.agent = SalesGPT()

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = {}

if 'current_prospect' not in st.session_state:
    st.session_state.current_prospect = None

# Header
st.title("🧠 SalesGPT - AI Sales Assistant with Memory")
st.markdown("*Powered by Hindsight - The AI that never forgets*")

# Sidebar - Prospect Selection
st.sidebar.header("📋 Select Prospect")

prospects = {
    "Rajesh Kumar": {
        "company": "TechCorp India",
        "role": "VP of Engineering",
        "status": "🟡 In Progress"
    },
    "Priya Sharma": {
        "company": "StartupXYZ",
        "role": "Founder & CEO",
        "status": "🟢 Hot Lead"
    },
    "John Smith": {
        "company": "BigEnterprise Corp",
        "role": "CTO",
        "status": "🔵 Discovery"
    },
    "Anita Desai": {
        "company": "FinanceFlow Ltd",
        "role": "Director of Sales",
        "status": "🟡 In Progress"
    },
    "Michael Chen": {
        "company": "CloudScale",
        "role": "Head of Operations",
        "status": "🔴 Follow-up Needed"
    }
}

# Prospect selector
prospect_options = [f"{name} - {info['company']}" for name, info in prospects.items()]
selected = st.sidebar.selectbox(
    "Choose prospect:",
    prospect_options,
    index=0
)

# Extract prospect name
prospect_name = selected.split(" - ")[0]
st.session_state.current_prospect = prospect_name

# Show prospect info card
prospect_info = prospects[prospect_name]
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {prospect_name}")
st.sidebar.markdown(f"**Company:** {prospect_info['company']}")
st.sidebar.markdown(f"**Role:** {prospect_info['role']}")
st.sidebar.markdown(f"**Status:** {prospect_info['status']}")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Memory Enabled**\n\nThis AI remembers ALL past conversations with this prospect!")

# Initialize conversation history for this prospect if not exists
if prospect_name not in st.session_state.conversation_history:
    st.session_state.conversation_history[prospect_name] = []

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"💬 Chat with {prospect_name}")

with col2:
    if st.button("🔄 New Conversation Session"):
        st.session_state.conversation_history[prospect_name] = []
        st.rerun()

# Display conversation history for current prospect
current_history = st.session_state.conversation_history[prospect_name]

if len(current_history) == 0:
    st.info(f"👋 Start a conversation with {prospect_name}. The AI will remember everything you discuss!")
else:
    for message in current_history:
        if message['role'] == 'user':
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**You (Sales Rep):**\n\n{message['content']}")
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**SalesGPT:**\n\n{message['content']}")
                if 'timestamp' in message:
                    st.caption(f"🕒 {message['timestamp']}")

# Input area
st.markdown("---")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your message to the AI:",
        placeholder=f"Example: Hi {prospect_name}, I wanted to follow up on our last conversation...",
        height=100,
        key="user_input_field"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        submit = st.form_submit_button("📤 Send", use_container_width=True)
    
    with col2:
        simulate = st.form_submit_button("🎭 Simulate Prospect Reply", use_container_width=True)
    
    if submit and user_input:
        # Add user message to history
        st.session_state.conversation_history[prospect_name].append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Get AI response
        with st.spinner("🧠 SalesGPT is thinking and checking memory..."):
            ai_response = st.session_state.agent.chat(
                prospect_name=prospect_name,
                user_message=user_input
            )
        
        # Add AI response to history
        st.session_state.conversation_history[prospect_name].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        st.rerun()
    
    elif simulate and user_input:
        # Simulate prospect response (for demo purposes)
        st.session_state.conversation_history[prospect_name].append({
            'role': 'user',
            'content': f"[PROSPECT RESPONSE]: {user_input}",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Save to memory
        st.session_state.agent.save_to_memory(
            prospect_name=prospect_name,
            conversation_text=f"Prospect said: {user_input}"
        )
        
        st.success("✅ Prospect response saved to memory!")
        st.rerun()

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Session Stats")
st.sidebar.metric("Messages in this session", len(current_history))

total_messages = sum(len(hist) for hist in st.session_state.conversation_history.values())
st.sidebar.metric("Total messages (all prospects)", total_messages)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Hindsight by Vectorize | Hackathon 2026")