"""
EdTech Chatbot — Streamlit UI.

Run with:  streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

import chatbot as cb
import llm

load_dotenv()


st.set_page_config(
    page_title="EdTech Chatbot",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded",
)


CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');

    :root {
        --bg:        #f6f7fb;          /* main canvas */
        --card:      #ffffff;
        --ink:       #0d1430;          /* dark navy — signature accent */
        --ink-soft:  #2c3354;
        --mute:      #6b7090;
        --line:      #e6e8f0;
        --line-soft: #eef0f5;
        --peach:     #ff8c5e;          /* warm accent */
        --peach-bg:  #ffece2;
        --green:     #16a34a;
        --amber:     #f59e0b;
    }

    /* hide streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                     "Segoe UI", system-ui, sans-serif;
        color: var(--ink);
        font-feature-settings: "ss01", "cv11";
    }

    /* subtle grid pattern on main canvas */
    [data-testid="stMain"]::before {
        content: '';
        position: fixed;
        top: 0; bottom: 0; left: 220px; right: 0;
        pointer-events: none;
        background-image:
            linear-gradient(to right, rgba(13,20,48,0.045) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(13,20,48,0.045) 1px, transparent 1px);
        background-size: 32px 32px;
        z-index: 0;
    }
    .block-container {
        position: relative; z-index: 1;
        padding: 0 2rem 7rem;
        max-width: 880px;
    }

    /* ---- top toolbar (sticky) ---- */
    .toolbar {
        position: sticky;
        top: 0;
        z-index: 50;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 -2rem 1.2rem;
        padding: 1rem 2rem 0.9rem;
        background: rgba(246, 247, 251, 0.85);
        backdrop-filter: saturate(180%) blur(10px);
        -webkit-backdrop-filter: saturate(180%) blur(10px);
        border-bottom: 1px solid var(--line);
    }
    .toolbar .title-block .eyebrow {
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--mute);
        font-weight: 600;
        margin-bottom: 0.15rem;
    }
    .toolbar .title-block .title {
        font-family: 'Fraunces', Georgia, serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--ink);
        letter-spacing: -0.01em;
        line-height: 1;
    }
    .toolbar .actions {
        display: flex; gap: 8px; align-items: center;
    }
    .toolbar .actions .icon-btn {
        width: 36px; height: 36px;
        border-radius: 10px;
        background: var(--card);
        border: 1px solid var(--line);
        display: inline-flex; align-items: center; justify-content: center;
        color: var(--ink-soft);
        font-size: 1rem;
        cursor: default;
    }
    .toolbar .actions .icon-btn.alert {color: var(--peach);}
    .toolbar .actions .pill {
        padding: 6px 14px;
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 999px;
        font-size: 0.78rem;
        color: var(--ink-soft);
        font-weight: 500;
    }
    .toolbar .actions .pill .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--green);
        display: inline-block; margin-right: 6px;
        vertical-align: middle;
    }
    .toolbar .actions .pill.off .dot {background: var(--amber);}

    /* ---- sidebar — narrow, dark ---- */
    [data-testid="stSidebar"] {
        background: var(--ink);
        border-right: none;
        width: 248px !important;
        min-width: 248px !important;
    }
    [data-testid="stSidebar"] > div {
        background: var(--ink);
    }
    /* sidebar grid pattern */
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute; inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(to right, rgba(255,255,255,0.04) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.04) 1px, transparent 1px);
        background-size: 30px 30px;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 0.6rem 1rem 1.2rem;
        position: relative; z-index: 1;
    }
    [data-testid="stSidebar"] hr {display: none;}

    /* brand: mark + wordmark */
    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.2rem 0.2rem 0;
        margin-bottom: 1.4rem;
    }
    .brand .mark {
        width: 30px; height: 30px;
        border-radius: 8px;
        background: linear-gradient(135deg, #ffffff 0%, #e8eaf2 100%);
        color: var(--ink);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: -0.04em;
        flex-shrink: 0;
    }
    .brand .word {
        line-height: 1.1;
    }
    .brand .word .name {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #ffffff;
        letter-spacing: -0.01em;
    }
    .brand .word .name em {
        font-style: normal;
        color: var(--peach);
    }
    .brand .word .tag {
        font-size: 0.68rem;
        color: rgba(255,255,255,0.45);
        margin-top: 1px;
        letter-spacing: 0.02em;
    }

    .sb-section {
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: rgba(255,255,255,0.4);
        font-weight: 600;
        margin: 0.9rem 0 0.5rem 0.3rem;
    }

    .sb-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 1rem 0.1rem;
    }

    .sb-spacer {display: none;}

    /* sidebar primary button — "New conversation" */
    [data-testid="stSidebar"] .stButton button {
        background: var(--peach);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        text-align: center;
        font-size: 0.86rem;
        font-weight: 600;
        padding: 0.65rem 0.8rem !important;
        width: 100%;
        height: auto !important;
        min-height: 40px !important;
        margin-bottom: 0.4rem;
        box-shadow: 0 4px 12px -6px rgba(255,140,94,0.45);
        transition: all 0.15s ease;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: #ff7a45;
        color: #ffffff;
        box-shadow: 0 6px 16px -6px rgba(255,140,94,0.55);
        transform: translateY(-1px);
    }
    [data-testid="stSidebar"] .stButton button:active,
    [data-testid="stSidebar"] .stButton button:focus {
        background: var(--peach);
        color: #ffffff;
        box-shadow: 0 2px 6px -2px rgba(255,140,94,0.35);
    }

    /* model selector in sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        font-size: 0.82rem;
        min-height: 36px;
        color: #ffffff;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* sidebar profile (bottom) */
    .sb-profile {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
        margin-top: 1rem;
    }
    .sb-profile .top {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 0.8rem;
    }
    .sb-profile .avatar {
        width: 38px; height: 38px;
        border-radius: 9px;
        background: var(--peach-bg);
        color: #b54708;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Fraunces', serif;
        font-weight: 600; font-size: 1rem;
        position: relative;
    }
    .sb-profile .avatar::after {
        content: '';
        position: absolute;
        right: -3px; bottom: -3px;
        width: 12px; height: 12px;
        background: var(--peach);
        border: 2px solid var(--ink);
        border-radius: 50%;
    }
    .sb-profile .who .name {
        font-size: 0.85rem; font-weight: 600; color: #ffffff;
        line-height: 1.1;
    }
    .sb-profile .who .meta {
        font-size: 0.72rem; color: rgba(255,255,255,0.5);
        margin-top: 2px;
    }
    .sb-profile .stat {
        display: flex; justify-content: space-between;
        font-size: 0.74rem; padding: 0.2rem 0;
        color: rgba(255,255,255,0.7);
    }
    .sb-profile .stat .v {color: #ffffff; font-weight: 500;}
    .sb-profile .bar {
        height: 3px; background: rgba(255,255,255,0.08);
        border-radius: 99px; margin-top: 0.3rem; overflow: hidden;
    }
    .sb-profile .bar > span {
        display: block; height: 100%;
        background: var(--peach);
        border-radius: 99px;
    }

    /* ---- chat ---- */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0.45rem 0 !important;
        gap: 0.6rem;
    }

    /* assistant bubble — left tab */
    [data-testid="stChatMessageContent"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-left: 4px solid var(--ink);
        border-radius: 4px 14px 14px 14px;
        padding: 0.85rem 1.1rem !important;
        font-size: 0.93rem;
        line-height: 1.62;
        color: var(--ink);
        max-width: 78%;
        box-shadow: 0 2px 8px -4px rgba(13,20,48,0.06);
    }

    /* user bubble — right tab, right-aligned */
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        flex-direction: row-reverse;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"])
        [data-testid="stChatMessageContent"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-right: 4px solid var(--ink);
        border-left: 1px solid var(--line);
        border-radius: 14px 4px 14px 14px;
    }

    /* avatars — compact square frames */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        border-radius: 8px !important;
        flex-shrink: 0;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background: var(--peach-bg) !important;
        color: #b54708 !important;
        border: 1px solid var(--peach) !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background: var(--ink) !important;
        color: #ffffff !important;
        border: 1px solid var(--ink) !important;
    }
    [data-testid="stChatMessageAvatarUser"] svg,
    [data-testid="stChatMessageAvatarAssistant"] svg,
    [data-testid="stChatMessageAvatarUser"] [data-testid="stIconMaterial"],
    [data-testid="stChatMessageAvatarAssistant"] [data-testid="stIconMaterial"] {
        font-size: 16px !important;
        width: 16px !important;
        height: 16px !important;
    }

    /* tables */
    [data-testid="stChatMessageContent"] table {
        border-collapse: collapse;
        margin: 0.6rem 0 0.2rem 0;
        font-size: 0.86rem; width: 100%;
    }
    [data-testid="stChatMessageContent"] th {
        color: var(--mute);
        font-weight: 600;
        padding: 0.4rem 0.6rem;
        text-align: left;
        border-bottom: 1px solid var(--line);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="stChatMessageContent"] td {
        padding: 0.5rem 0.6rem;
        border-bottom: 1px solid var(--line-soft);
    }
    [data-testid="stChatMessageContent"] tr:last-child td {border-bottom: none;}
    [data-testid="stChatMessageContent"] code {
        background: #f0f1f5;
        color: var(--ink);
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular,
                     Menlo, monospace;
    }
    [data-testid="stChatMessageContent"] blockquote {
        border-left: 3px solid var(--peach);
        background: var(--peach-bg);
        margin: 0.7rem 0;
        padding: 0.55rem 0.85rem;
        color: #7c2d12;
        border-radius: 0 6px 6px 0;
        font-size: 0.88rem;
    }
    [data-testid="stChatMessageContent"] strong {
        color: var(--ink); font-weight: 600;
    }

    /* caption under reply */
    .stCaption, .stCaption p, [data-testid="stCaptionContainer"] p {
        color: var(--mute) !important;
        font-size: 0.71rem !important;
        font-weight: 500 !important;
        margin-top: 0.4rem !important;
        letter-spacing: 0.02em;
    }

    /* ---- compact chips (above the input) ---- */
    [data-testid="stMain"] .stButton button {
        background: var(--card);
        color: var(--ink-soft);
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.32rem 0.7rem !important;
        font-size: 0.78rem;
        font-weight: 500;
        text-align: center;
        height: auto; min-height: 0 !important; line-height: 1.3;
        transition: all 0.12s ease;
    }
    [data-testid="stMain"] .stButton button:hover {
        background: var(--ink);
        border-color: var(--ink);
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px -6px rgba(13,20,48,0.25);
    }
    /* chip row — pinned just above the chat input, identified by key */
    [data-testid="stHorizontalBlock"]:has(.st-key-chip_Courses) {
        position: fixed !important;
        bottom: 96px !important;
        left: 248px !important;
        right: 0 !important;
        max-width: 880px !important;
        margin: 0 auto !important;
        padding: 1rem 2rem 0.4rem !important;
        gap: 8px !important;
        z-index: 40;
        background: linear-gradient(to top,
                    var(--bg) 65%, rgba(246,247,251,0)) !important;
    }
    .chip-row-anchor {display: none;}

    /* chat input — compact, sits at bottom of main area */
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottom"] > div {
        background: transparent !important;
        padding: 0 !important;
        max-width: 880px !important;
        margin: 0 auto !important;
    }
    [data-testid="stChatInput"] {
        background: var(--card) !important;
        padding: 0 !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
        margin: 0.4rem 2rem 0.8rem !important;
        max-width: 880px !important;
        box-shadow: 0 6px 20px -14px rgba(13,20,48,0.15);
        overflow: hidden;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--ink) !important;
        box-shadow: 0 6px 20px -10px rgba(13,20,48,0.22) !important;
    }
    [data-testid="stChatInput"] > div {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stChatInput"] textarea {
        border: none !important;
        border-radius: 14px !important;
        font-size: 0.93rem !important;
        background: transparent !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.85rem 1rem !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        box-shadow: none !important;
    }
    [data-testid="stChatInputSubmitButton"],
    [data-testid="stChatInput"] button {
        background: var(--ink) !important;
        color: #ffffff !important;
        border-radius: 9px !important;
        margin-right: 6px !important;
    }
    [data-testid="stChatInputSubmitButton"] svg,
    [data-testid="stChatInput"] button svg {color: #ffffff !important;}

    /* spinner */
    [data-testid="stSpinner"] > div {
        border-top-color: var(--ink) !important;
        border-right-color: var(--ink) !important;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def _init_state():
    if "messages" not in st.session_state:
        first_name = cb.STUDENT["name"].split()[0]
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"Welcome back, **{first_name}**. I can pull up your "
                    f"courses, grades, attendance, fees and assignments — "
                    f"or help you think through something more open-ended."
                ),
            }
        ]
    if "model" not in st.session_state:
        st.session_state.model = llm.DEFAULT_MODEL


_init_state()


with st.sidebar:
    st.markdown(
        '<div class="brand">'
        '<div class="mark">ed</div>'
        '<div class="word">'
        '<div class="name">EdTech<em>.</em></div>'
        '<div class="tag">Academic assistant</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button("+  New conversation", key="new_chat"):
        st.session_state.messages = []
        _init_state()
        st.rerun()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">AI Model</div>',
                unsafe_allow_html=True)
    MODEL_LABELS = {
        "llama-3.3-70b-versatile": "Llama 3.3 · 70B",
        "llama-3.1-8b-instant":    "Llama 3.1 · 8B",
    }
    st.session_state.model = st.selectbox(
        "Model",
        options=list(MODEL_LABELS.keys()),
        index=0,
        format_func=lambda k: MODEL_LABELS[k],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sb-divider" '
                'style="margin-top:1.2rem;"></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sb-section">Student</div>',
                unsafe_allow_html=True)

    total_attended = sum(a for _, a, _ in cb.ATTENDANCE)
    total_classes = sum(t for _, _, t in cb.ATTENDANCE)
    overall_pct = total_attended / total_classes * 100
    pending = sum(1 for _, _, _, s in cb.ASSIGNMENTS if s == "Pending")
    initial = cb.STUDENT["name"][0].upper()

    st.markdown(
        f"""
        <div class="sb-profile">
            <div class="top">
                <div class="avatar">{initial}</div>
                <div class="who">
                    <div class="name">{cb.STUDENT['name']}</div>
                    <div class="meta">{cb.STUDENT['roll_no']} · Sem {cb.STUDENT['semester']}</div>
                </div>
            </div>
            <div class="stat">
                <span>Attendance</span><span class="v">{overall_pct:.1f}%</span>
            </div>
            <div class="bar"><span style="width:{overall_pct:.0f}%"></span></div>
            <div class="stat" style="margin-top:0.5rem;">
                <span>Pending tasks</span><span class="v">{pending}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if llm.is_configured():
    pill_html = ('<span class="pill"><span class="dot"></span>'
                 'Llama 3.3 · ready</span>')
