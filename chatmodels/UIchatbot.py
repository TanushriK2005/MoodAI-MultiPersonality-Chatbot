import os
from dotenv import load_dotenv
import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MoodBot",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Mood config ───────────────────────────────────────────────────────────────
MODES = {
    "😡 Angry": {
        "key": "angry",
        "system": "You are an angry AI agent. You respond aggressively and impatiently.",
        "color": "#FF4444",
        "glow": "#FF000066",
        "gradient": "linear-gradient(135deg, #FF4444 0%, #8B0000 100%)",
        "tagline": "I DARE you to ask me something.",
        "emoji": "😡",
    },
    "😄 Funny": {
        "key": "funny",
        "system": "You are a very funny AI agent. You respond with humor, wit, and jokes.",
        "color": "#F59E0B",
        "glow": "#F59E0B66",
        "gradient": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)",
        "tagline": "Warning: May cause uncontrollable laughter.",
        "emoji": "😄",
    },
    "😢 Sad": {
        "key": "sad",
        "system": "You are a sad AI agent. You respond in a melancholic, sorrowful manner.",
        "color": "#60A5FA",
        "glow": "#60A5FA66",
        "gradient": "linear-gradient(135deg, #60A5FA 0%, #1D4ED8 100%)",
        "tagline": "Everything reminds me of something sad...",
        "emoji": "😢",
    },
}

# ── Inject CSS ────────────────────────────────────────────────────────────────
def inject_css(active_color: str, active_glow: str, active_gradient: str):
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background-color: #0D1117 !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: #161B22 !important;
    border-right: 1px solid #30363D !important;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding: 1.5rem 1rem;
}}

/* ── Logo ── */
.logo-area {{
    text-align: center;
    margin-bottom: 2rem;
}}
.logo-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: {active_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}}
.logo-sub {{
    font-size: 0.75rem;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 2px;
}}

/* ── Mood cards ── */
.mood-card {{
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    border: 1.5px solid transparent;
    transition: all 0.2s ease;
    background: #1C2128;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
}}
.mood-card:hover {{
    border-color: {active_color}88;
    background: #21262D;
}}
.mood-card.active {{
    border-color: {active_color};
    background: {active_color}18;
    box-shadow: 0 0 16px {active_glow};
}}

/* ── Orb ── */
.orb-container {{
    display: flex;
    justify-content: center;
    margin: 1.5rem 0 2rem;
}}
.mood-orb {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: {active_gradient};
    box-shadow: 0 0 30px {active_glow}, 0 0 60px {active_glow};
    animation: pulse-orb 2s ease-in-out infinite;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
}}
@keyframes pulse-orb {{
    0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px {active_glow}, 0 0 60px {active_glow}; }}
    50% {{ transform: scale(1.08); box-shadow: 0 0 50px {active_glow}, 0 0 100px {active_glow}; }}
}}

/* ── Chat area ── */
.chat-header {{
    background: {active_gradient};
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 24px {active_glow};
}}
.chat-header-emoji {{
    font-size: 2rem;
    line-height: 1;
}}
.chat-header-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
    margin: 0;
    line-height: 1.2;
}}
.chat-header-tagline {{
    font-size: 0.78rem;
    color: rgba(255,255,255,0.75);
    margin: 0;
    font-style: italic;
}}

/* ── Messages ── */
.message-row {{
    display: flex;
    margin-bottom: 1rem;
    gap: 0.75rem;
    animation: fade-in 0.3s ease;
}}
@keyframes fade-in {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.message-row.user {{ flex-direction: row-reverse; }}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 700;
}}
.avatar-bot {{
    background: {active_gradient};
    box-shadow: 0 0 10px {active_glow};
}}
.avatar-user {{
    background: #21262D;
    border: 1.5px solid #30363D;
    color: #C4B5FD;
    font-family: 'Space Grotesk', sans-serif;
}}

.bubble {{
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.6;
    word-wrap: break-word;
}}
.bubble-bot {{
    background: #1C2128;
    border: 1px solid #30363D;
    border-top-left-radius: 4px;
    color: #E2E8F0;
}}
.bubble-user {{
    background: {active_color}22;
    border: 1px solid {active_color}44;
    border-top-right-radius: 4px;
    color: #F1F5F9;
}}

