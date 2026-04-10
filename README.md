

# 🧠 SalesGPT — AI Sales Assistant with Perfect Memory

> An AI-powered sales agent that remembers every conversation and gets smarter over time using Hindsight memory.

**Built for Vectorize Hindsight Hackathon 2026**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-MVP-green.svg)

---

## 🎯 The Problem

Sales representatives lose deals every day because:

* ❌ They forget what prospects said in previous calls
* ❌ Prospects have to repeat themselves constantly
* ❌ Follow-ups are generic instead of personalized
* ❌ Important details (budget, pain points, objections) slip through the cracks

**Result:** Lost deals, frustrated prospects, wasted time.

---

## ✨ The Solution

**SalesGPT** uses **Hindsight memory** by Vectorize to create an AI sales assistant that:

✅ Remembers every conversation
✅ Gets smarter over time
✅ Personalizes every response
✅ Never forgets key prospect details

---

## 🎬 Demo

**Conversation 1 (Day 1)**
Rep: "Hi Rajesh, what did you think of the demo?"
Prospect: "It looked great but the pricing is too steep for our budget."

**Conversation 2 (Day 3)**
AI: "Rajesh, I remember you mentioned budget concerns. I wanted to share our ROI calculator..."

**Conversation 3 (Day 7)**
AI: "Rajesh, knowing you liked automation but needed a smaller package, I have good news..."

**The AI remembers:**

* Budget constraints ✅
* Liked automation features ✅
* Small team context ✅
* Interest in smaller packages ✅

---

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* Hindsight Cloud account
* Groq API key

---

### Installation

```bash
# Clone repository
git clone https://github.com/HarshitPandey-2021/salesgpt-hackathon.git
cd salesgpt-hackathon

# Create virtual environment
python -m venv venv

# Activate environment
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Configuration

Create a `.env` file in project root:

```
HINDSIGHT_API_KEY=<<YOUR_HINDSIGHT_API_KEY>>
GROQ_API_KEY=<<YOUR_GROQ_API_KEY>>
```

---

### Run the App

```bash
# Test core logic
python main.py

# Run web UI
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 💡 How It Works

```
User Input → SalesGPT → Groq LLM → Hindsight Memory → Response
                          ↑              ↓
                          └── Past conversations retrieved
```

### Memory Flow

1. User sends message to a prospect
2. SalesGPT retrieves past conversations
3. LLM generates personalized response
4. Conversation saved for future use
5. Memory improves over time

---

## ✨ Key Features

* 🧠 Persistent Memory using Hindsight
* 🤖 Fast responses with Groq LLM
* 👥 Multiple prospect support
* 💬 Streamlit UI
* 📊 Memory visualization
* 🔒 Secure API key handling

---

## 🏗️ Tech Stack

| Component | Technology             |
| --------- | ---------------------- |
| Memory    | Hindsight by Vectorize |
| LLM       | Groq (llama-3.3-70b)   |
| Frontend  | Streamlit              |
| Language  | Python 3.8+            |
| SDK       | hindsight-client       |

---

## 📁 Project Structure

```
salesgpt-hackathon/
│
├── main.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🎓 What I Learned

### Technical

* Vector database integration
* LLM prompt engineering
* API architecture design
* Error handling strategies

### Business

* Memory creates differentiation
* Context improves over time
* Personalization increases conversions
* Real-world sales impact

---

## 🎯 Future Enhancements

* Multi-user support
* Deal stage tracking
* Email integration
* Analytics dashboard
* Voice interface
* CRM integration
* Prospect mental models

---

## 👥 Team

* Harshit Pandey — Backend, AI logic, UI
* Shiva Singh — Testing 
* Somesh Pandey— Documentation & Demo

---

## 🤝 Contributing

Feel free to:

* Report bugs
* Suggest features
* Submit pull requests

---


## 🙏 Acknowledgments

* Vectorize (Hindsight)
* Groq
* Streamlit
* Hackathon organizers

---

## 📧 Contact

GitHub: [https://github.com/](https://github.com/)<<HarshitPandey-2021>>
Email: <<pandey6051172@gmail.com>>

---

## 🔗 Links

Live Demo: <<LIVE_DEMO_LINK>>
Demo Video: <<VIDEO_LINK>>
Hindsight Docs: [https://docs.vectorize.io](https://docs.vectorize.io)
Hackathon: <<HACKATHON_LINK>>

---

⭐ If you find this project useful, please give it a star!
