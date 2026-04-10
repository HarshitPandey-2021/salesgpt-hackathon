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

# Initialize Hindsight client
hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)

# Initialize Groq client (OpenAI-compatible)
llm_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


class SalesGPT:
    def __init__(self, bank_id="salesgpt-memory"):
        """
        Initialize SalesGPT with Hindsight memory
        """
        self.hindsight = hindsight_client
        self.llm = llm_client
        self.bank_id = bank_id
        
        # Create memory bank if it doesn't exist
        try:
            self.hindsight.create_bank(
                bank_id=self.bank_id,
                name="SalesGPT Memory Bank"
            )
            print(f"✅ Created memory bank: {self.bank_id}")
        except Exception as e:
            print(f"ℹ️ Memory bank already exists: {self.bank_id}")
    
    def save_to_memory(self, prospect_name, conversation_text):
        """
        Save conversation to Hindsight memory
        """
        try:
            self.hindsight.retain(
                bank_id=self.bank_id,
                content=f"[{prospect_name}] {conversation_text}",
                metadata={
                    "prospect": prospect_name,
                    "timestamp": datetime.now().isoformat(),
                    "type": "sales_conversation"
                }
            )
            print(f"💾 Saved memory for {prospect_name}")
            return True
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
            return False
    
    def get_memory(self, prospect_name):
        """
        Retrieve all past conversations with this prospect from Hindsight
        """
        try:
            # Recall memories - NO LIMIT PARAMETER!
            result = self.hindsight.recall(
                bank_id=self.bank_id,
                query=f"All conversations and information about {prospect_name}"
            )
            
            if result.results:
                # Get up to 10 most relevant results
                memories = result.results[:10] if len(result.results) > 10 else result.results
                
                memory_text = "\n".join([
                    f"- {memory.text}" 
                    for memory in memories
                ])
                print(f"🧠 Retrieved {len(memories)} memories for {prospect_name}")
                return memory_text
            else:
                print(f"ℹ️ No previous memories found for {prospect_name}")
                return ""
                
        except Exception as e:
            print(f"❌ Error retrieving memory: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def chat(self, prospect_name, user_message, simulate_prospect_response=None):
        """
        Main chat function - generates AI sales assistant response
        """
        
        # 1. Get past memories about this prospect
        past_conversations = self.get_memory(prospect_name)
        
        # 2. Build context from memory
        if past_conversations:
            memory_context = f"""
PAST CONVERSATIONS WITH {prospect_name}:
{past_conversations}

IMPORTANT: Use this context to personalize your response. Reference specific things they mentioned before.
Show that you REMEMBER previous conversations.
"""
        else:
            memory_context = f"This is your FIRST conversation with {prospect_name}. Focus on building rapport and understanding their needs."
        
        # 3. Create system prompt
        system_prompt = f"""You are SalesGPT, an elite AI sales assistant with perfect memory.

Your role: Help sales representatives have better conversations with prospects by remembering everything from past interactions.

{memory_context}

Current prospect: {prospect_name}

Instructions:
- If you have past conversation context, ALWAYS reference it specifically
- Mention specific things they said before (budget concerns, feature interests, pain points, etc.)
- Adapt your approach based on what you learned
- If this is the first conversation, focus on discovery
- Sound like a helpful human sales assistant, not a robot
- Be concise but personalized
"""
        
        # 4. Get LLM response
        try:
            response = self.llm.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            ai_response = f"Error: Could not generate response. {e}"
        
        # 5. Save this interaction to memory
        conversation_record = f"""
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Sales Rep: {user_message}
AI Assistant Response: {ai_response}
"""
        
        self.save_to_memory(prospect_name, conversation_record)
        
        # 6. If there's a simulated prospect response, save that too
        if simulate_prospect_response:
            prospect_record = f"""
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{prospect_name} (Prospect): {simulate_prospect_response}
"""
            self.save_to_memory(prospect_name, prospect_record)
        
        return ai_response
    
    def close(self):
        """Close the Hindsight client"""
        try:
            self.hindsight.close()
        except:
            pass


# ============================================
# TEST THE SYSTEM
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TESTING SALESGPT WITH HINDSIGHT MEMORY")
    print("=" * 60)
    
    # Initialize agent
    agent = SalesGPT()
    
    print("\n" + "=" * 60)
    print("📞 CONVERSATION 1 with Rajesh Kumar (Day 1)")
    print("=" * 60)
    
    response1 = agent.chat(
        prospect_name="Rajesh Kumar",
        user_message="Hi Rajesh, thanks for taking my call. I wanted to follow up on the product demo we did last week. What did you think?",
        simulate_prospect_response="Thanks for following up! The demo was impressive, I really liked the automation features. But honestly, the pricing is a bit steep for our current budget. We're a small team and can't justify $10k/month right now."
    )
    
    print(f"\n🤖 AI Response:\n{response1}\n")
    
    # Wait a moment
    print("\n⏳ Waiting 2 seconds to simulate time passing...\n")
    import time
    time.sleep(2)
    
    print("\n" + "=" * 60)
    print("📞 CONVERSATION 2 with Rajesh Kumar (Day 3 - Follow up)")
    print("=" * 60)
    
    response2 = agent.chat(
        prospect_name="Rajesh Kumar",
        user_message="Hi Rajesh, wanted to circle back with you. Have you had a chance to think more about our solution?",
        simulate_prospect_response="Hey, yes I've been thinking about it. The budget is still the main blocker. What's the minimum commitment? Can we start with a smaller package?"
    )
    
    print(f"\n🤖 AI Response:\n{response2}\n")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("=" * 60)
    print("\n🔍 CHECK IF THE AI REMEMBERED:")
    print("✓ Did it mention Rajesh's budget concerns in conversation 2?")
    print("✓ Did it reference the automation features he liked?")
    print("✓ Did it mention the small team context?")
    print("\nIf YES = HINDSIGHT MEMORY IS WORKING! 🎉")
    print("=" * 60)
    
    # Close client properly
    agent.close()