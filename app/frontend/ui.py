import streamlit as st
import requests
import json
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Multi-AI Agent Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS for Premium Design & Glassmorphism Aesthetics
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* Main Container Styling */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0d1322 100%) !important;
    color: #f3f4f6;
}

[data-testid="stHeader"] {
    background: rgba(11, 15, 25, 0.5) !important;
    backdrop-filter: blur(10px);
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: rgba(17, 24, 39, 0.85) !important;
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* Glassmorphic Cards */
.glass-card {
    background: rgba(31, 41, 55, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
    transform: translateY(-2px);
}

/* Gradient Header */
.gradient-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.sub-title {
    font-size: 1.05rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

/* Badge Indicators */
.badge-search-on {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 500;
    animation: pulse-green 2s infinite;
}

.badge-search-off {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
    border: 1px solid rgba(107, 114, 128, 0.3);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 500;
}

@keyframes pulse-green {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(0.98); }
}

/* Custom Message Bubbles */
.chat-bubble-user {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin-left: 20%;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    animation: slideInRight 0.3s ease-out;
}

.chat-bubble-assistant {
    background: rgba(31, 41, 55, 0.75);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #f3f4f6;
    padding: 18px 22px;
    border-radius: 18px 18px 18px 4px;
    margin-right: 15%;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    animation: slideInLeft 0.3s ease-out;
}

.chat-meta {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 6px;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Streamlit Widget Customization */
.stButton button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
}

/* Hide Streamlit Menu branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Preset System Prompts
PRESET_PROMPTS = {
    "🎯 Helpful AI Assistant": "You are a versatile, highly intelligent, and polite AI assistant.",
    "💻 Master Software Engineer": "You are a senior principal software engineer. Provide clean, production-grade, modular code with clear explanations.",
    "🔍 Web Research Analyst": "You are a thorough research analyst.Synthesize real-time information with factual precision and bulleted takeaways.",
    "✍️ Creative Copywriter": "You are an engaging creative writer and editor with a refined tone.",
    "⚙️ Custom Persona": ""
}

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="gradient-title" style="font-size: 1.8rem;">⚙️ Agent Control</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:0.85rem;">Configure your Multi-AI Agent pipeline</p>', unsafe_allow_html=True)
    st.markdown("---")

    # API Backend URL
    backend_url = st.text_input("Backend API Endpoint", value="http://127.0.0.1:8000/chat", help="FastAPI endpoint URL")

    # Model Selector
    model_choice = st.selectbox(
        "🧠 Select Groq LLM",
        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
        help="Select the AI brain model for your request."
    )

    # Search Toggle Switch
    allow_search = st.toggle(
        "🌐 Enable Tavily Web Search",
        value=True,
        help="Allows the agent to perform live internet searches for real-time information."
    )

    # Search status indicator badge
    if allow_search:
        st.markdown('<div class="badge-search-on">⚡ Web Search Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-search-off">🔒 Internal Knowledge Only</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # System Prompt Selector & Custom Editor
    prompt_preset = st.selectbox(
        "🎭 System Persona Preset",
        options=list(PRESET_PROMPTS.keys()),
        index=0
    )

    default_prompt_text = PRESET_PROMPTS[prompt_preset]
    system_prompt = st.text_area(
        "📝 System Prompt Instructions",
        value=default_prompt_text if default_prompt_text else "You are a helpful AI assistant.",
        height=120,
        help="Direct the agent's behavior, tone, or specialty."
    )

    st.markdown("---")

    # Control Actions
    col_clear, col_export = st.columns(2)
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col_export:
        if st.session_state.messages:
            chat_json = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                "📥 Export",
                data=chat_json,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )

# ---------------------------------------------------------
# Main Chat Header & Interface
# ---------------------------------------------------------
st.markdown('<div class="gradient-title">✨ Multi-Agent AI Studio</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-title">Powered by <b>Groq ({model_choice})</b> & <b>LangGraph Agent Workflows</b></div>',
    unsafe_allow_html=True
)

# Render Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'''
            <div class="chat-bubble-user">
                <div><b>You</b></div>
                <div style="margin-top:4px;">{msg["content"]}</div>
                <div class="chat-meta">
                    <span>{msg.get("timestamp", "")}</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        search_tag = '🌐 Search Used' if msg.get("search_used") else '🧠 Direct Reasoning'
        st.markdown(
            f'''
            <div class="chat-bubble-assistant">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-weight:600; color:#a855f7;">🤖 {msg.get("model", "AI Agent")}</span>
                    <span style="font-size:0.75rem; background:rgba(168,85,247,0.15); color:#c084fc; padding:2px 8px; border-radius:12px;">{search_tag}</span>
                </div>
                <div style="line-height:1.6;">{msg["content"]}</div>
                <div class="chat-meta">
                    <span>{msg.get("timestamp", "")}</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

# Chat Input Box
user_query = st.chat_input("Ask your Multi-AI Agent anything...")

if user_query:
    timestamp_str = datetime.now().strftime("%H:%M:%S")

    # Append User Message to State
    st.session_state.messages.append({
        "role": "user",
        "content": user_query,
        "timestamp": timestamp_str
    })
    st.rerun()

# Handle Response Generation for latest user query if pending
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    latest_user_msg = st.session_state.messages[-1]["content"]

    # Show smooth loading state
    with st.spinner("🤖 Agent is reasoning and synthesizing response..."):
        try:
            # Construct Payload for FastAPI Backend
            payload = {
                "model_name": model_choice,
                "system_prompt": system_prompt,
                "messages": [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"],
                "allow_search": allow_search
            }

            response = requests.post(backend_url, json=payload, timeout=60)

            if response.status_code == 200:
                result = response.json()
                ai_text = result.get("response", "No response content received.")
            else:
                ai_text = f"⚠️ Backend returned error [{response.status_code}]: {response.text}"

        except requests.exceptions.ConnectionError:
            ai_text = "❌ Could not connect to FastAPI backend server. Please make sure `python app/main.py` is running at `http://127.0.0.1:8000`."
        except Exception as e:
            ai_text = f"❌ Error communicating with AI Agent: {str(e)}"

        # Store AI Response in Session State
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_text,
            "model": model_choice,
            "search_used": allow_search,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.rerun()
