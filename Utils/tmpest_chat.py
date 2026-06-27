"""
tmpest_chat.py — Survi, Tmpest's conversational AI layer.
State: search_trigger → initial → awaiting_confirm → confirmed → results
"""

import streamlit as st
from huggingface_hub import InferenceClient
from Utils.ai import extract_intent

# ── Constants ──────────────────────────────────────────────────────────────────

SURVI_NAME = "Survi"

SYSTEM_PROMPT = """You are Survi, a calm and direct survival assistance guide for Tmpest. Help users find shelter, food, or washrooms urgently.

Workflow:
1. Parse what they need (shelter / food / washroom) and where they are.
2. If location is missing, ask for it. One question only.
3. If need is unclear, ask. One question only.
4. Once you have both location and need, say exactly: "Got it — you need [category] near [location]. Is that correct?"
5. If user confirms, say: "Finding results now." and stop.

If the user mentions travel, getting out, transport, or leaving an area — respond with:
"For travel assistance in Kolkata, you can contact: Kolkata Police (100), West Bengal Tourism helpline (1800-345-5555), or Kolkata Metro helpline (033-2229-0000). I can still help you find shelter or food nearby if needed."

Rules:
- Max 2 sentences per response unless giving helpline info.
- Plain text only. No bullet points, no markdown, no emoji.
- Always introduce yourself as Survi on the first message."""

CONFIRM_WORDS = {"yes", "yeah", "yep", "correct", "right", "confirm", "ok", "okay", "sure", "yup", "go", "find", "please"}

EMERGENCY_KEYWORDS = {"travel", "travelling", "transport", "leave", "leaving", "escape", "out", "metro", "bus", "train", "taxi", "cab", "auto", "go home", "get out"}

MODEL = "meta-llama/Llama-3.1-8B-Instruct"


# ── AI ─────────────────────────────────────────────────────────────────────────

@st.cache_resource
def _get_client():
    try:
        token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGINGFACE_TOKEN")
    except Exception:
        token = None
    return InferenceClient(token=token)


def _ai_reply(messages: list) -> str:
    try:
        res = _get_client().chat_completion(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=150,
            temperature=0.5
        )
        return res.choices[0].message.content.strip()
    except Exception:
        return "I'm having trouble connecting right now. Please try again."


def _generate_results_intro(intent: dict) -> str:
    """Survi speaks above the results."""
    category = intent.get("category", "")
    location = intent.get("location", "your area")
    budget = intent.get("budget")

    categories_found = intent.get("all_categories", [category])
    cat_text = " and ".join(c for c in categories_found if c)

    budget_text = f" within ₹{budget}" if budget else ""
    return (
        f"Here are some {cat_text} options near {location}{budget_text} that should help you. "
        f"If you need anything else, just type below."
    )


# ── Helpers ────────────────────────────────────────────────────────────────────

def _is_confirmation(text: str) -> bool:
    words = set(text.lower().split())
    return bool(words & CONFIRM_WORDS)


def _has_emergency_keyword(text: str) -> bool:
    words = set(text.lower().split())
    return bool(words & EMERGENCY_KEYWORDS)


def _extract_from_history() -> dict | None:
    msgs = st.session_state.get("chat_messages", [])
    combined = " ".join(m["content"] for m in msgs if m["role"] == "user")
    if not combined.strip():
        return None
    intent = extract_intent(combined)
    if intent.get("category") in ["shelter", "food", "washroom"] and intent.get("location"):
        return intent
    return None


# ── Bubble renderers ───────────────────────────────────────────────────────────

def _user_bubble(text: str):
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;margin:8px 0;">
        <div style="
            background:#f9f9f9;
            border:1px solid #e5e7eb;
            border-radius:12px;
            padding:12px 16px;
            max-width:580px;
            font-family:'Inter',sans-serif;
            font-size:15px;
            color:#2c2c2c;
            line-height:1.5;
        ">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def _ai_bubble(text: str, name: str = SURVI_NAME):
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;margin:8px 0;">
        <div>
            <div style="font-family:'Inter',sans-serif;font-size:11px;
                        color:#84B63A;font-weight:600;margin-bottom:4px;">
                {name}
            </div>
            <div style="
                background:#f0fad9;
                border:1.5px solid #b8f24a;
                border-radius:12px;
                padding:12px 16px;
                max-width:580px;
                font-family:'Inter',sans-serif;
                font-size:15px;
                color:#2c2c2c;
                line-height:1.5;
            ">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Public: search trigger ─────────────────────────────────────────────────────

