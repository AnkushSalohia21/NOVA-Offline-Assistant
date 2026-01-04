# =========================================
# NOVA ULTIMATE – ADVANCED OFFLINE CHATBOT
# =========================================

import json
import os
import random
import subprocess
import speech_recognition as sr
from datetime import datetime
from collections import deque

BOT_NAME = "NOVA"
MEMORY_FILE = "nova_memory.json"
CONTEXT_LIMIT = 10  

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'w') as f:
        json.dump({"last_user_input": [], "last_bot_reply": [], "user_name": ""}, f)

memory = json.load(open(MEMORY_FILE, 'r'))
user_name = memory.get("user_name", "")
context_user = deque(memory.get("last_user_input", []), maxlen=CONTEXT_LIMIT)
context_bot = deque(memory.get("last_bot_reply", []), maxlen=CONTEXT_LIMIT)
current_mood = "chill" 

# ================== VOICE OUTPUT ==================
def speak(text):
    text = text.replace('"', '`"')
    ps_script = f'''
    Add-Type –AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.SelectVoice("Microsoft Zira Desktop");
    $speak.Speak("{text}");
    '''
    subprocess.run(["powershell", "-Command", ps_script], capture_output=True)

# ================== INPUT HANDLER ==================
def take_voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-IN")
            print(f"You said: {query}")
            return query
        except:
            return input("Couldn't hear you properly. Type your message: ")

def take_input(mode):
    if mode == "voice":
        return take_voice_command()
    else:
        return input("Type your message: ")

# ================== INITIAL SETUP ==================
def choose_mode():
    while True:
        choice = input("Choose input mode - Chat or Voice? (c/v): ").strip().lower()
        if choice == 'v':
            print("Voice mode activated.")
            speak("Voice mode activated. Speak your queries.")
            return "voice"
        elif choice == 'c':
            print("Chat mode activated.")
            return "chat"
        else:
            print("Invalid choice. Type 'c' or 'v'.")

def get_user_name():
    global user_name, memory
    if user_name.strip() == "":
        name = input("Hey! What's your name? ").strip()
        if name:
            user_name = name
            memory["user_name"] = user_name
            save_memory()
    return user_name

# ================== INTENTS & RESPONSES ==================
INTENTS = {
    "greeting": ["hello", "hi", "hey", "wassup", "yo", "morning", "afternoon", "evening"],
    "time": ["time", "current time", "tell time"],
    "date": ["date", "today date", "current date"],
    "howareyou": ["how are you", "kya haal hai"],
    "thanks": ["thanks", "thank you", "thx"],
    "joke": ["joke", "tell joke", "funny", "make me laugh"],
    "bye": ["bye", "goodbye", "see you", "exit"],
    "mood": ["bored", "sad", "happy", "tired", "frustrated", "lonely"],
    "namebot": ["your name", "who are you", "what is your name"],
    "zira": ["zira", "microsoft", "voice"],
    "fun": ["game", "music", "movie", "plan", "hangout"]
}

JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything! 😅",
    "I told my computer I needed a break, it said 'No problem, I'll sleep!'",
    "Why did the scarecrow get a promotion? Because he was outstanding in his field! 🌾",
    "Why did the math book look sad? Because it had too many problems 😢",
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "Why did the coffee file a police report? It got mugged ☕",
    "Why did the tomato turn red? Because it saw the salad dressing! 🍅",
    "Why don’t skeletons fight each other? They don’t have the guts 💀",
    "What do you call fake spaghetti? An impasta! 🍝",
    "Why did the bicycle fall over? Because it was two-tired! 🚲",
    "Why did the computer go to the doctor? It caught a virus! 💻",
    "Why did the cookie go to the hospital? Because it felt crummy 🍪",
    "What did one wall say to the other wall? I'll meet you at the corner!",
    "Why can't your nose be 12 inches long? Because then it would be a foot! 👃",
    "Why did the gym close down? It just didn’t work out! 💪",
    "Why don’t eggs tell jokes? They’d crack each other up 🥚",
    "Why did the picture go to jail? Because it was framed! 🖼️",
    "Why did the belt go to jail? For holding up the pants! 👖",
    "Why did the stadium get hot after the game? Because all the fans left! 🏟️",
    "Why did the phone go to school? It wanted to be smarter! 📱"
]

