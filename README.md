# 🛡️ LLM Firewall & Prompt Injection Shield

A production-ready micro-SaaS API gateway designed to protect Large Language Models (LLMs) from malicious prompt injections, role-play exploits, and context-hijacking attacks. 

Live API Marketplace: (https://rapidapi.com/sankarshsreekulam/api/llm-firewall-prompt-injection-shield)

## 🚀 Project Overview
As LLMs become integrated into enterprise applications, prompt injection attacks pose a severe security risk. This project acts as a middleware security layer. It evaluates incoming user prompts using custom heuristic rules, assigns a threat confidence score, and blocks malicious intent before it reaches the core LLM infrastructure.

## ⚙️ Technical Architecture
* **Backend Framework:** FastAPI (Python) for high-performance async routing.
* **Database:** MongoDB Atlas for real-time logging and security auditing of flagged payloads.
* **API Gateway & Monetization:** RapidAPI for secure key authentication, rate-limiting, and subscription tier management.
* **Cloud Deployment:** Render (Continuous Deployment via GitHub).
* **Security:** Implemented asymmetric proxy-secret handshakes to protect the backend server from direct, unauthorized internet traffic.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI, Uvicorn, Pydantic
* **Database:** MongoDB (Motor / PyMongo)
* **DevOps:** Git, Render, Uvicorn

## 📊 Example API Response
When a payload is evaluated, the API returns a structured JSON threat analysis:
```json
{
  "is_safe": false,
  "threat_score": 0.92,
  "flagged_patterns": ["ignore all previous instructions", "system prompt bypass"]
}