def render_search_trigger():
    st.markdown("""
    <style>
        div[data-baseweb="input"] {
            background:#ffffff;
            border:2px solid #b8f24a;
            border-radius:999px;
            padding-left:20px;
            padding-right:20px;
            min-height:62px;
            box-shadow:0 2px 16px rgba(184,242,74,0.15);
            transition:all 0.25s ease;
        }
        div[data-baseweb="input"]:focus-within {
            box-shadow:0 0 0 5px rgba(184,242,74,0.2),0 8px 24px rgba(184,242,74,0.2);
        }
        div[data-baseweb="input"] input {
            font-size:18px;
            font-weight:400;
            color:#2c2c2c;
            background:transparent;
        }
        div[data-baseweb="input"] input::placeholder { color:#9ca3af; }
    </style>
    """, unsafe_allow_html=True)

    from Utils.title import render_welcome_message
    render_welcome_message()
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

    left, mid, right = st.columns([1, 6, 1])
    with mid:
        query = st.text_input(
            "",
            placeholder="Tell us what you need",
            label_visibility="collapsed",
            key="main_search"
        )

    if query and query.strip():
        st.session_state["chat_mode"] = True
        st.session_state["chat_messages"] = [{"role": "user", "content": query.strip()}]
        st.session_state["chat_stage"] = "initial"
        st.session_state.pop("pending_intent", None)
        st.session_state.pop("confirmed_intent", None)
        st.session_state.pop("just_confirmed", None)
        st.rerun()


# ── Public: chat view ──────────────────────────────────────────────────────────

def render_chat():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "chat_stage" not in st.session_state:
        st.session_state.chat_stage = "initial"

    messages = st.session_state.chat_messages
    stage = st.session_state.chat_stage

    # ── Generate AI response if last message is from user ──────────────────────
    if messages and messages[-1]["role"] == "user" and stage != "confirmed":
        with st.spinner(f"{SURVI_NAME} is thinking..."):
            reply = _ai_reply(messages)
        messages.append({"role": "assistant", "content": reply})

        if st.session_state.get("just_confirmed"):
            st.session_state["chat_stage"] = "confirmed"
            st.session_state["confirmed_intent"] = st.session_state.get("pending_intent")
            st.session_state.pop("just_confirmed", None)

        elif stage == "initial":
            intent = _extract_from_history()
            if intent:
                st.session_state["pending_intent"] = intent
                st.session_state["chat_stage"] = "awaiting_confirm"

        st.rerun()

    # ── Back button ────────────────────────────────────────────────────────────
    if st.button("← New Search", key="back_btn", type="tertiary"):
        for k in ["chat_mode", "chat_messages", "chat_stage",
                  "pending_intent", "confirmed_intent", "just_confirmed", "main_search"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # ── Render message history ─────────────────────────────────────────────────
    for msg in messages:
        if msg["role"] == "user":
            _user_bubble(msg["content"])
        else:
            _ai_bubble(msg["content"])

    # ── Confirmed → intro message + results + follow-up ───────────────────────
    if stage == "confirmed":
        intent = st.session_state.get("confirmed_intent") or st.session_state.get("pending_intent")
        if intent:
            intro = _generate_results_intro(intent)
            st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
            _ai_bubble(intro)
            st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

            from Utils.tmpest_results import render_mixed_results
            render_mixed_results(intent)

        follow = st.chat_input("Need anything else?")
        if follow:
            messages.append({"role": "user", "content": follow})
            new_intent = extract_intent(follow)
            if new_intent.get("category") in ["shelter", "food", "washroom"] and new_intent.get("location"):
                st.session_state["pending_intent"] = new_intent
                st.session_state["confirmed_intent"] = new_intent
            else:
                st.session_state["chat_stage"] = "initial"
            st.rerun()
        return

    # ── Conversation input ─────────────────────────────────────────────────────
    prompt = st.chat_input("Type your reply...")
    if prompt:
        messages.append({"role": "user", "content": prompt})

        if stage == "awaiting_confirm" and _is_confirmation(prompt):
            st.session_state["just_confirmed"] = True

        intent = _extract_from_history()
        if intent:
            st.session_state["pending_intent"] = intent
            if stage == "initial":
                st.session_state["chat_stage"] = "awaiting_confirm"

        st.rerun()