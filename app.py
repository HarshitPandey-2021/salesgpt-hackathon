import streamlit as st
from main import SalesGPT
from datetime import datetime
import time
import os
import json

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="FlowSales AI ✨",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD EXTERNAL CSS
# ============================================

def load_css(file_name):
    """Load CSS from external file"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('styles.css')

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
    return last_msg[:35] + "..." if len(last_msg) > 35 else last_msg

def get_stage_display(stage):
    """Get stage display info"""
    stages = {
        "welcome": {"icon": "👋", "name": "Welcome"},
        "discovery": {"icon": "🔍", "name": "Discovery"},
        "understanding": {"icon": "🎯", "name": "Understanding"},
        "recommendation": {"icon": "💡", "name": "Recommendation"}
    }
    return stages.get(stage, stages["welcome"])

def save_memory():
    """Save memory to JSON file (persistent across refreshes)"""
    chats_to_save = {}
    for chat_id, chat_data in st.session_state.chats.items():
        chats_to_save[chat_id] = {
            'name': chat_data['name'],
            'company': chat_data.get('company'),
            'created_at': chat_data['created_at'].isoformat() if isinstance(chat_data['created_at'], datetime) else chat_data['created_at'],
            'messages': chat_data['messages'],
            'conversation_count': chat_data['conversation_count'],
            'profile': chat_data.get('profile', {})
        }
    
    data = {
        "chats": chats_to_save,
        "current_chat_id": st.session_state.current_chat_id
    }
    
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=2)

def load_memory():
    """Load memory from JSON file"""
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r") as f:
                saved = json.load(f)
                
                chats = {}
                for chat_id, chat_data in saved.get("chats", {}).items():
                    try:
                        created_at = datetime.fromisoformat(chat_data['created_at']) if isinstance(chat_data['created_at'], str) else chat_data['created_at']
                    except:
                        created_at = datetime.now()
                    
                    chats[chat_id] = {
                        'name': chat_data['name'],
                        'company': chat_data.get('company'),
                        'created_at': created_at,
                        'messages': chat_data.get('messages', []),
                        'conversation_count': chat_data.get('conversation_count', 0),
                        'profile': chat_data.get('profile', {})
                    }
                
                return chats, saved.get("current_chat_id")
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {}, None
    return {}, None

# ============================================
# SESSION STATE - WITH PERSISTENCE
# ============================================

if 'agent' not in st.session_state:
    st.session_state.agent = SalesGPT()

if 'chats' not in st.session_state:
    loaded_chats, loaded_chat_id = load_memory()
    st.session_state.chats = loaded_chats
    st.session_state.current_chat_id = loaded_chat_id

if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# ============================================
# ONBOARDING
# ============================================

def show_onboarding():
    """Show onboarding form"""
    st.markdown("""
    <div class='onboarding-container'>
        <div class='onboarding-title'>🚀 Welcome to FlowSales AI ✨</div>
        <div class='onboarding-subtitle'>Your AI sales consultant that never forgets</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("onboarding_form", clear_on_submit=True):
        st.markdown("### 📋 Let's get started")
        
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
        
        submitted = st.form_submit_button("🚀 Start Journey", use_container_width=True, type="primary")
        
        if submitted:
            if name and company:
                chat_id = generate_chat_id()
                
                profile_data = {
                    "name": name,
                    "company": company,
                    "team_size": team_size,
                    "goal": goal
                }
                
                st.session_state.agent.save_profile(chat_id, profile_data)
                
                st.session_state.chats[chat_id] = {
                    'name': name,
                    'company': company,
                    'created_at': datetime.now(),
                    'messages': [],
                    'conversation_count': 0,
                    'profile': profile_data
                }
                
                st.session_state.current_chat_id = chat_id
                
                save_memory()
                
                st.success(f"✅ Welcome {name}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill all required fields")

# ============================================
# MAIN APP
# ============================================

if not st.session_state.current_chat_id or len(st.session_state.chats) == 0:
    show_onboarding()
