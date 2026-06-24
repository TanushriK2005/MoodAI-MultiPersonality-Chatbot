# 🤖 MoodAI – Multi-Personality AI Chatbot

A Generative AI-powered chatbot that allows users to interact with different AI personalities such as **Angry**, **Funny**, and **Sad**. Built using **LangChain**, **Mistral AI**, **Streamlit**, and **Hugging Face Embeddings**, the application demonstrates prompt engineering, conversation memory, and interactive AI-driven conversations.

---

## 🚀 Features

* 🎭 Multiple AI Personalities

  * 😡 Angry Mode
  * 😂 Funny Mode
  * 😢 Sad Mode

* 💬 Context-Aware Conversations

  * Maintains conversation history
  * Uses LangChain message objects for memory

* 🧠 Prompt Engineering

  * Dynamic system prompts based on selected personality
  * Distinct conversational behavior for each mode

* 🎨 Interactive Web Interface

  * Built with Streamlit
  * Clean and responsive chat interface
  * Real-time AI responses

* ⚡ Mistral AI Integration

  * Powered by Mistral Large Language Models
  * Fast and intelligent conversational responses

* 🤗 Hugging Face Embeddings

  * Embedding generation support
  * Foundation for future RAG-based enhancements

---

## 📸 Personality Demonstrations

### 😡 Angry Mode

![Angry Mode](images/angry-mode-demo.png)

### 😂 Funny Mode

![Funny Mode](images/funny-mode-demo.png)

### 😢 Sad Mode

![Sad Mode](images/sad-mode-demo.png)

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Mistral AI
* Hugging Face Embeddings
* Sentence Transformers
* Python Dotenv

---

## 📂 Project Structure

```text
MoodAI-MultiPersonality-Chatbot
│
├── chatmodels
│   ├── chat.py
│   ├── chatbot.py
│   └── UIchatbot.py
│
├── embeddingmodels
│   └── huggingface_embedding.py
│
├── images
│   ├── angry-mode-demo.png
│   ├── funny-mode-demo.png
│   └── sad-mode-demo.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/MoodAI-MultiPersonality-Chatbot.git
cd MoodAI-MultiPersonality-Chatbot
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run chatmodels/UIchatbot.py
```

Open your browser and visit:

```text
http://localhost:8501
```

---

## 🧠 How It Works

1. User selects an AI personality.
2. A system prompt is generated dynamically.
3. User messages are stored using LangChain message objects.
4. Conversation history is maintained throughout the session.
5. Mistral AI generates context-aware responses.
6. Responses are displayed through Streamlit's interactive chat interface.

---

## 🎯 Learning Outcomes

This project helped explore:

* Generative AI Fundamentals
* Prompt Engineering
* LangChain Framework
* Mistral AI Integration
* Streamlit Application Development
* Conversation Memory Management
* Hugging Face Embeddings
* Interactive AI System Design

---

## 🔮 Future Enhancements

* 📄 PDF Chat using RAG
* 📚 Document Question Answering
* 🎙️ Voice-Based Conversations
* 🌍 Multi-Language Support
* 💾 Persistent Chat History
* 📊 Conversation Analytics Dashboard
* 🧠 Additional AI Personalities

---

## 👩‍💻 Author

**Tanushri Kalaskar**

B.Tech Information Technology Student
AI/ML & Generative AI Enthusiast

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
