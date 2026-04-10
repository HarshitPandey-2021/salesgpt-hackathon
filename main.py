import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from openai import OpenAI
from datetime import datetime, timedelta
import random
from functools import lru_cache
import re

# Load environment variables
load_dotenv()

# API Keys
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Global clients
_hindsight_client = None
_llm_client = None

@lru_cache(maxsize=1)
def get_hindsight_client():
    """Get or create Hindsight client (cached)"""
    global _hindsight_client
    if _hindsight_client is None:
        import asyncio
        import warnings
        
        # Suppress specific async warnings from Hindsight library
        warnings.filterwarnings("ignore", message=".*coroutine.*")
        warnings.filterwarnings("ignore", message=".*Timeout.*")
        
        _hindsight_client = Hindsight(
            base_url="https://api.hindsight.vectorize.io",
            api_key=HINDSIGHT_API_KEY
        )
    return _hindsight_client

@lru_cache(maxsize=1)
def get_llm_client():
    """Get or create LLM client (cached)"""
    global _llm_client
    if _llm_client is None:
        _llm_client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
    return _llm_client


class SalesGPT:
    def __init__(self, bank_id="flowsales-winner-v1"):
        """
        Initialize SalesGPT with Hindsight memory
        """
        self.bank_id = bank_id
        
        # Create memory bank if it doesn't exist
        try:
            client = get_hindsight_client()
            client.create_bank(
                bank_id=self.bank_id,
                name="FlowSales Winner Memory Bank"
            )
            print(f"✅ Memory bank ready: {self.bank_id}")
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower() or "bank_id" in error_msg.lower():
                print(f"ℹ️ Memory bank exists: {self.bank_id}")
            else:
                print(f"⚠️ Bank note: {error_msg[:80]}")
    
    def save_profile(self, user_id, profile_data):
        """
        Save user profile from onboarding (UPGRADE #1)
        """
        try:
            client = get_hindsight_client()
            
            # Create rich profile content
            profile_content = f"""
[USER_ID:{user_id}] [PROFILE_DATA]

Name: {profile_data.get('name', 'Unknown')}
Company: {profile_data.get('company', 'Unknown')}
Team Size: {profile_data.get('team_size', 'Unknown')}
Primary Goal: {profile_data.get('goal', 'Unknown')}

Profile created at: {datetime.now().strftime('%B %d, %Y')}
"""
            
            metadata = {
                "user_id": user_id,
                "type": "profile",
                "name": profile_data.get('name'),
                "company": profile_data.get('company'),
                "team_size": profile_data.get('team_size'),
                "goal": profile_data.get('goal'),
                "created_at": datetime.now().isoformat()
            }
            
            client.retain(
                bank_id=self.bank_id,
                content=profile_content,
                metadata=metadata
            )
            
            print(f"✅ Profile saved for {profile_data.get('name')} (ID: {user_id})")
            return True
            
        except Exception as e:
            print(f"⚠️ Profile save note: {str(e)[:80]}")
            return False
    
    def save_to_memory(self, user_id, conversation_text, client_name=None, extracted_data=None):
        """
        Save conversation with evolution tracking (UPGRADE #2)
        """
        try:
            client = get_hindsight_client()
            
            # Simulate time progression for demo (UPGRADE #6)
            # Makes it feel like long-term memory
            simulated_time = datetime.now() - timedelta(days=random.randint(0, 3))
            
            # Build enriched content
            data_summary = ""
            if extracted_data:
                updates = []
                for key, value in extracted_data.items():
                    updates.append(f"{key}: {value}")
                data_summary = f"\n[UPDATED: {', '.join(updates)}]"
            
            tagged_content = f"[USER_ID:{user_id}] [CLIENT:{client_name or 'Unknown'}]{data_summary} {conversation_text}"
            
            # Enhanced metadata with update tracking
            metadata = {
                "user_id": user_id,
                "timestamp": simulated_time.isoformat(),
                "type": "conversation",
                "updated_at": datetime.now().isoformat()
            }
            
            if client_name:
                metadata["client_name"] = client_name
            
            if extracted_data:
                metadata.update(extracted_data)
                # Track when data was updated
                for key in extracted_data.keys():
                    metadata[f"{key}_updated_at"] = datetime.now().isoformat()
            
            client.retain(
                bank_id=self.bank_id,
                content=tagged_content,
                metadata=metadata
            )
            
            print(f"💾 Memory saved for {client_name or user_id}")
            return True
            
        except Exception as e:
            print(f"⚠️ Memory save note: {str(e)[:80]}")
            return False
    
    def get_memory(self, user_id):
        """
        Retrieve conversation history ONLY for specific user_id
        """
        try:
            client = get_hindsight_client()
            
            result = client.recall(
                bank_id=self.bank_id,
                query=f"USER_ID:{user_id} - complete history, profile, preferences, goals, budget, team, decisions, objections, concerns"
            )
            
            if result.results:
                # Filter by user_id
                filtered_memories = [
                    memory for memory in result.results
                    if f"USER_ID:{user_id}" in memory.text
                ]
                
                if not filtered_memories:
                    return ""
                
                # Get top 20 memories
                memories = filtered_memories[:20]
                
                memory_text = "\n".join([
                    f"- {memory.text.replace(f'[USER_ID:{user_id}]', '').replace(f'[CLIENT:', '[')}"
                    for memory in memories
                ])
                
                print(f"🧠 Retrieved {len(memories)} memories for {user_id}")
                return memory_text
            else:
                return ""
                
        except Exception as e:
            print(f"⚠️ Memory retrieval note: {str(e)[:80]}")
            return ""
    
    def get_profile(self, user_id):
        """
        Get structured profile data
        """
        memories = self.get_memory(user_id)
        if not memories:
            return {}
        
        profile = {}
        
        # Extract profile data
        if "Name:" in memories:
            match = re.search(r'Name:\s*([^\n]+)', memories)
            if match:
                profile['name'] = match.group(1).strip()
        
        if "Company:" in memories:
            match = re.search(r'Company:\s*([^\n]+)', memories)
            if match:
                profile['company'] = match.group(1).strip()
        
        if "Team Size:" in memories:
            match = re.search(r'Team Size:\s*([^\n]+)', memories)
            if match:
                profile['team_size'] = match.group(1).strip()
        
        if "Primary Goal:" in memories or "Goal:" in memories:
            match = re.search(r'(?:Primary )?Goal:\s*([^\n]+)', memories)
            if match:
                profile['goal'] = match.group(1).strip()
        
        return profile
    
    def get_extracted_info(self, user_id):
        """
        Extract and track evolving information (UPGRADE #2)
        """
        memories = self.get_memory(user_id)
        if not memories:
            return {}
        
        info = {}
        
        # Extract team size with update tracking
        team_matches = re.findall(r'(\d+)\s*(?:people|reps|members|team)', memories, re.IGNORECASE)
        if team_matches:
            info['team_size'] = team_matches[0]  # Most recent
            if len(team_matches) > 1:
                info['team_size_changed'] = True  # Track if it evolved
        
        # Extract budget signals
        budget_keywords = {
            'limited': ['small', 'tight', 'limited', 'low'],
            'mid-range': ['medium', 'moderate', 'reasonable'],
            'enterprise': ['large', 'big', 'enterprise', 'unlimited']
        }
        
        memories_lower = memories.lower()
        for budget_type, keywords in budget_keywords.items():
            if any(kw in memories_lower for kw in keywords):
                info['budget'] = budget_type.title()
                break
        
        # Extract goals (multiple possible)
        goals = []
        if 'automat' in memories_lower:
            goals.append('automation')
        if 'close' in memories_lower or 'deal' in memories_lower:
            goals.append('close deals')
        if 'lead' in memories_lower:
            goals.append('generate leads')
        if 'follow' in memories_lower:
            goals.append('follow-ups')
        
        if goals:
            info['goals'] = ', '.join(set(goals))
        
        # Extract pain points
        pain_points = []
        if 'manual' in memories_lower:
            pain_points.append('manual processes')
        if 'slow' in memories_lower:
            pain_points.append('slow response times')
        if 'track' in memories_lower:
            pain_points.append('tracking issues')
        
        if pain_points:
            info['pain_points'] = ', '.join(set(pain_points))
        
        return info
    
    def generate_insights(self, user_id):
        """
        UPGRADE #3: Generate insights from memory
        """
        memories = self.get_memory(user_id)
        profile = self.get_profile(user_id)
        extracted = self.get_extracted_info(user_id)
        
        if not memories:
            return []
        
        insights = []
        
        # Insight 1: Team size insight
        if 'team_size' in extracted:
            team_size = int(extracted['team_size']) if extracted['team_size'].isdigit() else 0
            if team_size < 5:
                insights.append(f"💡 Small team ({team_size}) → High automation ROI potential")
            elif team_size > 10:
                insights.append(f"💡 Large team ({team_size}) → Enterprise features recommended")
        
        # Insight 2: Goal alignment
        if 'goal' in profile:
            goal = profile['goal'].lower()
            if 'automat' in goal:
                insights.append("🎯 Automation focus detected → Follow-up sequences are key")
            elif 'close' in goal or 'deal' in goal:
                insights.append("🎯 Deal closing focus → Pipeline tracking is priority")
        
        # Insight 3: Budget fit
        if 'budget' in extracted:
            budget = extracted['budget'].lower()
            if 'limited' in budget:
                insights.append("💰 Budget-conscious → Starter plan is best fit")
            elif 'enterprise' in budget:
                insights.append("💰 Enterprise budget → Full feature set recommended")
        
        # Insight 4: Frequency patterns
        if memories.count('follow') > 2:
            insights.append("📊 Follow-ups mentioned frequently → High priority feature")
        
        # Insight 5: Evolution tracking
        if 'team_size_changed' in extracted:
            insights.append("📈 Team size evolved during conversations → Scalability important")
        
        return insights[:4]  # Top 4 insights
    
    def get_conversation_stage(self, conversation_count):
        """
        Determine conversation stage
        """
        if conversation_count == 0:
            return "welcome"
        elif conversation_count <= 2:
            return "discovery"
        elif conversation_count <= 5:
            return "understanding"
        else:
            return "recommendation"
    
    def get_memory_confidence(self, user_id):
        """
        Calculate memory confidence score
        """
        memories = self.get_memory(user_id)
        if not memories:
            return 0
        
        score = 0
        memory_lines = len([line for line in memories.split('\n') if line.strip()])
        
        # Base score from messages
        score += min(memory_lines * 8, 60)
        
        # Bonus for profile completeness
        profile = self.get_profile(user_id)
        score += len(profile) * 10
        
        # Bonus for extracted insights
        extracted = self.get_extracted_info(user_id)
        score += len(extracted) * 5
        
        return min(score, 100)
    
    def generate_summary(self, user_id):
        """
        UPGRADE #5: Generate "What I Know About You" summary
        """
        profile = self.get_profile(user_id)
        extracted = self.get_extracted_info(user_id)
        insights = self.generate_insights(user_id)
        confidence = self.get_memory_confidence(user_id)
        
        summary = "# 🧠 What I Know About You\n\n"
        
        # Profile section
        summary += "## 📋 Profile\n"
        if profile:
            for key, value in profile.items():
                summary += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        else:
            summary += "- Building your profile...\n"
        
        summary += "\n## 🎯 Insights\n"
        if extracted:
            for key, value in extracted.items():
                if key not in ['team_size_changed']:
                    summary += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        else:
            summary += "- Learning about your needs...\n"
        
        # Insights section
        if insights:
            summary += "\n## 💡 Key Insights\n"
            for insight in insights:
                summary += f"{insight}\n"
        
        summary += f"\n## 📊 Memory Confidence: {confidence}%\n"
        
        return summary
    
    def chat(self, user_id, user_message, client_name=None, conversation_stage=None):
        """
        Main chat function with FORCED memory usage (UPGRADE #4)
        """
        
        # Retrieve memories and insights
        past_conversations = self.get_memory(user_id)
        profile = self.get_profile(user_id)
        extracted_info = self.get_extracted_info(user_id)
        insights = self.generate_insights(user_id)
        
        # Build insights context
        insights_text = "\n".join(insights) if insights else "No insights yet"
        
        # Build stage-based context
        if conversation_stage == "welcome":
            context = f"""
This is the FIRST conversation with {client_name or 'this person'}.

Their profile:
{profile}

Your goal:
- Give a warm, professional welcome
- Acknowledge their profile information naturally
- Ask ONE clear discovery question about their biggest challenge
- Be conversational and helpful

Example:
"Hi {profile.get('name', 'there')}! Great to meet you. I see you're focused on {profile.get('goal', 'improving sales')}. What's your biggest challenge in that area right now?"
"""
        
        elif conversation_stage == "discovery":
            context = f"""
DISCOVERY stage with {client_name}.

What you know:
{past_conversations}

Profile: {profile}
Extracted: {extracted_info}

MANDATORY: Start your response with a reference to something they mentioned or their profile.

Your goal:
- Reference their profile or previous messages
- Ask targeted questions: tools, timeline, specific pain points
- Build deeper understanding
- ONE question at a time

Example:
"Thanks for sharing that! Since your team has {extracted_info.get('team_size', 'X')} people, I'm curious - how are you currently handling follow-ups?"
"""
        
        elif conversation_stage == "understanding":
            context = f"""
UNDERSTANDING stage with {client_name}.

Complete context:
{past_conversations}

Profile: {profile}
Insights: {insights_text}

MANDATORY: 
- Start with a personalized reference using their name or company
- Use at least ONE insight from their conversations
- Connect their needs to specific solutions

Your goal:
- Show deep understanding
- Provide valuable insights
- Start making connections to FlowSales features
- Be consultative

Example:
"Based on what you've shared, {profile.get('name', 'I see')} - your team of {extracted_info.get('team_size', 'X')} is spending too much time on manual follow-ups. Here's what I'm thinking..."
"""
        
        else:  # recommendation
            context = f"""
RECOMMENDATION stage with {client_name}. You're their trusted advisor.

Everything you know:
{past_conversations}

Profile: {profile}
Key Insights: {insights_text}

MANDATORY:
- Reference multiple specific details from your conversations
- Use their name and company naturally
- Provide expert recommendations based on their complete profile
- Be confident and consultative

Example:
"{profile.get('name', 'Based on our conversations')}, given your team size of {extracted_info.get('team_size', 'X')}, {extracted_info.get('goal', 'your goals')}, and your focus on {extracted_info.get('pain_points', 'efficiency')}, here's my recommendation..."
"""
        
        # Enhanced system prompt with FORCED memory usage
        system_prompt = f"""You are SalesGPT, an expert AI sales consultant for FlowSales.

ABOUT FLOWSALES:
- Sales automation platform (email sequences, automated follow-ups, CRM integration)
- Pricing tiers:
  * Starter: $50/user/month (basic automation)
  * Professional: $100/user/month (advanced features)
  * Enterprise: $150/user/month (full suite + analytics)
- Best for: Sales teams of 3-50 people
- Key features: AI-powered follow-ups, deal tracking, email automation, analytics, pipeline management
- Implementation: 1-2 weeks average
- Integration: Salesforce, HubSpot, Pipedrive, custom APIs
- ROI: Average 20 hours saved per week per rep

{context}

Current client: {client_name or user_id}
User ID: {user_id}

CRITICAL RULES (YOU MUST FOLLOW):
1. ALWAYS start responses with a personalized reference when past context exists
2. Use memory insights in EVERY response after discovery stage
3. Reference their name, company, or specific details they shared
4. Keep responses SHORT (2-4 sentences max)
5. ONLY remember conversations with THIS user_id
6. Never confuse them with other clients
7. Ask ONE question at a time
8. Be genuinely helpful, not pushy
9. When they ask "what do you know about me", provide detailed summary
10. Track objections and address them later

YOUR PERSONALITY:
- Expert sales consultant (10+ years experience)
- Excellent listener
- Problem solver
- Friendly but professional
- Data-driven
- Memory-powered (you never forget)

RESPONSE QUALITY:
- Bad: "Here are some options..."
- Good: "Since your team has 8 reps and you mentioned follow-ups, here's what I recommend..."
- Great: "Hi {profile.get('name', '')}, based on our conversation about {extracted_info.get('goals', 'your goals')} and your team of {extracted_info.get('team_size', 'X')}, I think..."
"""
        
        # Get LLM response
        try:
            llm = get_llm_client()
            
            response = llm.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=450
            )
            
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ LLM Error: {str(e)}")
            ai_response = "I'm having a moment - can you try that again? 😅"
        
        # Extract new information from this exchange
        new_extracted = {}
        
        # Check for team size mentions
        team_match = re.search(r'(\d+)\s*(?:people|reps|members)', user_message, re.IGNORECASE)
        if team_match:
            new_extracted['team_size'] = team_match.group(1)
        
        # Check for budget mentions
        if any(word in user_message.lower() for word in ['cheap', 'affordable', 'budget', 'expensive']):
            if any(word in user_message.lower() for word in ['tight', 'limited', 'small']):
                new_extracted['budget'] = 'Limited'
            elif any(word in user_message.lower() for word in ['flexible', 'not an issue']):
                new_extracted['budget'] = 'Enterprise'
        
        # Save conversation with evolution tracking
        conversation_record = f"""
{datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{client_name or 'User'}: {user_message}

SalesGPT: {ai_response}
"""
        
        self.save_to_memory(
            user_id=user_id,
            conversation_text=conversation_record,
            client_name=client_name,
            extracted_data=new_extracted if new_extracted else None
        )
        
        return ai_response


# Quick test
if __name__ == "__main__":
    print("\n🧪 Testing Enhanced FlowSales System...\n")
    agent = SalesGPT()
    
    # Test profile save
    agent.save_profile(
        user_id="test_001",
        profile_data={
            "name": "Test User",
            "company": "Test Corp",
            "team_size": "5-10",
            "goal": "Automate follow-ups"
        }
    )
    
    # Test chat
    response = agent.chat(
        user_id="test_001",
        user_message="Hi! Tell me about FlowSales.",
        client_name="Test User",
        conversation_stage="welcome"
    )
    print(f"AI: {response}\n")
    
    # Test insights
    insights = agent.generate_insights("test_001")
    print(f"Insights: {insights}\n")
    
    print("✅ System ready!")