# ================== MOOD-BASED RESPONSES ==================
MOODS = {
    "chill": ["Haha chill 😎", "All good, just vibing 😏", "Let's take it easy 😌"],
    "funny": ["Lol 😂", "Hahaha, that's funny 😅", "ROFL 🤣"],
    "serious": ["Hmm 🤔", "I see...", "Let's focus then."],
    "sarcastic": ["Oh really? 😏", "Wow, genius 🤨", "Sure, totally… 🙄"]
}

RESPONSES = {
    "greeting": [
        lambda: f"Hey {user_name}! What's up? 😎",
        lambda: f"Yo {user_name}! How's your day going?",
        lambda: f"Sup buddy {user_name}? Ready to chill?",
        lambda: f"Hey {user_name}, nice to see you!"
    ],
    "time": [
        lambda: f"It's {datetime.now().strftime('%H:%M')} right now ⏰",
        lambda: f"The clock says {datetime.now().strftime('%I:%M %p')}"
    ],
    "date": [
        lambda: f"Today is {datetime.now().strftime('%A, %d %B %Y')}",
        lambda: f"Date today is {datetime.now().strftime('%d-%m-%Y')}"
    ],
    "howareyou": [
        "I'm feeling awesome 😎, how about you?",
        "All good here, chill mode ON 😏",
        "Feeling fun today, wanna vibe?"
    ],
    "thanks": ["No worries 😎", "Anytime buddy!", "Glad to help!"],
    "joke": [lambda: random.choice(JOKES)],
    "bye": ["Catch you later ✌️", "See ya! 😎", "Later gator! 🐊"],
    "mood": ["Cheer up! 😊", "Let's do something fun 😏", "Keep grinding 💪"],
    "namebot": [f"My name is {BOT_NAME}, your personal assistant 🤖"],
    "zira": ["Zira is Microsoft’s TTS voice, sounds nice!"],
    "fun": ["Wanna play a game? 🎮", "Let's listen to some music 🎵", "Movie time? 🍿"]
}

# ================== UTILITY FUNCTIONS ==================
def detect_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in user_input:
                return intent
    return "unknown"

def shift_personality():
    global current_mood
    current_mood = random.choice(list(MOODS.keys()))

def generate_reply(intent):
    # Randomly shift personality every 3-5 queries
    if random.random() < 0.3:
        shift_personality()
    if intent in RESPONSES:
        response = random.choice(RESPONSES[intent])
        reply = response() if callable(response) else response
    else:
        fallback = [
            "Hmm, interesting 🤔",
            "I get you, tell me more!",
            "That's cool 😎",
            "Haha, I see! 😂",
            "Can you explain a bit more?",
            "Wow, didn't know that! 😮",
            "Sounds fun! 😏"
        ]
        reply = random.choice(fallback)
    # Apply mood style
    reply += " " + random.choice(MOODS[current_mood])
    return reply

def save_memory():
    memory["last_user_input"] = list(context_user)
    memory["last_bot_reply"] = list(context_bot)
    memory["user_name"] = user_name
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

# ================== MAIN CHAT LOOP ==================
def main():
    global context_user, context_bot
    print(f"========== {BOT_NAME.upper()} CHATBOT ==========")
    speak(f"Hey there! I am {BOT_NAME}, ready to chat with you.")
    mode = choose_mode()
    get_user_name()
    speak(f"Nice to meet you, {user_name}!")

    while True:
        user_input = take_input(mode)
        if not user_input:
            continue

        context_user.append(user_input)
        intent = detect_intent(user_input)
        reply = generate_reply(intent)
        context_bot.append(reply)

        print(f"{BOT_NAME}: {reply}")
        if mode == "voice":
            speak(reply)

        save_memory()

        if intent == "bye":
            break

if __name__ == "__main__":
    main()
