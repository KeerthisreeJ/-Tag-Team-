import streamlit as st
from groq import Groq
from pinecone import Pinecone
import requests
import datetime

# Initialize Groq and Pinecone clients
client = Groq(api_key="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")
pc = Pinecone(api_key="b311901d-a6a4-4b0a-a292-9431183d5623")
index = pc.Index("quickstart")

# Set the API key in session state
st.session_state.api_key = "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"


st.markdown("""
    <style>
    .stChatMessage .user { color: #ffffff; background-color: #1abc9c; padding: 10px; border-radius: 10px; }
    .stChatMessage .assistant { color: #ffffff; background-color: #3498db; padding: 10px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='color: #27ae60; text-align: center'>🩺 MediChat: Your AI Medical Companion</h1>
<p style='color: #27ae60; text-align: center'>Think of me as your health buddy 🤖💬 — here to chat, care, and guide you!</p>
<hr>
""", unsafe_allow_html=True)

#Mood Tracker 
st.markdown("""
<h3 style='color: #f39c12;'>🌈 Mood Tracker</h3>
<p style='color: #ecf0f1;'>Let me know how you're feeling today. I'll keep it private 💖</p>
""", unsafe_allow_html=True)

emoji_options = ["😄", "🙂", "😐", "😔", "😢"]
mood = st.select_slider("Your Mood Today", options=emoji_options, value="😐")
note = st.text_input("Any notes about your mood? (optional)")

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if st.button("📅 Log Mood"):
    st.session_state.mood_log.append({
        "date": str(datetime.date.today()),
        "mood": mood,
        "note": note
    })
    st.success("Mood logged! 💾")

# Show recent mood logs
if st.session_state.mood_log:
    with st.expander("📔 View Mood Journal"):
        for entry in reversed(st.session_state.mood_log[-5:]):
            st.markdown(f"**{entry['date']}** — {entry['mood']}  ")
            if entry['note']:
                st.markdown(f"_Note:_ {entry['note']}")

# Offer game if mood is low
if mood in ["😢", "😔"]:
    st.warning("Hey, looks like you're feeling down today. Wanna play a quick game to lift your mood? 🎮")
    if st.button("🕹️ Play Some refreshing games ;)"):
        st.markdown(
            "Trivia <br>"
            "Tic-Tac-Toe <br>  "
            "20 Questions <br>"
            "Riddles <br>"
            "Rock, Paper, Scissors <br>",
            unsafe_allow_html=True
        )

if not st.session_state.api_key:
    api_key = st.text_input("Enter API Key", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.experimental_rerun()
else:
    if "chat_messages" not in st.session_state:
        st.session_state.groq_chat_messages = [{
            "role": "system", 
            "content": (
                "You're Medi, the user's friendly AI health buddy. Speak casually and warmly, like a caring best friend who knows a lot about health. "
                "Be supportive, encouraging, and kind. Explain things clearly in a chill tone. If it's serious, gently recommend seeing a doctor. "
                "Add a few emojis where it feels natural. Always be comforting and understanding."
            )
        }]
        st.session_state.chat_messages = []

    if len(st.session_state.chat_messages) == 0:
        with st.chat_message("assistant"):
            st.markdown("Hey there! 😊 I'm **Medi**, your AI health buddy. Feeling off or got a health question? I’m all ears! 👂💬")

    for messages in st.session_state.chat_messages:
        if messages["role"] in ["user", "assistant"]:
            with st.chat_message(messages["role"]):
                st.markdown(f"<p style='color: #fbffff ;'>{messages['content']}</p>", unsafe_allow_html=True)

    def get_chat():
        embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[st.session_state.chat_messages[-1]["content"]],
            parameters={"input_type": "query"}
        )
        results = index.query(
            namespace="ns1",
            vector=embedding[0].values,
            top_k=3,
            include_values=False,
            include_metadata=True
        )
        context = ""
        for result in results.matches:
            if result['score'] > 0.8:
                context += result['metadata']['text']

        st.session_state.groq_chat_messages[-1]["content"] = f"User Query: {st.session_state.chat_messages[-1]['content']} \n Retrieved Content (optional): {context}"

        chat_completion = client.chat.completions.create(
            messages=st.session_state.groq_chat_messages,
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    if prompt := st.chat_input("Describe your symptoms or ask a health question"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            st.markdown("Ooh okay, let me check that out for you real quick! 🩺✨")

        with st.spinner("👀 Pretending to understand what’s going on..."):
            response = get_chat()
        with st.chat_message("assistant"):
            st.markdown(f"<p style='color: #fbffff ;'>{response}</p>", unsafe_allow_html=True)

        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.groq_chat_messages.append({"role": "assistant", "content": response})
