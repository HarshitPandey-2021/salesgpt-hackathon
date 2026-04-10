import streamlit as st
from main import SalesGPT
import json

# Initialize
if 'agent' not in st.session_state:
    st.session_state.agent = SalesGPT()

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Page config
st.set_page_config(
    page_title="SalesGPT - AI with Memory",
    page_icon="🧠",
    layout="wide"
)

# Header
st.title("🧠 SalesGPT - AI Sales Assistant with Memory")
st.markdown("*Powered by Hindsight - Never forget a conversation*")

# Sidebar - Prospect Selection
st.sidebar.header("Select Prospect")

prospects = [
    "Rajesh Kumar - TechCorp India",
    "Priya Sharma - StartupXYZ",
    "John Smith - BigEnterprise Corp",
    "Anita Desai - FinanceFlow Ltd",
    "Michael Chen - CloudScale"
]

selected_prospect = st.sidebar.selectbox(
    "Choose a prospect:",
    prospects
)

# Extract just the name
prospect_name = selected_prospect.split(" - ")[0]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Prospect:** {prospect_name}")
st.sidebar.markdown("The AI remembers ALL past conversations with this person!")

# New conversation button
if st.sidebar.button("Start Fresh Conversation"):
    st.session_state.conversation_history = []
    st.rerun()

# Main chat interface
st.header(f"Chat with {prospect_name}")

# Display conversation history
for message in st.session_state.conversation_history:
    if message['role'] == 'user':
        st.markdown(f"**You (Sales Rep):** {message['content']}")
    else:
        st.markdown(f"**🤖 SalesGPT:** {message['content']}")
    st.markdown("---")

# Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your message:",
        placeholder="E.g., Hi Rajesh, following up on our demo...",
        height=100
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.form_submit_button("Send 📤")
    
    if submit and user_input:
        # Add user message to history
        st.session_state.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get AI response
        with st.spinner("SalesGPT is thinking and checking memory..."):
            ai_response = st.session_state.agent.chat(prospect_name, user_input)
        
        # Add AI response to history
        st.session_state.conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        st.rerun()

# Show memory indicator
if len(st.session_state.conversation_history) > 0:
    st.sidebar.success(f"💾 {len(st.session_state.conversation_history)} messages in this session")