import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Airport Quality Quest", page_icon="✈️", layout="wide")
st_autorefresh(interval=3000, key="refresh")

# -----------------------------
# CSS / VISUAL DESIGN
# -----------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 20%, rgba(56,189,248,0.25), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(251,191,36,0.20), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(168,85,247,0.22), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #1e293b 100%);
    color: white;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1250px;
}

@keyframes fly {
    0% { transform: translateX(-10%) translateY(0px) rotate(5deg); }
    50% { transform: translateX(45vw) translateY(-25px) rotate(8deg); }
    100% { transform: translateX(95vw) translateY(0px) rotate(5deg); }
}

@keyframes glow {
    0% { box-shadow: 0 0 12px rgba(56,189,248,0.35); }
    50% { box-shadow: 0 0 35px rgba(56,189,248,0.85); }
    100% { box-shadow: 0 0 12px rgba(56,189,248,0.35); }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

.hero {
    background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.05));
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 30px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    overflow: hidden;
}

.title {
    font-size: 48px;
    font-weight: 950;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #dbeafe;
}

.flying-plane {
    font-size: 50px;
    animation: fly 8s infinite ease-in-out;
    margin-top: 18px;
}

.panel {
    background: rgba(255,255,255,0.11);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.28);
}

.globe {
    width: 230px;
    height: 230px;
    border-radius: 50%;
    margin: auto;
    background: radial-gradient(circle, #38bdf8 0%, #1d4ed8 42%, #020617 78%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 100px;
    border: 3px solid rgba(255,255,255,0.35);
    animation: glow 2.5s infinite;
}

.character-card {
    background: linear-gradient(135deg, rgba(56,189,248,0.22), rgba(168,85,247,0.20));
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    animation: float 3.2s infinite ease-in-out;
}

.character-emoji {
    font-size: 60px;
}

.score-card {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    animation: glow 3s infinite;
}

.score-num {
    font-size: 30px;
    font-weight: 950;
}

.roadmap {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin: 18px 0;
}

.stop {
    flex: 1;
    text-align: center;
    padding: 10px;
    border-radius: 16px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    font-size: 13px;
}

.stop-active {
    background: #38bdf8;
    color: #020617;
    font-weight: 900;
    animation: glow 2s infinite;
}

.stop-done {
    background: #22c55e;
    color: #052e16;
    font-weight: 900;
}

.leaderboard {
    background: linear-gradient(135deg, rgba(251,191,36,0.20), rgba(56,189,248,0.14));
    border: 1px solid rgba(251,191,36,0.4);
    border-radius: 22px;
    padding: 18px;
}

.rank {
    padding: 12px;
    margin: 8px 0;
    border-radius: 14px;
    background: rgba(255,255,255,0.12);
    font-weight: 800;
}

div.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #fbbf24);
    color: #020617;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1.25rem;
    font-weight: 900;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #7dd3fc, #fde68a);
    color: #020617;
}

.stRadio label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# STATE
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
    "🏴‍☠️ Luffy", "⚔️ Zoro", "🔥 Sanji", "💰 Nami",
    "💥 Goku", "👑 Vegeta",
    "❄️ Elsa", "🧜‍♀️ Ariel", "🏹 Merida",
    "🕷️ Spider-Man", "🛡️ Captain America", "⚡ Thor",
    "🦇 Batman", "☀️ Superman", "🛡️ Wonder Woman"
]

# -----------------------------
# QUESTIONS
# -----------------------------
base_questions = [
    {
        "stage": "DEFINE",
        "city": "Dubai",
        "flag": "🇦🇪",
        "q": "Passengers are complaining about long check-in queues. What is the main quality problem?",
        "a": "Waiting time is too high",
        "options": ["Waiting time is too high", "Airport decoration", "Ticket color", "Pilot uniforms"]
    },
    {
        "stage": "MEASURE",
        "city": "Doha",
        "flag": "🇶🇦",
        "q": "What should the airport measure first?",
        "a": "Average passenger waiting time",
        "options": ["Restaurant sales", "Average passenger waiting time", "Plane color", "Number of shops"]
    },
    {
        "stage": "ANALYZE",
        "city": "London",
        "flag": "🇬🇧",
        "q": "Data shows delays happen from 6 PM to 9 PM. What is the likely cause?",
        "a": "Not enough counters during peak hours",
        "options": ["Weather only", "Not enough counters during peak hours", "Too many signs", "Long runway"]
    },
    {
        "stage": "IMPROVE",
        "city": "Paris",
        "flag": "🇫🇷",
        "q": "What is the best improvement action?",
        "a": "Open more counters and guide passengers to self-check-in",
        "options": ["Close the airport", "Ignore complaints", "Open more counters and guide passengers to self-check-in", "Remove staff"]
    },
    {
        "stage": "CONTROL",
        "city": "Tokyo",
        "flag": "🇯🇵",
        "q": "How should the airport keep the improvement stable?",
        "a": "Monitor waiting time using control charts",
        "options": ["Stop collecting data", "Monitor waiting time using control charts", "Guess daily", "Wait for complaints"]
    },
    {
        "stage": "FINAL",
        "city": "New York",
        "flag": "🇺🇸",
        "q": "What is the correct DMAIC order?",
        "a": "Define, Measure, Analyze, Improve, Control",
        "options": ["Improve, Define, Control", "Measure, Improve, Guess", "Define, Measure, Analyze, Improve, Control", "Control, Analyze, Stop"]
    }
]

