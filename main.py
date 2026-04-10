import os
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI

# Load environment variables
load_dotenv()

# API Keys
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Hindsight API endpoint (check their docs for exact endpoint)
HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io/v1"  # VERIFY THIS IN DOCS

# Initialize Groq client (it's OpenAI-compatible)
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# OR if using Featherless:
# client = OpenAI(
#     api_key=os.getenv("FEATHERLESS_API_KEY"),
#     base_url="https://api.featherless.ai/v1"
# )


class SalesGPT:
    def __init__(self):
        self.hindsight_api_key = HINDSIGHT_API_KEY
        self.llm_client = client
        
    def save_to_memory(self, prospect_name, conversation):
        """
        Save conversation to Hindsight memory
        """
        # Check Hindsight docs for exact API format
        # This is a template - adjust based on their docs
        
        headers = {
            "Authorization": f"Bearer {self.hindsight_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "user_id": prospect_name,  # Each prospect is a "user"
            "memory": conversation,
            "metadata": {
                "timestamp": str(datetime.now()),
                "type": "sales_conversation"
            }
        }
        
        response = requests.post(
            f"{HINDSIGHT_BASE_URL}/memories",  # Check docs for endpoint
            headers=headers,
            json=payload
        )
        
        return response.json()
    
    def get_memory(self, prospect_name):
        """
        Retrieve all past conversations with this prospect
        """
        headers = {
            "Authorization": f"Bearer {self.hindsight_api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{HINDSIGHT_BASE_URL}/memories/{prospect_name}",  # Check docs
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    
    def chat(self, prospect_name, user_message):
        """
        Main chat function
        """
        # 1. Get past memories
        past_conversations = self.get_memory(prospect_name)
        
        # 2. Build context from memory
        memory_context = ""
        if past_conversations:
            memory_context = "Previous conversations with this prospect:\n"
            for conv in past_conversations:
                memory_context += f"- {conv}\n"
        
        # 3. Create prompt
        system_prompt = f"""You are SalesGPT, an AI sales assistant with perfect memory.

Your job: Help sales reps follow up with prospects by remembering everything from past conversations.

{memory_context}

Current prospect: {prospect_name}

Instructions:
- Reference past conversations naturally
- Adapt your pitch based on what they said before
- If this is first conversation, be friendly and gather info
- If you know their pain points, address them
- Sound human and helpful, not robotic
"""
        
        # 4. Get LLM response
        response = self.llm_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Groq model
            # model="meta-llama/Meta-Llama-3.1-70B-Instruct",  # Featherless
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        # 5. Save this conversation to memory
        conversation_record = f"User: {user_message}\nAI: {ai_response}"
        self.save_to_memory(prospect_name, conversation_record)
        
        return ai_response


# Test it
if __name__ == "__main__":
    agent = SalesGPT()
    
    # Test conversation 1
    print("=== Conversation 1 with Rajesh ===")
    response1 = agent.chat(
        "Rajesh Kumar",
        "Hi, following up on our demo. What did you think?"
    )
    print(f"AI: {response1}\n")
    
    # Simulate prospect response (in real app, this comes from user)
    agent.save_to_memory(
        "Rajesh Kumar",
        "User (Rajesh): It looked good but honestly it seems expensive for our current budget."
    )
    
    # Test conversation 2 (next day)
    print("=== Conversation 2 with Rajesh (next day) ===")
    response2 = agent.chat(
        "Rajesh Kumar",
        "Hi Rajesh, wanted to follow up with you"
    )
    print(f"AI: {response2}\n")
    
    # You should see it reference budget concerns!