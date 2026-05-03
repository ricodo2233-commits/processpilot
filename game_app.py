import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Airport Game", layout="wide")

# auto refresh every 3 sec
st_autorefresh(interval=3000, key="refresh")

# -----------------------------
# GLOBAL STORAGE (simple)
# -----------------------------
if "players" not in st.session_state:
    st.session_state.players = {}

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# -----------------------------
# CHARACTERS
# -----------------------------
characters = [
    "🧑‍✈️ Luffy", "⚔️ Zoro", "🔥 Sanji", "💰 Nami",
    "💥 Goku", "👑 Vegeta",
    "❄️ Elsa", "🧜‍♀️ Ariel", "🏹 Merida",
    "🕷️ Spider-Man", "🛡️ Captain America", "⚡ Thor",
    "🦇 Batman", "🦸‍♂️ Superman", "🦸‍♀️ Wonder Woman"
]

# -----------------------------
# QUESTIONS (RANDOMIZED)
# -----------------------------
questions = [
    {
        "q": "What is the main problem?",
        "a": "Waiting time too high",
        "options": [
            "Airport decoration",
            "Waiting time too high",
            "Pilot uniforms",
            "Weather"
        ]
    },
    {
        "q": "What should be measured?",
        "a": "Waiting time",
        "options": [
            "Waiting time",
            "Food quality",
            "Pilot names",
            "Airport size"
        ]
    },
    {
        "q": "Root cause?",
        "a": "Not enough counters",
        "options": [
            "Too many counters",
            "Weather",
            "Not enough counters",
            "Plane size"
        ]
    },
    {
        "q": "Best improvement?",
        "a": "Open more counters",
        "options": [
            "Close airport",
            "Open more counters",
            "Ignore",
            "Raise prices"
        ]
    },
    {
        "q": "Control method?",
        "a": "Control charts",
        "options": [
            "Control charts",
            "Do nothing",
            "Wait",
            "Guess"
        ]
    }
]

# shuffle options
for q in questions:
    random.shuffle(q["options"])

# -----------------------------
# TITLE
# -----------------------------
st.title("✈️ Airport Quality Game")

# -----------------------------
# ADMIN LOGIN
# -----------------------------
admin_pass = st.sidebar.text_input("Admin password", type="password")

if admin_pass == "admin123":
    st.session_state.admin = True

# -----------------------------
# PLAYER JOIN
# -----------------------------
if not st.session_state.game_started:

    st.subheader("Join Lobby")

    name = st.text_input("Enter your name")

    character = st.selectbox("Choose character", characters)

    if st.button("Join"):
        if name != "":
            st.session_state.players[name] = {
                "character": character,
                "score": 0,
                "ready": False,
                "level": 0
            }

    # READY BUTTON
    for player in st.session_state.players:
        if st.button(f"{player} Ready"):
            st.session_state.players[player]["ready"] = True

    # SHOW LOBBY
    st.subheader("Lobby Players")

    for p, data in st.session_state.players.items():
        st.write(f"{data['character']} {p} - {'Ready' if data['ready'] else 'Waiting'}")

    # ADMIN START
    if st.session_state.admin:
        if st.button("START GAME"):
            st.session_state.game_started = True

# -----------------------------
# GAME START
# -----------------------------
else:

    st.subheader("Game Running")

    for player, data in st.session_state.players.items():

        st.markdown(f"### {data['character']} {player}")

        if data["level"] < len(questions):

            q = questions[data["level"]]

            answer = st.radio(
                q["q"],
                q["options"],
                key=f"{player}_{data['level']}"
            )

            if st.button(f"Submit {player}", key=f"btn_{player}_{data['level']}"):
                if answer == q["a"]:
                    st.session_state.players[player]["score"] += 10

                st.session_state.players[player]["level"] += 1

        else:
            st.success("Finished")

    # -----------------------------
    # LEADERBOARD
    # -----------------------------
    st.subheader("🏆 Leaderboard")

    sorted_players = sorted(
        st.session_state.players.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    for i, (p, data) in enumerate(sorted_players, 1):
        st.write(f"{i}. {data['character']} {p} — {data['score']} pts")

    # RESET (ADMIN ONLY)
    if st.session_state.admin:
        if st.button("RESET GAME"):
            st.session_state.players = {}
            st.session_state.game_started = False