# Shuffle options once per session
if "questions" not in st.session_state:
    st.session_state.questions = []
    for q in base_questions:
        copy_q = q.copy()
        copy_q["options"] = q["options"].copy()
        random.shuffle(copy_q["options"])
        st.session_state.questions.append(copy_q)

questions = st.session_state.questions

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="title">✈️ Airport Quality Quest</div>
    <div class="subtitle">A multiplayer-style DMAIC airport mission with characters, leaderboard, and global quality challenges.</div>
    <div class="flying-plane">✈️ ・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・ 🌍</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR ADMIN
# -----------------------------
st.sidebar.title("Admin Panel")
admin_pass = st.sidebar.text_input("Admin password", type="password")

if admin_pass == "admin123":
    st.session_state.admin = True
    st.sidebar.success("Admin mode active")

if st.session_state.admin:
    if st.sidebar.button("Reset Full Game"):
        st.session_state.players = {}
        st.session_state.game_started = False
        st.session_state.questions = []
        st.rerun()

# -----------------------------
# LOBBY
# -----------------------------
if not st.session_state.game_started:
    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("""
        <div class="panel">
            <h2>🌍 Mission Lobby</h2>
            <p>Enter your name, choose your character, and get ready for takeoff.</p>
            <p>You are joining a global airport quality mission where each level follows DMAIC.</p>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Player name")
        character = st.selectbox("Choose your character", characters)

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Join Lobby"):
                if name.strip():
                    st.session_state.players[name] = {
                        "character": character,
                        "score": 0,
                        "ready": False,
                        "level": 0
                    }
                    st.success("Joined lobby!")

        with c2:
            if name in st.session_state.players:
                if st.button("Ready for Takeoff"):
                    st.session_state.players[name]["ready"] = True
                    st.success("You are ready!")

    with right:
        st.markdown("<div class='globe'>🌍</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="panel">
            <h3>Rules</h3>
            <p>✅ Correct answer: +15 points</p>
            <p>❌ Wrong answer: 0 points</p>
            <p>🏆 Live leaderboard updates during the game</p>
            <p>🔐 Admin starts the mission</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 👥 Players in Lobby")

    if len(st.session_state.players) == 0:
        st.info("No players yet.")
    else:
        cols = st.columns(3)
        for i, (p, data) in enumerate(st.session_state.players.items()):
            with cols[i % 3]:
                status = "✅ Ready" if data["ready"] else "⏳ Waiting"
                st.markdown(f"""
                <div class="character-card">
                    <div class="character-emoji">{data["character"].split()[0]}</div>
                    <h3>{p}</h3>
                    <p>{data["character"]}</p>
                    <b>{status}</b>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.admin:
        st.write("")
        if st.button("🚀 START GAME"):
            st.session_state.game_started = True
            st.rerun()

# -----------------------------
# GAME
# -----------------------------
else:
    st.markdown("## 🛫 Mission in Progress")

    # Roadmap
    max_level = max([p["level"] for p in st.session_state.players.values()], default=0)
    roadmap_html = "<div class='roadmap'>"
    for i, q in enumerate(questions):
        if i < max_level:
            cls = "stop stop-done"
        elif i == max_level:
            cls = "stop stop-active"
        else:
            cls = "stop"
        roadmap_html += f"<div class='{cls}'>{q['flag']}<br>{q['city']}<br>{q['stage']}</div>"
    roadmap_html += "</div>"
    st.markdown(roadmap_html, unsafe_allow_html=True)

    game_col, board_col = st.columns([1.7, 1])

    with game_col:
        for player, data in st.session_state.players.items():
            st.markdown(f"""
            <div class="panel">
                <h2>{data["character"]} {player}</h2>
            </div>
            """, unsafe_allow_html=True)

            if data["level"] < len(questions):
                q = questions[data["level"]]

                st.markdown(f"""
                <div class="panel">
                    <span class="badge">{q["stage"]}</span>
                    <h3>{q["flag"]} {q["city"]} Airport Mission</h3>
                    <p>{q["q"]}</p>
                </div>
                """, unsafe_allow_html=True)

                answer = st.radio(
                    f"Decision for {player}",
                    q["options"],
                    key=f"{player}_{data['level']}"
                )

                if st.button(f"Submit Decision - {player}", key=f"submit_{player}_{data['level']}"):
                    if answer == q["a"]:
                        st.session_state.players[player]["score"] += 15
                        st.success("Correct decision! +15 points")
                    else:
                        st.error(f"Wrong decision. Correct answer: {q['a']}")

                    st.session_state.players[player]["level"] += 1
                    st.rerun()
            else:
                st.success("Mission completed!")

    with board_col:
        st.markdown("<div class='leaderboard'>", unsafe_allow_html=True)
        st.markdown("## 🏆 Live Leaderboard")

        sorted_players = sorted(
            st.session_state.players.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        for i, (p, data) in enumerate(sorted_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "✈️"
            st.markdown(
                f"<div class='rank'>{medal} {data['character']} {p} — {data['score']} pts</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)
