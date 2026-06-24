
# 🤖 Multi-Agent Research System using LangChain

An AI-powered research assistant that uses a multi-agent architecture to automatically search, analyze, synthesize, and critique information from the web.

🔗 **Live Demo:** https://multi-agent-research-system-using.onrender.com

---
web Interface :

<img width="1907" height="936" alt="image" src="https://github.com/user-attachments/assets/c00d8a00-d367-4ab0-9ffc-4b69faf37552" />

#####

<img width="1908" height="931" alt="image" src="https://github.com/user-attachments/assets/b9ca8192-f586-4d11-a370-21f7311594e7" />




## 🚀 Overview

The Multi-Agent Research System is an intelligent research pipeline built with **LangChain**, **Groq LLMs**, **Tavily Search**, and **Streamlit**.

Instead of relying on a single prompt, the system delegates responsibilities across specialized AI agents:

* 🔍 Search Agent
* 📖 Reader Agent
* ✍️ Writer Chain
* 🎯 Critic Chain

These components collaborate to produce high-quality research reports on any topic provided by the user.

---

## 🏗️ Architecture

```text
User Topic
    │
    ▼
🔍 Search Agent
    │
    ▼
Best Source Selection
    │
    ▼
📖 Reader Agent
    │
    ▼
Deep Content Extraction
    │
    ▼
✍️ Writer Chain
    │
    ▼
Research Report
    │
    ▼
🎯 Critic Chain
    │
    ▼
Quality Evaluation
```

---

## ⚡ Features

### 🔍 Search Agent

* Searches the web using Tavily Search API
* Finds recent and relevant information
* Evaluates search results
* Selects the most relevant source

### 📖 Reader Agent

* Scrapes selected web pages
* Extracts clean readable content
* Removes navigation menus, ads, scripts, and clutter
* Uses multiple extraction strategies for reliability

### ✍️ Writer Chain

Generates a structured report including:

* Introduction
* Key Findings
* Conclusion
* Sources

### 🎯 Critic Chain

Evaluates the generated report and provides:

* Research Score
* Strengths
* Areas for Improvement
* Final Verdict

### 🌐 Modern Web Interface

* Dark AI SaaS-inspired UI
* Interactive pipeline visualization
* Real-time status updates
* Responsive design
* Professional user experience

---

## 🧠 How It Works

### Step 1: Search Agent

The Search Agent uses Tavily Search to gather web information related to the user's topic.

Example:

```text
Topic:
Impact of AI on the Job Market in 2026
```

The agent identifies the most relevant source and returns:

```text
Title
URL
Snippet
```

---

### Step 2: Reader Agent

The Reader Agent scrapes the selected URL and extracts meaningful content.

Extraction Strategy:

1. Trafilatura
2. Readability
3. BeautifulSoup Fallback

This ensures robust content extraction across different websites.

---

### Step 3: Writer Chain

The Writer combines:

* Search Results
* Scraped Content

to generate a professional research report.

---

### Step 4: Critic Chain

The Critic reviews the report and provides objective feedback and scoring.

---

## 🛠️ Tech Stack

### AI & LLM

* LangChain
* Groq
* Llama 3.3 70B Versatile

### Search & Research

* Tavily Search API

### Web Scraping

* Requests
* BeautifulSoup
* Readability-LXML
* Trafilatura

### Frontend

* Streamlit

### Utilities

* Python Dotenv

---

## 📂 Project Structure

```text
Multi-Agent-Research-System/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
│
├── src
│   │
│   ├── agents
│   │   └── agents.py
│   │
│   ├── tools
│   │   └── tools.py
│   │
│   └── pipeline
│       └── pipeline.py
│
└── README.md
```

---

## 🔧 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Multi-Agent-Research-System-using-Langchain.git

cd Multi-Agent-Research-System-using-Langchain
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 🌍 Deployment

### Render

This project is deployed on Render:

https://multi-agent-research-system-using.onrender.com

---

## 📸 Screenshots

Add screenshots of:

* Home Page
* Research Pipeline
* Generated Report
* Critic Feedback

---

## 🔮 Future Enhancements

* Multi-source research synthesis
* Top-K source ranking
* PDF report generation
* Report export to DOCX
* Citation management
* LangGraph workflow integration
* Parallel web scraping
* Research memory and history
* Agent observability dashboard

---

## 💡 Example Topics

Try researching:

* Future of AGI Development
* Impact of AI on Healthcare
* Climate Change and Renewable Energy
* Quantum Computing Roadmap
* Future of Autonomous Vehicles
* AI Agents in 2026

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit a pull request.

---

## ⭐ Support

If you found this project useful, please consider giving it a star ⭐ on GitHub.

It helps others discover the project and supports future development.

---

## 👨‍💻 Author

Developed by Ranjith Kumar

Passionate about AI, Machine Learning, Agentic AI Systems, and Full-Stack Development.
