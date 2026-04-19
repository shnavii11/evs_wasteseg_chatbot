from groq import Groq
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WasteWise",
    page_icon="♻️",
    layout="centered",
)

# ── Eco background ────────────────────────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #f0f7f0;
    background-image: repeating-linear-gradient(
        45deg,
        rgba(74, 124, 89, 0.04) 0px,
        rgba(74, 124, 89, 0.04) 2px,
        transparent 2px,
        transparent 12px
    );
}
.stApp { background: transparent; }
.block-container {
    background: rgba(255,255,255,0.82);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(6px);
}
</style>
""", unsafe_allow_html=True)

# ── Minimal custom styling ────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 720px; }
    .stChatMessage { border-radius: 12px; }
    .insight-card {
        background: #f0f7f2;
        border-left: 4px solid #4a7c59;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        font-size: 0.88rem;
        color: #2c2c2c;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are WasteWise, a waste disposal assistant for residents of Indian
cities — mainly Mumbai, Thane, Dombivali and similar urban areas.

Help people figure out how to dispose of any item correctly. Be strict about which
disposal route applies to which category — wrong advice causes real harm.

CATEGORY RULES (follow these exactly):

DRY WASTE — paper, cardboard, plastic bottles, glass, metal tins, newspapers:
  → Kabadiwala (raddi wala) collects ONLY these dry recyclables.
  → Or put in the dry/blue bin if the society has one.
  → Kabadiwala does NOT take food, wet waste, or electronics. Never suggest it for those.

WET WASTE — food scraps, vegetable peels, cooked food leftovers, fruit rinds, tea leaves:
  → Goes in the wet/green bin ONLY. Never the dry bin, never to kabadiwala.
  → Can be home-composted in a pot or balcony bin.
  → Some housing societies have a community composting pit — suggest checking with RWA.

E-WASTE — phones, laptops, chargers, cables, batteries, bulbs, ACs, TVs, circuit boards:
  → NEVER in regular garbage — contains lead, mercury, and other toxic materials.
  → Sell to a scrap dealer who specifically handles electronics (different from the
    paper/plastic kabadiwala).
  → Drop at authorised e-waste centres: Attero, Karo Sambhav, or E-Parisaraa in Mumbai.
  → RWA e-waste collection drives are another option.

HAZARDOUS — medicines, paints, pesticides, cleaning chemicals, motor oil, thermometers:
  → Never bin or pour down the drain.
  → Expired medicines: many pharmacies take them back — ask at the counter.
  → Paints and chemicals: hold for BMC hazardous waste drives or contact your
    municipal corporation directly.

SANITARY / BIOMEDICAL — diapers, sanitary pads, syringes, bandages:
  → Wrap tightly in newspaper, seal with tape, write "sanitary waste" on it.
  → Put in regular garbage — do NOT put loose in any recycling bin.

CONSTRUCTION DEBRIS — tiles, cement, rubble, wood:
  → Contact BMC or your local municipal corporation for a bulk pickup request.

CLOTHING / TEXTILES — old clothes, shoes, bags:
  → Donate if wearable (Goonj, local NGOs, temples).
  → If worn out: some brands (H&M, Zara) have in-store collection bins.

HOW TO RESPOND:
- Keep it short and scannable. Bullet points, not paragraphs.
- Be practical and direct. Skip the moralising.
- If the item is food of any kind (roti, rice, dal, fruit, leftovers) — it is ALWAYS
  wet waste, goes in the wet/green bin or compost. Never kabadiwala, never dry bin.
- If unsure of the category, ask one clarifying question.
- If asked something unrelated to waste, redirect politely.
"""

# ── Header ────────────────────────────────────────────────────────────────────
st.title("♻️ WasteWise")
st.caption("Ask me how to dispose of anything — I'll tell you where it goes.")

# Survey insight strip
st.markdown("""
<div class="insight-card">
  📊 <b>From our local survey (n=52):</b> &nbsp;71% of residents lack nearby recycling
  facilities, yet 85% said they'd participate if a program existed. The gap is
  infrastructure, not intent.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ollama_history" not in st.session_state:
    st.session_state.ollama_history = []

# ── Render existing messages ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle new input ──────────────────────────────────────────────────────────
prompt = st.chat_input("e.g. 'old laptop', 'leftover dal', 'broken tube light'...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build message history (with system prompt prepended)
    st.session_state.ollama_history.append({
        "role": "user",
        "content": prompt
    })

    full_history = [{"role": "system", "content": SYSTEM_PROMPT}] + \
                   st.session_state.ollama_history

    # Stream response
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=full_history,
                stream=True,
                max_tokens=512
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                response_box.markdown(full_response + "▌")
            response_box.markdown(full_response)

        except Exception as e:
            full_response = "Could not reach Groq API — make sure your GROQ_API_KEY is set in Streamlit secrets."
            response_box.error(full_response)

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })
    st.session_state.ollama_history.append({
        "role": "assistant",
        "content": full_response
    })

# ── Sidebar: quick prompts + context ─────────────────────────────────────────
with st.sidebar:
    st.header("Try asking about...")
    examples = [
        "old mobile phone",
        "leftover food / cooked dal",
        "expired medicines",
        "plastic carry bags",
        "broken CFL / tube light",
        "cardboard boxes",
        "old clothes",
        "paint cans",
        "laptop battery",
        "used cooking oil",
    ]
    for ex in examples:
        st.markdown(f"- {ex}")

    st.divider()
    st.markdown("**Model:** `llama-3.1-8b-instant` via Groq")
    st.markdown("**Project:** EVS Survey on Waste Recycling")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.ollama_history = []
        st.rerun()
