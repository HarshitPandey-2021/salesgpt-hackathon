import streamlit as st
from main import SalesGPT
from datetime import datetime
import time
import re

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="FlowSales AI - Smart Memory",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# FIXED CSS - PRODUCTION READY
# ============================================

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Keep header visible */
    button[kind="header"] {
        visibility: visible !important;
    }
    
    /* Main container */
    .block-container {
        padding: 1rem 1.5rem;
        max-width: 1200px;
    }
    
    /* ========================================== */
    /* SIDEBAR STYLING - FIXED THEME */
    /* ========================================== */
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        min-width: 320px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
    }
    
    /* Sidebar text colors - FIXED */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] span {
        color: #e0e0e0 !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 1rem 0;
    }
    
    /* ========================================== */
    /* CHAT ITEMS IN SIDEBAR */
    /* ========================================== */
    
    .chat-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        cursor: pointer;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .chat-item:hover {
        background: rgba(102, 126, 234, 0.15);
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .chat-item-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.5);
    }
    
    .chat-item-active * {
        color: white !important;
    }
    
    .chat-name {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.4rem;
        color: #ffffff;
    }
    
    .chat-preview {
        font-size: 0.85rem;
        opacity: 0.8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #e0e0e0;
    }
    
    .chat-meta {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.4rem;
        color: #b0b0b0;
    }
    
    /* ========================================== */
    /* SIDEBAR BUTTONS - FIXED */
    /* ========================================== */
    
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        background: rgba(102, 126, 234, 0.2);
        color: #ffffff !important;
        border: 1px solid rgba(102, 126, 234, 0.4);
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(102, 126, 234, 0.4);
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* ========================================== */
    /* SIDEBAR INFO BOX - FIXED */
    /* ========================================== */
    
    section[data-testid="stSidebar"] .stAlert {
        background: rgba(102, 126, 234, 0.1) !important;
        border-left: 3px solid #667eea !important;
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] .stAlert p,
    section[data-testid="stSidebar"] .stAlert strong {
        color: #ffffff !important;
    }
    
    /* ========================================== */
    /* MAIN AREA STYLING */
    /* ========================================== */
    
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* ========================================== */
    /* WELCOME CARD - FIXED VISIBILITY */
    /* ========================================== */
    
    .welcome-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-left: 5px solid #667eea;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .welcome-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1a1a2e !important;
        margin-bottom: 1rem;
    }
    
    .welcome-card p {
        color: #2d3748 !important;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0.75rem 0;
    }
    
    .welcome-card strong {
        color: #667eea !important;
        font-weight: 700;
    }
    
    /* ========================================== */
    /* MEMORY INDICATOR */
    /* ========================================== */
    
    .memory-pulse {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #fff8e1 0%, #ffe082 100%);
        border-left: 4px solid #ffa726;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #e65100 !important;
        margin: 0.5rem 0;
        font-weight: 600;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 2px 8px rgba(255, 167, 38, 0.2);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.85; transform: scale(1.02); }
    }
    
    /* ========================================== */
    /* QUICK REPLY BUTTONS */
    /* ========================================== */
    
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid #667eea;
        background: white;
        color: #667eea;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* ========================================== */
    /* CHAT MESSAGES */
    /* ========================================== */
    
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    }
    
    /* ========================================== */
    /* FOOTER */
    /* ========================================== */
    
    .footer-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_name_from_message(message):
    """Extract name from user message"""
    patterns = [
        r"i'?m\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"i am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"my name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"call me\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"this is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            return ' '.join(word.capitalize() for word in name.split())
    
    return None

def extract_company_from_message(message):
    """Extract company from user message"""
    patterns = [
        r"from\s+([A-Z][A-Za-z0-9\s&]+(?:Corp|Inc|LLC|Ltd|Company)?)",
        r"at\s+([A-Z][A-Za-z0-9\s&]+(?:Corp|Inc|LLC|Ltd|Company)?)",
        r"work at\s+([A-Z][A-Za-z0-9\s&]+)",
        r"company\s+(?:is\s+)?([A-Z][A-Za-z0-9\s&]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            company = re.sub(r'\s+', ' ', company)
            return company[:50]
    
    return None

def generate_chat_id():
    """Generate unique chat ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_suffix = str(time.time()).split('.')[-1][:4]
    return f"chat_{timestamp}_{random_suffix}"

def get_preview_text(messages):
    """Get preview text from last message"""
    if not messages:
        return "New conversation"
    
    last_msg = messages[-1]['content']
    preview = last_msg[:45] + "..." if len(last_msg) > 45 else last_msg
    return preview

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

# Initialize agent (ONE instance shared across all chats)
if 'agent' not in st.session_state:
    st.session_state.agent = SalesGPT()

# Initialize chats dictionary
if 'chats' not in st.session_state:
    st.session_state.chats = {}

# Initialize current chat
if 'current_chat_id' not in st.session_state:
    first_chat_id = generate_chat_id()
    st.session_state.chats[first_chat_id] = {
        'name': 'New Visitor',
        'company': None,
        'created_at': datetime.now(),
        'messages': [],
        'conversation_count': 0,
    }
    st.session_state.current_chat_id = first_chat_id

# Track if first message sent
if 'first_message_sent' not in st.session_state:
    st.session_state.first_message_sent = False

# ============================================
# SIDEBAR - CHAT MANAGEMENT
# ============================================

with st.sidebar:
    st.markdown("# 💬 FlowSales Chats")
    
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True, type="primary"):
        new_chat_id = generate_chat_id()
        st.session_state.chats[new_chat_id] = {
            'name': 'New Visitor',
            'company': None,
            'created_at': datetime.now(),
            'messages': [],
            'conversation_count': 0,
        }
        st.session_state.current_chat_id = new_chat_id
        st.session_state.first_message_sent = False
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📋 All Conversations")
    
    # Display all chats (most recent first)
    sorted_chats = sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1]['created_at'],
        reverse=True
    )
    
    if len(sorted_chats) == 0:
        st.info("No chats yet")
    else:
        for chat_id, chat_data in sorted_chats:
            is_active = (chat_id == st.session_state.current_chat_id)
            
            name = chat_data['name']
            company = chat_data.get('company', '')
            company_text = f" @ {company}" if company else ""
            preview = get_preview_text(chat_data['messages'])
            conv_count = chat_data['conversation_count']
            
            if is_active:
                # Active chat - show highlighted card
                st.markdown(f"""
                <div class='chat-item chat-item-active'>
                    <div class='chat-name'>✓ {name}{company_text}</div>
                    <div class='chat-preview'>{preview}</div>
                    <div class='chat-meta'>💬 {conv_count} messages</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Inactive chat - clickable button
                if st.button(
                    f"👤 {name}{company_text}",
                    key=f"chat_{chat_id}",
                    help=f"{preview} ({conv_count} messages)",
                    use_container_width=True
                ):
                    # SWITCH TO THIS CHAT
                    st.session_state.current_chat_id = chat_id
                    st.rerun()
    
    st.markdown("---")
    
    # Current chat info
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    st.markdown("### 🧠 Current Client")
    
    st.info(f"""
**Name:** {current_chat['name']}  
**Company:** {current_chat.get('company') or 'Not mentioned'}  
**Messages:** {current_chat['conversation_count']}
    """)
    
    # View memory button
    if current_chat['conversation_count'] > 0:
        if st.button("📋 View Memory", use_container_width=True):
            with st.spinner("🧠 Retrieving memories..."):
                try:
                    memories = st.session_state.agent.get_memory(st.session_state.current_chat_id)
                    if memories:
                        st.text_area("Memory:", memories, height=200, key="memory_display")
                    else:
                        st.info("Building memory...")
                except Exception as e:
                    st.warning(f"Memory loading... ({str(e)[:30]})")
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat_id]['messages'] = []
            st.session_state.chats[st.session_state.current_chat_id]['conversation_count'] = 0
            st.rerun()
    
    with col2:
        if len(st.session_state.chats) > 1:
            if st.button("🗑️ Delete", use_container_width=True):
                del st.session_state.chats[st.session_state.current_chat_id]
                st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                st.rerun()
    
    st.markdown("---")
    
    st.caption("🧠 Powered by Hindsight Memory")
    st.caption("⚡ Groq AI - Ultra Fast")
    st.caption(f"💬 {len(st.session_state.chats)} total chats")

# ============================================
# MAIN AREA - HEADER
# ============================================

current_chat = st.session_state.chats[st.session_state.current_chat_id]

st.markdown(f"""
<div class='app-header'>
    <div class='header-title'>💬 FlowSales AI Consultant</div>
    <div class='header-subtitle'>Chatting with: <strong>{current_chat['name']}</strong>{' @ ' + current_chat['company'] if current_chat.get('company') else ''}</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# WELCOME MESSAGE - FIXED VISIBILITY
# ============================================

if len(current_chat['messages']) == 0:
    st.markdown("""
    <div class='welcome-card'>
        <div class='welcome-title'>👋 Welcome! I'm your AI Sales Consultant</div>
        <p>I'll remember <strong>everything</strong> about you - your needs, budget, team size, and goals. The more we talk, the smarter I get about YOUR specific situation.</p>
        <p><strong>Just start chatting below!</strong> Use quick replies or type freely.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DISPLAY CHAT HISTORY
# ============================================

for message in current_chat['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"🕒 {message['timestamp']}")

# ============================================
# QUICK REPLY BUTTONS
# ============================================

if current_chat['conversation_count'] < 2:
    st.markdown("### 💡 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👋 Introduce Myself", use_container_width=True):
            st.session_state.quick_reply = "Hi! I'm looking to improve our sales process."
            st.rerun()
    
    with col2:
        if st.button("🎯 My Goal", use_container_width=True):
            st.session_state.quick_reply = "We need to close more deals faster."
            st.rerun()
    
    with col3:
        if st.button("💰 Budget Discussion", use_container_width=True):
            st.session_state.quick_reply = "What are the pricing options?"
            st.rerun()

# ============================================
# CHAT INPUT HANDLER - PERFECT MEMORY ISOLATION
# ============================================

# Check for quick reply
if 'quick_reply' in st.session_state:
    prompt = st.session_state.quick_reply
    del st.session_state.quick_reply
else:
    prompt = st.chat_input("💬 Type your message... (or use quick replies above)")

if prompt:
    st.session_state.first_message_sent = True
    
    # Extract name and company from first message
    if current_chat['conversation_count'] == 0:
        extracted_name = extract_name_from_message(prompt)
        extracted_company = extract_company_from_message(prompt)
        
        if extracted_name:
            current_chat['name'] = extracted_name
        if extracted_company:
            current_chat['company'] = extracted_company
    
    # Add user message
    user_msg = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime('%I:%M %p')
    }
    current_chat['messages'].append(user_msg)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕒 {user_msg['timestamp']}")
    
    # Get AI response (with perfect memory isolation)
    with st.chat_message("assistant"):
        # Show memory indicator if not first message
        if current_chat['conversation_count'] > 0:
            st.markdown("<div class='memory-pulse'>🧠 Recalling our previous conversations...</div>", unsafe_allow_html=True)
            time.sleep(0.8)
        
        with st.spinner("💭 Thinking..."):
            try:
                # CRITICAL: Pass current_chat_id to ensure memory isolation
                response = st.session_state.agent.chat(
                    user_id=st.session_state.current_chat_id,  # Unique per chat
                    user_message=prompt,
                    client_name=current_chat['name'],
                    client_company=current_chat.get('company')
                )
            except Exception as e:
                response = f"Oops! I had a hiccup. Can you say that again? 😅"
                st.error(f"Error: {str(e)}")
        
        st.markdown(response)
        st.caption(f"🕒 {datetime.now().strftime('%I:%M %p')}")
    
    # Add AI response
    ai_msg = {
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime('%I:%M %p')
    }
    current_chat['messages'].append(ai_msg)
    
    # Update conversation count
    current_chat['conversation_count'] += 1
    
    # Celebration at milestones
    if current_chat['conversation_count'] in [5, 10, 20]:
        st.balloons()
        st.success(f"🎉 Milestone: {current_chat['conversation_count']} messages! I know you really well now.")
    
    st.rerun()

# ============================================
# FOOTER
# ============================================

st.markdown("---")

st.markdown("""
<div class='footer-section'>
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;'>
        <div>
            <strong style='color: #667eea;'>🧠 Memory by</strong><br>
            <span style='color: #718096;'>Hindsight (Vectorize)</span>
        </div>
        <div>
            <strong style='color: #667eea;'>⚡ Powered by</strong><br>
            <span style='color: #718096;'>Groq AI</span>
        </div>
        <div>
            <strong style='color: #667eea;'>💬 Total Chats</strong><br>
            <span style='color: #718096;'>{} conversations</span>
        </div>
    </div>
</div>
""".format(len(st.session_state.chats)), unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.9rem; margin-top: 1.5rem; padding: 1rem;'>
    🏆 Built for Vectorize Hindsight Hackathon | Persistent Multi-Client Memory with Perfect Isolation
</div>
""", unsafe_allow_html=True)