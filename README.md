# <Tag Team>

# MediChat – Your Personal AI Health Companion

Welcome to **MediChat**, a simple and friendly web application where you can chat with an AI about your health, track your mood, and engage in light, relaxing activities. Whether you're feeling great or just need someone to talk to, Medi is here to support you with helpful wellness advice and a listening ear.

## Features

### AI Chat Companion
- Talk to **Medi**, your AI-powered health assistant trained to provide thoughtful, friendly, and supportive responses.
- Ask questions related to general health, symptoms, lifestyle, or wellness.
- While Medi offers helpful insights, it will recommend consulting a real doctor if a topic seems serious or beyond its scope.

### Mood Tracker and Journal
- Keep track of how you're feeling with daily mood entries.
- Add personal notes to reflect on your thoughts or experiences.
- Your data is saved temporarily in your session and remains private during your visit.

### Fun and Relaxing Activities
Take a break from stress with tools designed to improve your well-being:
- **Daily Challenges**: Simple wellness goals like drinking enough water or taking a short walk.
- **Motivational Quotes**: Get inspired with uplifting thoughts.
- **Compliment Generator**: A quick way to boost your mood.
- **Hydration Tracker**: Monitor your daily water intake.
- **Breathing Exercises**: Relax and refocus with guided breathing techniques.

## How It Works

- Built using **Streamlit** for a responsive and interactive user interface.
- Uses **Groq API** to generate natural, human-like responses.
- Chat and mood logs are stored using **Streamlit’s session_state** to keep everything organized within your session.
- Integrates with **Pinecone** for semantic search from health-related content.
- Presents a random health fact during each session for a bit of extra learning.

## Getting Started

1. Install Dependencies
Make sure Python is installed, then run:

pip install streamlit groq pinecone requests


2. Run the Application

python -m streamlit run your_script_name.py


3. Open in Browser 
Your app will launch in the browser and you're ready to begin.


## Important Note

MediChat is a helpful tool for general wellness and support, but it is **not a replacement for professional medical advice**. If you are experiencing health issues or symptoms that require attention, don't hesitate to get in touch with a licensed healthcare provider.


## About MediChat

MediChat was created to provide a calm, supportive space where users can check in with themselves, receive helpful guidance, and feel heard. It blends technology and empathy to promote everyday mental and physical wellness.


