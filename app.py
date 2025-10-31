import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for funky styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    .user-message {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: 15px;
        padding: 12px;
        margin: 5px 0;
        color: white;
        text-align: right;
    }
    .bot-message {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 15px;
        padding: 12px;
        margin: 5px 0;
        color: white;
    }
    .model-selector {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 15px;
    }
    .stButton button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.warning("⚠️ No API key found. Please set it in Streamlit Secrets.")
else:
    st.success("🗝️ API key loaded successfully.")

# API endpoints
LANGCHAIN_API = "http://localhost:8000/api/chat"
LLAMAINDEX_API = "http://localhost:8001/api/chat"

class ChatBotApp:
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_model' not in st.session_state:
            st.session_state.current_model = "LangChain"
        if 'api_status' not in st.session_state:
            st.session_state.api_status = {
                "LangChain": "Unknown",
                "LlamaIndex": "Unknown"
            }

    def check_api_status(self):
        """Check if APIs are running"""
        try:
            response = requests.get(LANGCHAIN_API.replace("/api/chat", "/docs"), timeout=2)
            st.session_state.api_status["LangChain"] = "🟢 Online" if response.status_code == 200 else "🔴 Offline"
        except:
            st.session_state.api_status["LangChain"] = "🔴 Offline"
        
        try:
            response = requests.get(LLAMAINDEX_API.replace("/api/chat", "/docs"), timeout=2)
            st.session_state.api_status["LlamaIndex"] = "🟢 Online" if response.status_code == 200 else "🔴 Offline"
        except:
            st.session_state.api_status["LlamaIndex"] = "🔴 Offline"

    def send_message(self, message, model_type):
        """Send message to the appropriate API"""
        api_url = LANGCHAIN_API if model_type == "LangChain" else LLAMAINDEX_API
        
        try:
            response = requests.post(api_url, json={"message": message}, timeout=30)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Error: API returned status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            return f"❌ Error: Cannot connect to {model_type} API. Make sure the server is running on port {8000 if model_type == 'LangChain' else 8001}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def display_header(self):
        """Display the funky header"""
        st.markdown('<div class="main-header">🎉 Funky AI ChatBot 🎉</div>', unsafe_allow_html=True)
        
        # Funky subtitle
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
            Choose your AI model and start chatting! ✨
        </div>
        """, unsafe_allow_html=True)

    def display_sidebar(self):
        """Display the sidebar with model selection and info"""
        with st.sidebar:
            st.markdown('<div class="model-selector">', unsafe_allow_html=True)
            
            st.markdown("### 🤖 Model Selection")
            
            # Model selection with emojis
            model_option = st.radio(
                "Choose your AI model:",
                ["LangChain", "LlamaIndex"],
                index=0 if st.session_state.current_model == "LangChain" else 1,
                key="model_selector"
            )
            
            if model_option != st.session_state.current_model:
                st.session_state.current_model = model_option
                st.session_state.messages = []  # Clear conversation when switching models
                st.rerun()
            
            st.markdown("---")
            
            # API Status
            st.markdown("### 📊 API Status")
            self.check_api_status()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("LangChain", st.session_state.api_status["LangChain"])
            with col2:
                st.metric("LlamaIndex", st.session_state.api_status["LlamaIndex"])
            
            st.markdown("---")
            
            # Conversation info
            st.markdown("### 💬 Conversation Info")
            st.write(f"Messages: **{len(st.session_state.messages)}**")
            st.write(f"Current Model: **{st.session_state.current_model}**")
            
            # Clear conversation button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            st.markdown("---")
            
            # Fun facts
            st.markdown("### 🎯 Did You Know?")
            fun_facts = [
                "LangChain is great for complex reasoning!",
                "LlamaIndex excels at document processing!",
                "Both models use GPT-3.5-turbo!",
                "You can switch models anytime!",
                "The chat history is preserved! 🎉"
            ]
            st.info(fun_facts[len(st.session_state.messages) % len(fun_facts)])
            
            st.markdown('</div>', unsafe_allow_html=True)

    def display_chat(self):
        """Display the chat interface"""
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {message["content"]}
                        <br><small>{message["timestamp"]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="bot-message">
                        <strong>🤖 {message["model"]}:</strong> {message["content"]}
                        <br><small>{message["timestamp"]}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Type your message here...",
                key="user_input",
                label_visibility="collapsed",
                placeholder=f"Ask me anything using {st.session_state.current_model}..."
            )
        with col2:
            send_button = st.button("Send 🚀", use_container_width=True)
        
        # Handle user input
        if (send_button or user_input) and user_input.strip():
            # Add user message to chat
            user_message = {
                "role": "user",
                "content": user_input.strip(),
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "model": st.session_state.current_model
            }
            st.session_state.messages.append(user_message)
            
            # Get bot response
            with st.spinner(f"🤖 {st.session_state.current_model} is thinking..."):
                bot_response = self.send_message(user_input.strip(), st.session_state.current_model)
            
            # Add bot response to chat
            bot_message = {
                "role": "assistant",
                "content": bot_response,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "model": st.session_state.current_model
            }
            st.session_state.messages.append(bot_message)
            
            # Clear input and rerun
            st.session_state.user_input = ""
            st.rerun()

    def run(self):
        """Run the main application"""
        self.display_header()
        self.display_sidebar()
        self.display_chat()

# Run the application
if __name__ == "__main__":
    # Display startup message
    with st.spinner("🚀 Starting Funky ChatBot..."):
        time.sleep(1)
    
    app = ChatBotApp()
    app.run()