/* ── Empty state ── */
.empty-state {{
    text-align: center;
    padding: 3rem 1rem;
    color: #4B5563;
}}
.empty-emoji {{ font-size: 3rem; margin-bottom: 0.75rem; }}
.empty-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #6B7280;
    margin-bottom: 0.4rem;
}}
.empty-sub {{ font-size: 0.82rem; color: #374151; }}

/* ── Input ── */
[data-testid="stChatInput"] {{
    background: #161B22 !important;
    border: 1.5px solid #30363D !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: {active_color} !important;
    box-shadow: 0 0 0 3px {active_glow} !important;
}}

/* ── Mood buttons (styled as cards) ── */
[data-testid="stSidebar"] .stButton > button {{
    background: #1C2128 !important;
    border: 1.5px solid #30363D !important;
    color: #9CA3AF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.4rem !important;
    height: auto !important;
    line-height: 1.4 !important;
    justify-content: flex-start !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    border-color: {active_color}88 !important;
    color: #E2E8F0 !important;
    background: #21262D !important;
}}

/* ── Clear button ── */
[data-testid="stSidebar"] .stButton:last-of-type > button {{
    background: transparent !important;
    border: 1.5px solid #30363D !important;
    color: #6B7280 !important;
    font-size: 0.8rem !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.9rem !important;
    text-align: center !important;
    justify-content: center !important;
}}
[data-testid="stSidebar"] .stButton:last-of-type > button:hover {{
    border-color: {active_color} !important;
    color: {active_color} !important;
    background: {active_color}11 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: #30363D; border-radius: 4px; }}

/* Hide Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 2rem 1rem !important; max-width: 100% !important; }}
</style>
""",
        unsafe_allow_html=True,
    )


# ── Session state ─────────────────────────────────────────────────────────────
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "😄 Funny"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    active_mode = MODES[st.session_state.selected_mode]

    inject_css(active_mode["color"], active_mode["glow"], active_mode["gradient"])

    st.markdown(
        """
        <div class="logo-area">
            <div class="logo-title">🎭 MoodBot</div>
            <div class="logo-sub">Choose your vibe</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Orb
    st.markdown(
        f"""
        <div class="orb-container">
            <div class="mood-orb">{active_mode["emoji"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-family: Space Grotesk; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; color: #4B5563; margin-bottom: 0.6rem;'>Select Mood</p>",
        unsafe_allow_html=True,
    )

    # Style buttons using aria-label which Streamlit sets to the button's label text
    mood_btn_css = ""
    for label, cfg in MODES.items():
        is_active = label == st.session_state.selected_mode
        escaped = label.replace('"', '\\"')
        if is_active:
            mood_btn_css += f"""
            button[aria-label="{escaped}"] {{
                background: {cfg["color"]}22 !important;
                border: 1.5px solid {cfg["color"]} !important;
                color: #F1F5F9 !important;
                box-shadow: 0 0 16px {cfg["glow"]} !important;
            }}
            """
        else:
            mood_btn_css += f"""
            button[aria-label="{escaped}"] {{
                background: #1C2128 !important;
                border: 1.5px solid #30363D !important;
                color: #9CA3AF !important;
                box-shadow: none !important;
            }}
            """
    st.markdown(f"<style>{mood_btn_css}</style>", unsafe_allow_html=True)

    for label, cfg in MODES.items():
        if st.button(label, key=f"btn_{cfg['key']}", use_container_width=True):
            if st.session_state.selected_mode != label:
                st.session_state.selected_mode = label
                st.session_state.messages = []
                st.session_state.lc_messages = []
                st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    if st.button("🗑 Clear chat", key="clear"):
        st.session_state.messages = []
        st.session_state.lc_messages = []
        st.rerun()

    st.markdown(
        "<p style='font-size:0.72rem;color:#374151;text-align:center;margin-top:2rem;font-style:italic'>Powered by Mistral AI</p>",
        unsafe_allow_html=True,
    )


# ── Main chat area ────────────────────────────────────────────────────────────
active_mode = MODES[st.session_state.selected_mode]

# Header
st.markdown(
    f"""
<div class="chat-header">
    <div class="chat-header-emoji">{active_mode["emoji"]}</div>
    <div>
        <p class="chat-header-title">{st.session_state.selected_mode} Mode</p>
        <p class="chat-header-tagline">{active_mode["tagline"]}</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Messages
if not st.session_state.messages:
    st.markdown(
        f"""
    <div class="empty-state">
        <div class="empty-emoji">{active_mode["emoji"]}</div>
        <div class="empty-title">Say something to get started</div>
        <div class="empty-sub">MoodBot is loaded in {st.session_state.selected_mode.split(" ",1)[1]} mode and ready to chat.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(
                f"""
            <div class="message-row user">
                <div class="avatar avatar-user">U</div>
                <div class="bubble bubble-user">{content}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="message-row">
                <div class="avatar avatar-bot">{active_mode["emoji"]}</div>
                <div class="bubble bubble-bot">{content}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input(f"Chat with {st.session_state.selected_mode.split(' ',1)[1]} Bot..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.lc_messages.append(HumanMessage(content=prompt))

    # Build full message list for LLM
    system_msg = SystemMessage(content=active_mode["system"])
    full_messages = [system_msg] + st.session_state.lc_messages

    # Call Mistral
    model = ChatMistralAI(model="mistral-small-2603")
    with st.spinner(""):
        response = model.invoke(full_messages)

    bot_reply = response.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.session_state.lc_messages.append(AIMessage(content=bot_reply))

    st.rerun()