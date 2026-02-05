## 🤖 Multimodel Chatbot
---
A full-stack Conversational Chatbot and Text Generation Service built using LangChain, LlamaIndex, and FastAPI, featuring a Streamlit UI.
The entire solution is containerized with Docker and deployed on AWS EC2 for scalable cloud-based inference.

🚀 Features
---
* 💬 Conversational chatbot UI powered by Streamlit
* 🧠 Toggle between LangChain and LlamaIndex backend APIs
* ⚡️ FastAPI microservices for each framework
	* Port 8000 → LangChain
	* Port 8001 → LlamaIndex
* 🐳 Single Docker container runs both APIs + Streamlit UI
* 🔐 Secure API key management via .streamlit/secrets.toml
* ☁️ Fully deployed on AWS EC2 with public endpoint
---

🧩 Technology Stack
---

<img width="409" height="391" alt="image" src="https://github.com/user-attachments/assets/441689c4-7ce8-4d88-adb9-8aaaadbc5137" />



🧱 Project Structure
---

├── app.py                  # Streamlit frontend with model switch

├── lang_chat.py            # FastAPI app for LangChain

├── llamaindex_chat.py      # FastAPI app for LlamaIndex

├── requirements.txt        # Dependencies

├── Dockerfile              # Container setup (Streamlit + APIs)

├── .streamlit/

│   └── secrets.toml        # Stores API keys securely

└── README.md               # Documentation

---

⚙️ Setup & Local Run
---

1️⃣ Add Your API Key
Create .streamlit/secrets.toml and include:

OPENAI_API_KEY = "YOUR_API_KEY"

Or

You can keep your key details in .env file

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Run Locally
python lang_chat.py    # Runs LangChain API on port 8000
python llamaindex_chat.py  # Runs LlamaIndex API on port 8001
streamlit run app.py   # Runs Streamlit UI on port 8501

Access at 👉 http://localhost:8501

🐳 Docker Deployment
---

Build Image
```
docker build -t ai-frameworks-chatbot .
```
Run Container
```
docker run -d -p 8501:8501 -p 8000:8000 -p 8001:8001 ai-frameworks-chatbot
```
Then open your browser at
👉 http://localhost:8501

☁️ AWS EC2 Deployment (Free Tier Eligible)
---
* Launch an Ubuntu 24.04 EC2 Instance (t2.micro)
* SSH into instance
* Install Docker
* sudo apt update && sudo apt install docker.io -y
* Copy project files using WinSCP or git clone
* Build & Run Docker
	* docker build -t ai-frameworks-chatbot .
	* docker run -d -p 8501:8501 -p 8000:8000 -p 8001:8001 ai-frameworks-chatbot
* Add Inbound Rules to Security Group
* TCP 22 → SSH (Your IP only)
* TCP 8501, 8000, 8001 → 0.0.0.0/0
* 
✅ Access at:
http://:8501

---

🧠 Technical Architecture
---
📘 Architecture Overview
Below is the architecture representing:

* Streamlit UI
* LangChain & LlamaIndex FastAPI backends
* Docker container orchestration
* AWS EC2 deployment layer

<img width="1224" height="690" alt="image" src="https://github.com/user-attachments/assets/dd1280f6-35a0-4f66-9a18-b61cf1ae4781" />


🔐 Security Notes
---
✅ API Keys are never hardcoded (stored in .streamlit/secrets.toml or you can keep in .env file)

✅ AWS-level network security (controlled inbound rules)
