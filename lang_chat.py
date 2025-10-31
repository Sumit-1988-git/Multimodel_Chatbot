from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI  # or OpenAI

from typing import Optional
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (local) or Streamlit secrets (deployed)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found in Streamlit Secrets or .env file.")

app = FastAPI(
    title="LangChain ChatBot API",
    description="A conversational AI chatbot using LangChain and OpenAI",
    version="1.1.0"
)

conversation_chain: Optional[ConversationChain] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class OpenAIChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)

    def create_conversation(self) -> ConversationChain:
        memory = ConversationBufferMemory()
        return ConversationChain(llm=self.llm, memory=memory, verbose=True)

chatbot = OpenAIChatbot()
conversation_chain = chatbot.create_conversation()

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = conversation_chain.predict(input=request.message)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)