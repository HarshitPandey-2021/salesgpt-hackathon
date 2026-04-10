import streamlit as st
from main import SalesGPT
from datetime import datetime
import time
import re

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="FlowSales AI - Winner Edition",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PRODUCTION CSS
# ============================================

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: visible !important;}
    
    /* Fix navbar overlap */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }
    
    /* ========================================== */
    /* SIDEBAR */
    /* ========================================== */
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f36 0%, #0f1419 100%) !important;
        min-width: 340px !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 1.2rem 0;
    }
    
    /* Chat items */
    .chat-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border: 2px solid rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .chat-item:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: #6366f1;
        transform: translateX(5px);
    }
    
    .chat-item-active {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-color: #6366f1;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    .chat-name {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.4rem;
        color: #ffffff;
    }
    
    .chat-preview {
        font-size: 0.85rem;
        opacity: 0.85;
        color: #e0e0e0;
    }
    
    .chat-meta {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.4rem;
        color: #b0b0b0;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.2);
        color: #ffffff !important;
        border: 1px solid rgba(99, 102, 241, 0.4);
        transition: all 0.3s;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
    }
    
    /* ========================================== */
    /* ONBOARDING FORM */
    /* ========================================== */
    
    .onboarding-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 2.5rem;
        max-width: 600px;
        margin: 2rem auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .onboarding-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .onboarding-subtitle {
        font-size: 1.1rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* ========================================== */
    /* MAIN HEADER */
    /* ========================================== */
    
    .app-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* ========================================== */
    /* STAGE INDICATOR */
    /* ========================================== */
    
    .stage-indicator {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0284c7;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .stage-icon {
        font-size: 1.5rem;
    }
    
    .stage-text {
        flex: 1;
    }
    
    .stage-label {
        font-size: 0.85rem;
        color: #0369a1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stage-name {
        font-size: 1.1rem;
        color: #0c4a6e;
        font-weight: 700;
        margin-top: 0.2rem;
    }
    
    /* ========================================== */
    /* MEMORY TIMELINE */
    /* ========================================== */
    
    .memory-timeline {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border-left: 4px solid #eab308;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .memory-title {
        font-size: 1rem;
        font-weight: 700;
        color: #854d0e;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .memory-item {
        font-size: 0.9rem;
        color: #713f12;
        margin: 0.4rem 0;
        padding-left: 1rem;
    }
    
    .memory-confidence {
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(234, 179, 8, 0.3);
    }
    
    .confidence-bar {
        background: rgba(234, 179, 8, 0.2);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #eab308 0%, #ca8a04 100%);
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* ========================================== */
    /* INSIGHTS BOX */
    /* ========================================== */
    
    .insights-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .insights-title {
        font-size: 1rem;
        font-weight: 700;
        color: #166534;
        margin-bottom: 0.8rem;
    }
    
    .insight-item {
        font-size: 0.9rem;
        color: #15803d;
        margin: 0.5rem 0;
        padding-left: 0.5rem;
    }
    
    /* ========================================== */
    /* BUTTONS */
    /* ========================================== */
    
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 2px solid #6366f1;
        background: white;
        color: #6366f1;
        transition: all 0.3s;
        padding: 0.75rem 1.5rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* ========================================== */
    /* MEMORY PULSE */
    /* ========================================== */
    
    .memory-pulse {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #92400e !important;
        margin: 0.5rem 0;
        font-weight: 600;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    /* ========================================== */
    /* FOOTER */
    /* ========================================== */
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 2rem;
        text-align: center;
    }
    
    .footer-item strong {
        color: #6366f1;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .footer-item span {
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_chat_id():
    """Generate unique chat ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_suffix = str(time.time()).split('.')[-1][:4]
    return f"chat_{timestamp}_{random_suffix}"

def get_preview_text(messages):
    """Get preview text"""
    if not messages:
        return "New conversation"
    last_msg = messages[-1]['content']
    return last_msg[:45] + "..." if len(last_msg) > 45 else last_msg

def get_stage_display(stage):
    """Get stage display info"""
    stages = {
        "welcome": {"icon": "👋", "name": "Welcome", "color": "#10b981"},
        "discovery": {"icon": "🔍", "name": "Discovery", "color": "#3b82f6"},
        "understanding": {"icon": "🎯", "name": "Understanding", "color": "#8b5cf6"},
        "recommendation": {"icon": "💡", "name": "Recommendation", "color": "#f59e0b"}
    }
    return stages.get(stage, stages["welcome"])

# ============================================
# SESSION STATE
# ============================================

if 'agent' not in st.session_state:
    st.session_state.agent = SalesGPT()

if 'chats' not in st.session_state:
    st.session_state.chats = {}

if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None

if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# ============================================
# ONBOARDING FLOW (UPGRADE #1)
# ============================================

def show_onboarding():
    """Show onboarding form"""
    st.markdown("""
    <div class='onboarding-container'>
        <div class='onboarding-title'>🚀 Welcome to FlowSales AI</div>
        <div class='onboarding-subtitle'>Let's personalize your experience (takes 30 seconds)</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("onboarding_form", clear_on_submit=True):
        st.markdown("### 📋 Tell us about yourself")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name *", placeholder="John Doe")
            company = st.text_input("Company *", placeholder="Acme Corp")
        
        with col2:
            team_size = st.selectbox(
                "Team Size *",
                ["1-5 people", "5-10 people", "10-20 people", "20-50 people", "50+ people"]
            )
            
            goal = st.selectbox(
                "Primary Goal *",
                [
                    "Close more deals",
                    "Automate follow-ups",
                    "Generate more leads",
                    "Track deals better",
                    "Improve response time"
                ]
            )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("🚀 Start My Journey", use_container_width=True, type="primary")
        
        if submitted:
            if name and company:
                # Create new chat with profile
                chat_id = generate_chat_id()
                
                profile_data = {
                    "name": name,
                    "company": company,
                    "team_size": team_size,
                    "goal": goal
                }
                
                # Save profile to Hindsight
                st.session_state.agent.save_profile(chat_id, profile_data)
                
                # Create chat
                st.session_state.chats[chat_id] = {
                    'name': name,
                    'company': company,
                    'created_at': datetime.now(),
                    'messages': [],
                    'conversation_count': 0,
                    'profile': profile_data
                }
                
                st.session_state.current_chat_id = chat_id
                st.success(f"✅ Welcome {name}! Let's get started.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

# ============================================
# MAIN APP
# ============================================

# Check if onboarding needed
if not st.session_state.current_chat_id or len(st.session_state.chats) == 0:
    show_onboarding()
else:
    # ============================================
    # SIDEBAR
    # ============================================
    
    with st.sidebar:
        st.markdown("# 🏆 FlowSales AI")
        st.markdown("### Multi-Client Sales Consultant")
        
        st.markdown("---")
        
        # New Chat Button
        if st.button("➕ Start New Client", key="new_chat_btn", use_container_width=True, type="primary"):
            st.session_state.current_chat_id = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 All Clients")
        
        # Display chats
        sorted_chats = sorted(
            st.session_state.chats.items(),
            key=lambda x: x[1]['created_at'],
            reverse=True
        )
        
        for chat_id, chat_data in sorted_chats:
            is_active = (chat_id == st.session_state.current_chat_id)
            
            name = chat_data['name']
            company = chat_data.get('company', '')
            company_text = f" @ {company}" if company else ""
            preview = get_preview_text(chat_data['messages'])
            conv_count = chat_data['conversation_count']
            
            if is_active:
                st.markdown(f"""
                <div class='chat-item chat-item-active'>
                    <div class='chat-name'>✓ {name}{company_text}</div>
                    <div class='chat-preview'>{preview}</div>
                    <div class='chat-meta'>💬 {conv_count} messages</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(
                    f"👤 {name}{company_text}",
                    key=f"chat_{chat_id}",
                    help=f"{preview}",
                    use_container_width=True
                ):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.show_summary = False
                    st.rerun()
        
        st.markdown("---")
        
        # Current client info
        current_chat = st.session_state.chats[st.session_state.current_chat_id]
        
        st.markdown("### 🧠 Current Client")
        
        # Get profile and insights
        profile = st.session_state.agent.get_profile(st.session_state.current_chat_id)
        
        info_text = f"""
**Name:** {current_chat['name']}  
**Company:** {current_chat.get('company', 'N/A')}  
**Team:** {profile.get('team_size', 'Unknown')}  
**Goal:** {profile.get('goal', 'Unknown')}  
**Messages:** {current_chat['conversation_count']}
"""
        
        st.info(info_text)
        
        # UPGRADE #5: "What I Know About You" button
        if st.button("🧠 What I Know About You", use_container_width=True):
            st.session_state.show_summary = True
            st.rerun()
        
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
        st.caption("⚡ Groq AI - llama-3.3-70b")
        st.caption(f"💬 {len(st.session_state.chats)} active clients")
    
    # ============================================
    # MAIN AREA
    # ============================================
    
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # Header
    st.markdown(f"""
    <div class='app-header'>
        <div class='header-title'>🏆 FlowSales AI - Winner Edition</div>
        <div class='header-subtitle'>Intelligent sales automation with evolving memory • Currently with: <strong>{current_chat['name']}</strong> @ {current_chat.get('company', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show summary if requested (UPGRADE #5)
    if st.session_state.show_summary:
        summary = st.session_state.agent.generate_summary(st.session_state.current_chat_id)
        st.markdown(summary)
        
        if st.button("✖️ Close Summary"):
            st.session_state.show_summary = False
            st.rerun()
        
        st.markdown("---")
    
    # Conversation stage
    conv_count = current_chat['conversation_count']
    stage = st.session_state.agent.get_conversation_stage(conv_count)
    stage_info = get_stage_display(stage)
    
    st.markdown(f"""
    <div class='stage-indicator'>
        <div class='stage-icon'>{stage_info['icon']}</div>
        <div class='stage-text'>
            <div class='stage-label'>Conversation Stage</div>
            <div class='stage-name'>{stage_info['name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Memory Timeline
    if conv_count > 0:
        confidence = st.session_state.agent.get_memory_confidence(st.session_state.current_chat_id)
        profile = st.session_state.agent.get_profile(st.session_state.current_chat_id)
        extracted = st.session_state.agent.get_extracted_info(st.session_state.current_chat_id)
        
        memory_items = []
        if profile.get('name'):
            memory_items.append(f"✓ Name: {profile['name']}")
        if profile.get('company'):
            memory_items.append(f"✓ Company: {profile['company']}")
        if profile.get('team_size'):
            memory_items.append(f"✓ Team: {profile['team_size']}")
        if profile.get('goal'):
            memory_items.append(f"✓ Goal: {profile['goal']}")
        if extracted.get('budget'):
            memory_items.append(f"✓ Budget: {extracted['budget']}")
        if extracted.get('pain_points'):
            memory_items.append(f"✓ Pain Points: {extracted['pain_points']}")
        
        if memory_items:
            memory_html = "\n".join([f"<div class='memory-item'>{item}</div>" for item in memory_items])
            
            st.markdown(f"""
            <div class='memory-timeline'>
                <div class='memory-title'>🧠 What I've Learned</div>
                {memory_html}
                <div class='memory-confidence'>
                    <div style='font-size: 0.85rem; color: #854d0e; font-weight: 600;'>Memory Confidence: {confidence}%</div>
                    <div class='confidence-bar'>
                        <div class='confidence-fill' style='width: {confidence}%;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Insights Box (UPGRADE #3)
    if conv_count > 1:
        insights = st.session_state.agent.generate_insights(st.session_state.current_chat_id)
        if insights:
            insights_html = "\n".join([f"<div class='insight-item'>{insight}</div>" for insight in insights])
            
            st.markdown(f"""
            <div class='insights-box'>
                <div class='insights-title'>💡 AI Insights</div>
                {insights_html}
            </div>
            """, unsafe_allow_html=True)
    
    # Display chat history
    for message in current_chat['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"🕒 {message['timestamp']}")
    
    # Quick actions
    if conv_count < 2:
        st.markdown("### 💡 Quick Start")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Improve Performance", use_container_width=True):
                st.session_state.quick_reply = "I want to improve our sales performance."
                st.rerun()
        
        with col2:
            if st.button("🤖 Automate Follow-ups", use_container_width=True):
                st.session_state.quick_reply = "We need to automate follow-ups."
                st.rerun()
        
        with col3:
            if st.button("💰 Pricing Options", use_container_width=True):
                st.session_state.quick_reply = "What's your pricing?"
                st.rerun()
    
    elif conv_count >= 3:
        st.markdown("### ⚡ Smart Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📅 Book Demo", use_container_width=True):
                st.session_state.quick_reply = "I'd like to book a demo."
                st.rerun()
        
        with col2:
            if st.button("💰 Calculate ROI", use_container_width=True):
                st.session_state.quick_reply = "Help me calculate ROI for my team."
                st.rerun()
        
        with col3:
            if st.button("⚙️ Implementation", use_container_width=True):
                st.session_state.quick_reply = "How does implementation work?"
                st.rerun()
        
        with col4:
            if st.button("🔗 Integration", use_container_width=True):
                st.session_state.quick_reply = "How does it integrate with our CRM?"
                st.rerun()
    
    # Chat input
    if 'quick_reply' in st.session_state:
        prompt = st.session_state.quick_reply
        del st.session_state.quick_reply
    else:
        prompt = st.chat_input("💬 Type your message...")
    
    if prompt:
        # Add user message
        user_msg = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime('%I:%M %p')
        }
        current_chat['messages'].append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕒 {user_msg['timestamp']}")
        
        # Get AI response
        with st.chat_message("assistant"):
            if conv_count > 0:
                st.markdown("<div class='memory-pulse'>🧠 Accessing conversation history and insights...</div>", unsafe_allow_html=True)
                time.sleep(0.8)
            
            with st.spinner("💭 Thinking with memory..."):
                try:
                    response = st.session_state.agent.chat(
                        user_id=st.session_state.current_chat_id,
                        user_message=prompt,
                        client_name=current_chat['name'],
                        conversation_stage=stage
                    )
                except Exception as e:
                    response = f"I had a brief hiccup - can you say that again? 😅"
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
        current_chat['conversation_count'] += 1
        
        # Milestones
        if current_chat['conversation_count'] in [5, 10, 20]:
            st.balloons()
            st.success(f"🎉 Milestone: {current_chat['conversation_count']} messages!")
        
        st.rerun()
    
    # Footer
    st.markdown("---")
    
    st.markdown(f"""
    <div class='footer-grid'>
        <div class='footer-item'>
            <strong>🧠 Memory Tech</strong>
            <span>Hindsight by Vectorize</span>
        </div>
        <div class='footer-item'>
            <strong>⚡ AI Engine</strong>
            <span>Groq - llama-3.3-70b</span>
        </div>
        <div class='footer-item'>
            <strong>💬 Active Clients</strong>
            <span>{len(st.session_state.chats)} conversations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 1.5rem;'>
        🏆 Built for Vectorize Hindsight Hackathon | Production-Grade Evolving Memory System
    </div>
    """, unsafe_allow_html=True)