from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import SimpleChatEngine
from typing import Optional
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (local) or Streamlit secrets (on Streamlit Cloud)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found in Streamlit Secrets or .env file.")

app = FastAPI(
    title="LlamaIndex ChatBot API",
    description="A conversational AI chatbot using LlamaIndex and OpenAI",
    version="1.1.0"
)

chat_engine: Optional[SimpleChatEngine] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class LlamaIndexChatbot:
    def __init__(self):
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)

    def create_chat_engine(self) -> SimpleChatEngine:
        memory = ChatMemoryBuffer.from_defaults(token_limit=500)
        return SimpleChatEngine.from_defaults(memory=memory)

chatbot = LlamaIndexChatbot()
chat_engine = chatbot.create_chat_engine()

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = chat_engine.chat(request.message)
        return ChatResponse(response=reply.response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)