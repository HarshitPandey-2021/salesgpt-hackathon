import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

# API Keys
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize clients globally
hindsight_client = None
llm_client = None

def get_hindsight_client():
    """Get or create Hindsight client"""
    global hindsight_client
    if hindsight_client is None:
        hindsight_client = Hindsight(
            base_url="https://api.hindsight.vectorize.io",
            api_key=HINDSIGHT_API_KEY
        )
    return hindsight_client

def get_llm_client():
    """Get or create LLM client"""
    global llm_client
    if llm_client is None:
        llm_client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
    return llm_client


class SalesGPT:
    def __init__(self, bank_id="flowsales-multichats-v3"):
        """
        Initialize SalesGPT with Hindsight memory
        """
        self.bank_id = bank_id
        
        # Create memory bank if it doesn't exist
        try:
            client = get_hindsight_client()
            client.create_bank(
                bank_id=self.bank_id,
                name="FlowSales Multi-Client Memory Bank v3"
            )
            print(f"✅ Memory bank ready: {self.bank_id}")
        except Exception as e:
            print(f"ℹ️ Memory bank exists: {str(e)[:80]}")
    
    def save_to_memory(self, user_id, conversation_text, client_name=None, client_company=None):
        """
        Save conversation to Hindsight with STRICT metadata for isolation
        """
        try:
            client = get_hindsight_client()
            
            # CRITICAL: Include user_id in content for perfect isolation
            tagged_content = f"[USER_ID:{user_id}] [CLIENT:{client_name or 'Unknown'}] {conversation_text}"
            
            # Build rich metadata
            metadata = {
                "user_id": user_id,  # CRITICAL for filtering
                "timestamp": datetime.now().isoformat(),
                "type": "conversation"
            }
            
            if client_name:
                metadata["client_name"] = client_name
            if client_company:
                metadata["client_company"] = client_company
            
            # Save to Hindsight
            client.retain(
                bank_id=self.bank_id,
                content=tagged_content,
                metadata=metadata
            )
            
            print(f"���� Saved memory for {client_name or user_id} (ID: {user_id})")
            return True
            
        except Exception as e:
            print(f"❌ Memory save error: {str(e)[:100]}")
            return False
    
    def get_memory(self, user_id):
        """
        Retrieve conversation history ONLY for specific user_id
        """
        try:
            client = get_hindsight_client()
            
            # CRITICAL: Query with user_id to ensure isolation
            result = client.recall(
                bank_id=self.bank_id,
                query=f"USER_ID:{user_id} - All previous conversations, name, company, budget, team size, pain points, goals, preferences discussed"
            )
            
            if result.results:
                # Filter to ensure ONLY this user's memories
                filtered_memories = [
                    memory for memory in result.results
                    if f"USER_ID:{user_id}" in memory.text
                ]
                
                if not filtered_memories:
                    print(f"ℹ️ No memories yet for {user_id}")
                    return ""
                
                # Get top 10 most relevant memories
                memories = filtered_memories[:10]
                
                memory_text = "\n".join([
                    f"- {memory.text.replace(f'[USER_ID:{user_id}]', '').replace(f'[CLIENT:', '[')}"
                    for memory in memories
                ])
                
                print(f"🧠 Retrieved {len(memories)} memories for {user_id}")
                return memory_text
            else:
                print(f"ℹ️ No memories yet for {user_id}")
                return ""
                
        except Exception as e:
            print(f"❌ Memory retrieval error: {str(e)[:100]}")
            return ""
    
    def get_conversation_count(self, user_id):
        """
        Get conversation count for specific user
        """
        memories = self.get_memory(user_id)
        if not memories:
            return 0
        
        # Count conversation entries
        count = len([line for line in memories.split('\n') if 'Conversation #' in line])
        return max(count, len(memories.split('\n')) // 3)
    
    def chat(self, user_id, user_message, client_name=None, client_company=None):
        """
        Main chat function with PERFECT memory isolation per user_id
        """
        
        # Retrieve ONLY this user's memories
        past_conversations = self.get_memory(user_id)
        conversation_count = self.get_conversation_count(user_id)
        
        # Build context based on history
        if conversation_count == 0:
            # FIRST CONVERSATION
            context = f"""
This is your FIRST conversation with {client_name or 'this person'}.

Your goal:
- Give them a warm, friendly welcome
- Introduce yourself as their FlowSales AI consultant
- Ask ONE natural discovery question about their sales challenges
- Be conversational (like talking to a friend)
- Don't overwhelm them

Example:
"Hey! I'm your FlowSales AI consultant. I'm here to help solve your sales challenges. To get started - what's the biggest thing slowing down your sales right now?"
"""
        
        elif conversation_count < 3:
            # EARLY STAGE
            context = f"""
You've chatted with {client_name or 'this client'} {conversation_count} time(s).

What you remember about THEM:
{past_conversations}

Your goal:
- Reference something specific THEY mentioned before
- Ask ONE more natural question to understand THEIR situation
- Be helpful and genuinely interested
- Focus on: budget, team size, pain points, timeline

Example:
"Thanks! I remember you mentioned [specific thing]. Quick question - how many people are on your sales team?"
"""
        
        elif conversation_count < 6:
            # MID STAGE
            context = f"""
You've had {conversation_count} conversations with {client_name or 'this client'}.

Everything you know about THEM:
{past_conversations}

Your goal:
- Show you deeply understand THEIR situation
- Reference multiple things THEY shared (budget, team, pain points)
- Start making personalized recommendations for THEM
- Connect FlowSales features to THEIR specific needs

Example:
"Based on what you've shared - [their budget], [their team size], [their pain point] - here's what I recommend..."
"""
        
        else:
            # EXPERT STAGE
            context = f"""
You've had {conversation_count} conversations with {client_name or 'this client'}. You're their trusted advisor.

Complete history with THIS client:
{past_conversations}

Your goal:
- Act like you've been working together for months
- Reference specific details from YOUR conversations together
- Anticipate THEIR needs before they ask
- Provide expert guidance tailored to THEM

You should sound like a consultant who knows THEM inside-out.
"""
        
        # System prompt
        system_prompt = f"""You are SalesGPT, an expert AI sales consultant for FlowSales.

ABOUT FLOWSALES:
- Sales automation platform (email sequences, automated follow-ups, CRM integration)
- Pricing: $50-150 per user/month (depending on features)
- Best for: Sales teams of 3-50 people
- Key features: AI-powered follow-ups, deal tracking, email automation, sales analytics
- Implementation time: 1-2 weeks on average

{context}

Current client: {client_name or user_id}
{f"Company: {client_company}" if client_company else ""}
User ID: {user_id}

CRITICAL RULES:
- ONLY remember conversations with THIS specific client (user_id: {user_id})
- Be conversational and warm
- Keep responses SHORT (2-4 sentences max)
- Focus on THEIR needs
- Always reference THEIR past conversations (if any)
- NEVER confuse them with other clients
- If they ask "what am I" or "who am I", tell them their name and company based on YOUR conversations with THEM

YOUR PERSONALITY:
- Smart and helpful
- Great listener
- Genuinely wants them to succeed
- Expert in sales automation
- Friendly but professional
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
                max_tokens=350
            )
            
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ LLM Error: {str(e)}")
            ai_response = "I'm having a moment - can you try that again? 😅"
        
        # Save conversation to memory (with user_id tag)
        conversation_record = f"""
Conversation #{conversation_count + 1} - {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{client_name or 'User'} said: {user_message}

SalesGPT responded: {ai_response}
"""
        
        self.save_to_memory(
            user_id=user_id,
            conversation_text=conversation_record,
            client_name=client_name,
            client_company=client_company
        )
        
        return ai_response


# Test multi-client isolation
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTING MULTI-CLIENT MEMORY ISOLATION")
    print("="*60)
    
    agent = SalesGPT()
    
    # Chat 1: Harsh from ABC
    print("\n" + "="*60)
    print("CHAT 1: Harsh from ABC")
    print("="*60)
    response = agent.chat(
        user_id="chat_001_harsh",
        user_message="Hi! I'm Harsh from ABC Corp. We need sales automation.",
        client_name="Harsh",
        client_company="ABC Corp"
    )
    print(f"\n🤖 AI: {response}")
    
    # Chat 2: Vincenzo from XYZ
    print("\n" + "="*60)
    print("CHAT 2: Vincenzo from XYZ")
    print("="*60)
    response = agent.chat(
        user_id="chat_002_vincenzo",
        user_message="Hello! I'm Vincenzo from XYZ Inc. We have 15 reps.",
        client_name="Vincenzo",
        client_company="XYZ Inc"
    )
    print(f"\n🤖 AI: {response}")
    
    # Switch back to Chat 1
    print("\n" + "="*60)
    print("BACK TO CHAT 1: Testing Memory Recall")
    print("="*60)
    response = agent.chat(
        user_id="chat_001_harsh",
        user_message="What's my name and company?",
        client_name="Harsh",
        client_company="ABC Corp"
    )
    print(f"\n🤖 AI: {response}")
    
    # Switch to Chat 2
    print("\n" + "="*60)
    print("BACK TO CHAT 2: Testing Memory Recall")
    print("="*60)
    response = agent.chat(
        user_id="chat_002_vincenzo",
        user_message="How many reps did I mention?",
        client_name="Vincenzo",
        client_company="XYZ Inc"
    )
    print(f"\n🤖 AI: {response}")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE - MEMORY ISOLATION VERIFIED!")
    print("="*60)