else:
    # ============================================
    # SIDEBAR - COMPACT, NO SCROLL
    # ============================================
    
    with st.sidebar:
        st.markdown("# 🚀 FlowSales")
        st.caption("AI that never forgets")
        
        st.markdown("---")
        
        if st.button("➕ New Client", key="new_chat", use_container_width=True, type="primary"):
            st.session_state.current_chat_id = None
            save_memory()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💼 Clients")
        
        sorted_chats = sorted(
            st.session_state.chats.items(),
            key=lambda x: x[1]['created_at'],
            reverse=True
        )
        
        for chat_id, chat_data in sorted_chats[:5]:
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
                    <div class='chat-meta'>💬 {conv_count} msgs</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(
                    f"👤 {name}{company_text}",
                    key=f"chat_{chat_id}",
                    use_container_width=True
                ):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.show_summary = False
                    save_memory()
                    st.rerun()
        
        st.markdown("---")
        
        current_chat = st.session_state.chats[st.session_state.current_chat_id]
        
        st.markdown("### 🧠 Profile")
        
        profile = current_chat.get('profile', {})
        if not profile:
            profile = st.session_state.agent.get_profile(st.session_state.current_chat_id)
        
        st.info(f"""
**{current_chat['name']}**  
📍 {current_chat.get('company', 'N/A')}  
👥 {profile.get('team_size', 'Unknown')}  
🎯 {profile.get('goal', 'Unknown')}  
💬 {current_chat['conversation_count']} msgs
        """)
        
        if st.button("🧠 Summary", use_container_width=True):
            st.session_state.show_summary = True
            st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄", use_container_width=True, help="Clear"):
                st.session_state.chats[st.session_state.current_chat_id]['messages'] = []
                st.session_state.chats[st.session_state.current_chat_id]['conversation_count'] = 0
                save_memory()
                st.rerun()
        
        with col2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑️", use_container_width=True, help="Delete"):
                    del st.session_state.chats[st.session_state.current_chat_id]
                    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                    save_memory()
                    st.rerun()
        
        st.markdown("---")
        st.caption("🧠 Hindsight • ⚡ Groq")
        st.caption(f"💬 {len(st.session_state.chats)} clients")
    
    # ============================================
    # MAIN AREA
    # ============================================
    
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # STICKY HEADER
    st.markdown(f"""
    <div class='app-header'>
        <div class='header-title'>FlowSales AI ✨</div>
        <div class='header-subtitle'>With <strong>{current_chat['name']}</strong> @ {current_chat.get('company', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # SUMMARY MODAL
    if st.session_state.show_summary:
        summary = st.session_state.agent.generate_summary(st.session_state.current_chat_id)
        
        st.markdown(f"""
        <div class='glass-card'>
        {summary.replace('#', '###')}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✖️ Close"):
            st.session_state.show_summary = False
            st.rerun()
        
        st.markdown("---")
    
    # STAGE
    conv_count = current_chat['conversation_count']
    stage = st.session_state.agent.get_conversation_stage(conv_count)
    stage_info = get_stage_display(stage)
    
    st.markdown(f"""
    <div class='stage-indicator'>
        <div class='stage-icon'>{stage_info['icon']}</div>
        <div class='stage-text'>
            <div class='stage-label'>Stage</div>
            <div class='stage-name'>{stage_info['name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # MEMORY TIMELINE
    if conv_count > 0:
        confidence = st.session_state.agent.get_memory_confidence(st.session_state.current_chat_id)
        profile = current_chat.get('profile', {})
        if not profile:
            profile = st.session_state.agent.get_profile(st.session_state.current_chat_id)
        extracted = st.session_state.agent.get_extracted_info(st.session_state.current_chat_id)
        
        items = []
        if profile.get('name'): items.append(f"✓ {profile['name']}")
        if profile.get('company'): items.append(f"✓ @ {profile['company']}")
        if profile.get('team_size'): items.append(f"✓ Team: {profile['team_size']}")
        if profile.get('goal'): items.append(f"✓ Goal: {profile['goal']}")
        if extracted.get('budget'): items.append(f"✓ Budget: {extracted['budget']}")
        
        if items:
            items_html = "\n".join([f"<div class='memory-item'>{i}</div>" for i in items])
            
            st.markdown(f"""
            <div class='memory-timeline'>
                <div class='memory-title'>🧠 Memory</div>
                {items_html}
                <div class='memory-confidence'>
                    <div style='font-size: 0.7rem; color: #fde047; font-weight: 600;'>Confidence: {confidence}%</div>
                    <div class='confidence-bar'>
                        <div class='confidence-fill' style='width: {confidence}%;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # INSIGHTS
    if conv_count > 1:
        insights = st.session_state.agent.generate_insights(st.session_state.current_chat_id)
        if insights:
            insights_html = "\n".join([f"<div class='insight-item'>{i}</div>" for i in insights])
            
            st.markdown(f"""
            <div class='insights-box'>
                <div class='insights-title'>💡 Insights</div>
                {insights_html}
            </div>
            """, unsafe_allow_html=True)
    
    # CHAT MESSAGES
    for msg in current_chat['messages']:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "timestamp" in msg:
                st.caption(f"🕒 {msg['timestamp']}")
    
    # QUICK ACTIONS
    if conv_count < 2:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Improve Sales", use_container_width=True):
                st.session_state.quick_reply = "I want to improve sales performance."
                st.rerun()
        
        with col2:
            if st.button("🤖 Automate", use_container_width=True):
                st.session_state.quick_reply = "We need automation."
                st.rerun()
        
        with col3:
            if st.button("💰 Pricing", use_container_width=True):
                st.session_state.quick_reply = "What's your pricing?"
                st.rerun()
    
    elif conv_count >= 3:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📅 Demo", use_container_width=True):
                st.session_state.quick_reply = "Book a demo."
                st.rerun()
        
        with col2:
            if st.button("💰 ROI", use_container_width=True):
                st.session_state.quick_reply = "Calculate ROI."
                st.rerun()
        
        with col3:
            if st.button("⚙️ Setup", use_container_width=True):
                st.session_state.quick_reply = "How to implement?"
                st.rerun()
        
        with col4:
            if st.button("🔗 CRM", use_container_width=True):
                st.session_state.quick_reply = "CRM integration?"
                st.rerun()
    
    
    # CHAT INPUT (Fixed at bottom)
    if 'quick_reply' in st.session_state:
        prompt = st.session_state.quick_reply
        del st.session_state.quick_reply
    else:
        prompt = st.chat_input("Ask me anything about improving your sales 🚀")
    
    if prompt:
        user_msg = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime('%I:%M %p')
        }
        current_chat['messages'].append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕒 {user_msg['timestamp']}")
        
        with st.chat_message("assistant"):
            if conv_count > 0:
                st.markdown("<div class='memory-pulse'>🧠 Recalling conversations...</div>", unsafe_allow_html=True)
                time.sleep(0.5)
                with st.spinner("💡 Generating personalized response..."):
                    time.sleep(0.4)
            
            try:
                response = st.session_state.agent.chat(
                    user_id=st.session_state.current_chat_id,
                    user_message=prompt,
                    client_name=current_chat['name'],
                    conversation_stage=stage
                )
            except Exception as e:
                response = "Brief hiccup - try again? 😅"
                st.error(f"{str(e)}")
            
            st.markdown(response)
            st.caption(f"🕒 {datetime.now().strftime('%I:%M %p')}")
        
        ai_msg = {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime('%I:%M %p')
        }
        current_chat['messages'].append(ai_msg)
        current_chat['conversation_count'] += 1
        
        save_memory()
        
        if current_chat['conversation_count'] in [5, 10, 20]:
            st.balloons()
            st.success(f"🎉 {current_chat['conversation_count']} messages!")
        
        st.rerun()
        
        
        
    # FOOTER - POSITIONED CORRECTLY
    st.markdown("""
    <div class='footer-container'>
        <div class='footer-grid'>
            <div class='footer-item'>
                <strong>🧠 Memory</strong>
                <span>Hindsight</span>
            </div>
            <div class='footer-item'>
                <strong>⚡ AI</strong>
                <span>Groq</span>
            </div>
            <div class='footer-item'>
                <strong>💬 Clients</strong>
                <span>{}</span>
            </div>
        </div>
        <div class='footer-credit'>🏆 Built for Agent Memory Hackathon</div>
    </div>
    """.format(len(st.session_state.chats)), unsafe_allow_html=True)