else:
    pill_html = ('<span class="pill off"><span class="dot"></span>'
                 'Rule-based mode</span>')

st.markdown(
    f"""
    <div class="toolbar">
        <div class="title-block">
            <div class="eyebrow">Academic assistant</div>
            <div class="title">Your study companion.</div>
        </div>
        <div class="actions">
            {pill_html}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("source"):
            st.caption(msg["source"])


CHIPS = [
    ("Courses",     "courses"),
    ("Grades",      "grades"),
    ("Attendance",  "attendance"),
    ("Fees",        "fees"),
    ("Assignments", "assignments"),
    ("Status",      "status"),
]

with st.container():
    st.markdown('<div class="chip-row-anchor"></div>',
                unsafe_allow_html=True)
    chip_cols = st.columns(len(CHIPS))
    for col, (label, query) in zip(chip_cols, CHIPS):
        if col.button(label, key=f"chip_{label}",
                      use_container_width=True):
            st.session_state._pending_input = query
            st.rerun()

pending_input = st.session_state.pop("_pending_input", None)
prompt = st.chat_input("Type a new message here")
if pending_input and not prompt:
    prompt = pending_input


def _build_history_for_llm():
    msgs = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[1:]
    ]
    return msgs[-6:]


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            intent, response = cb.get_response(prompt)
            if intent == "unknown":
                response = llm.ask_llm(
                    prompt,
                    history=_build_history_for_llm(),
                    model=st.session_state.model,
                )
                source = "AI · Llama 3.3"
            elif intent in ("greet", "thanks", "empty", "exit"):
                source = ""
            else:
                source = "Rule-based"
        st.markdown(response)
        if source:
            st.caption(source)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "source": source,
    })
