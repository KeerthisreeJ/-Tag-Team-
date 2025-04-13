import streamlit as st
from groq import Groq
from pinecone import Pinecone
import requests
import datetime
import random

# Initialize Groq and Pinecone clients
client = Groq(api_key="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")
pc = Pinecone(api_key="b311901d-a6a4-4b0a-a292-9431183d5623")
index = pc.Index("quickstart")

# Session Setup
if "api_key" not in st.session_state:
    st.session_state.api_key = "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"
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "groq_chat_messages" not in st.session_state:
    st.session_state.groq_chat_messages = [{
        "role": "system",
        "content": (
            "You're Medi, the user's friendly AI health buddy. Speak casually and warmly, like a caring best friend who knows a lot about health. Try to Understand the speakers tone, if they are sad , u can recommned them to play games "
            "Be supportive, encouraging, and kind. Explain things clearly in a chill tone. If it's serious, gently recommend seeing a doctor. "
            "Add a few emojis where it feels natural. Always be comforting and understanding."
        )
    }]

# Sidebar Tabs
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🩺 MediChat")
tab = st.sidebar.radio("Choose a Section", ["🩺 AI Companion", "📓 Mood Tracker + Journal", "🎮 Fun & Games"])


# Health Fact of the Day
health_facts = [
    "Drinking water first thing in the morning boosts metabolism. 💧",
    "Laughing is good for your heart and increases blood flow by 20%. 😂❤️",
    "A 20-minute walk can improve mood and reduce stress. 🚶‍♂️✨",
    "Sleep is essential for healing and immune function. 😴🛌",
    "Deep breathing reduces anxiety. Try 4-7-8 breathing! 🧘"
]

if tab == "🩺 AI Companion":
    st.title("🩺 Medi - Your AI Health Buddy")
    st.info(random.choice(health_facts))

    if len(st.session_state.chat_messages) == 0:
        with st.chat_message("assistant"):
            st.markdown("Hey there! 😊 I'm **Medi**, your AI health buddy. Feeling off or got a health question? I’m all ears! 👂💬")

    for messages in st.session_state.chat_messages:
        if messages["role"] in ["user", "assistant"]:
            with st.chat_message(messages["role"]):
                st.markdown(f"{messages['content']}")

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

        st.session_state.groq_chat_messages[-1]["content"] = f"User Query: {st.session_state.chat_messages[-1]['content']}\n Retrieved Content (optional): {context}"

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
            st.markdown(response)

        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.groq_chat_messages.append({"role": "assistant", "content": response})

elif tab == "📓 Mood Tracker + Journal":
    st.title("📓 Mood Tracker + Journal")
    st.info(random.choice(health_facts))

    emoji_options = ["😄", "🙂", "😐", "😔", "😢"]
    note = st.text_input("Any notes about your mood? (optional)")
    mood = ""
    if note:
        # Mood prediction based on simple sentiment detection
        if any(word in note.lower() for word in ["sad", "down", "tired", "bad"]):
            mood = "😢"
        elif any(word in note.lower() for word in ["happy", "great", "joy", "good"]):
            mood = "😄"
        else:
            mood = st.select_slider("Your Mood Today", options=emoji_options, value="😐")
    else:
        mood = st.select_slider("Your Mood Today", options=emoji_options, value="😐")

    if st.button("📅 Log Mood"):
        st.session_state.mood_log.append({
            "date": str(datetime.date.today()),
            "mood": mood,
            "note": note
        })
        st.success("Mood logged! 💾")

    if st.session_state.mood_log:
        with st.expander("📔 View Mood Journal"):
            for entry in reversed(st.session_state.mood_log[-5:]):
                st.markdown(f"**{entry['date']}** — {entry['mood']}")
                if entry['note']:
                    st.markdown(f"_Note:_ {entry['note']}")

elif tab == "🎮 Fun & Games":
    st.title("🎮 Refresh & Play")

    # Daily Challenge
    st.subheader("🎯 Daily Challenge Spinner")
    if st.button("Spin Challenge Wheel"):
        challenge = random.choice([
            "Drink 2L of water 💧",
            "Take a 10-minute walk 🚶",
            "Stretch for 5 minutes 🧘",
            "No junk food today 🍎",
            "Write down 3 things you’re grateful for 🙏"
        ])
        st.success(f"Your Challenge: {challenge}")

    # Motivation
    st.subheader("🌟 Motivational Quote")
    quote = random.choice([
        "You're stronger than you think. 💪",
        "Every day is a second chance. 🌱",
        "Breathe. You got this. 🌬️",
        "Your vibe attracts your tribe. ✨",
        "Progress, not perfection. 🔄"
    ])
    st.markdown(f"**{quote}**")

    # Compliment Bot
    st.subheader("💬 Compliment Generator")
    if st.button("Get a Compliment 💖"):
        compliment = random.choice([
            "You're a sunshine in human form! ☀️",
            "You radiate positivity! 🌈",
            "You're doing amazing, sweetie! 💫",
            "You're as strong as espresso! ☕",
            "Your smile can light up rooms. 😁"
        ])
        st.balloons()
        st.success(compliment)

     # Hydration Reminder Game
    st.subheader("💧 Hydration Buddy")
    st.markdown("Click the button every time you drink a glass of water today!")
    if "water_count" not in st.session_state:
        st.session_state.water_count = 0

    if st.button("🥤 I drank water!"):
        st.session_state.water_count += 1
        st.success(f"You've had {st.session_state.water_count} glass(es) today! Keep going! 🚰")

    # Breathing Exercise
    st.subheader("🧘 Calm Breathing Exercise")
    st.markdown("Follow this simple breathing guide to relax:")
    with st.expander("Show Breathing Steps"):
        st.markdown("""
        - Inhale deeply for 4 seconds 🫁  
        - Hold for 7 seconds ✋  
        - Exhale slowly for 8 seconds 🌬️  
        - Repeat 4 times to feel calm.
        """)
        st.info("Try doing this exercise before bed or during stressful times. 💖")

    
