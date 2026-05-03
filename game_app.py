import streamlit as st
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Airport Quality World Cup",
    page_icon="✈️",
    layout="wide"
)

st_autorefresh(interval=2500, key="live_refresh")

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 15%, rgba(56,189,248,0.25), transparent 25%),
        radial-gradient(circle at 85% 10%, rgba(251,191,36,0.22), transparent 23%),
        radial-gradient(circle at 50% 95%, rgba(168,85,247,0.25), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #1e293b 100%);
    color: white;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1280px;
}

@keyframes flyPlane {
    0% { transform: translateX(-10%) translateY(0px) rotate(5deg); }
    50% { transform: translateX(45vw) translateY(-22px) rotate(8deg); }
    100% { transform: translateX(95vw) translateY(0px) rotate(5deg); }
}

@keyframes floatCard {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-9px); }
    100% { transform: translateY(0px); }
}

@keyframes glow {
    0% { box-shadow: 0 0 12px rgba(56,189,248,0.30); }
    50% { box-shadow: 0 0 35px rgba(56,189,248,0.80); }
    100% { box-shadow: 0 0 12px rgba(56,189,248,0.30); }
}

@keyframes pulseGold {
    0% { box-shadow: 0 0 10px rgba(251,191,36,0.30); }
    50% { box-shadow: 0 0 35px rgba(251,191,36,0.85); }
    100% { box-shadow: 0 0 10px rgba(251,191,36,0.30); }
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
}

.subtitle {
    color: #dbeafe;
    font-size: 18px;
}

.flying-plane {
    font-size: 52px;
    animation: flyPlane 7s infinite ease-in-out;
    margin-top: 16px;
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

.panel-gold {
    background: linear-gradient(135deg, rgba(251,191,36,0.22), rgba(56,189,248,0.12));
    border: 1px solid rgba(251,191,36,0.45);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.28);
    animation: pulseGold 3s infinite;
}

.globe {
    width: 245px;
    height: 245px;
    border-radius: 50%;
    margin: auto;
    background: radial-gradient(circle, #38bdf8 0%, #1d4ed8 42%, #020617 78%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 105px;
    border: 3px solid rgba(255,255,255,0.35);
    animation: glow 2.5s infinite;
}

.character-card {
    background: linear-gradient(135deg, rgba(56,189,248,0.22), rgba(168,85,247,0.20));
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    animation: floatCard 3.2s infinite ease-in-out;
}

.character-emoji {
    font-size: 64px;
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

.rank {
    padding: 12px;
    margin: 8px 0;
    border-radius: 14px;
    background: rgba(255,255,255,0.12);
    font-weight: 800;
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: #fbbf24;
    color: #111827;
    font-weight: 900;
    margin-right: 8px;
}

.announcement {
    background: rgba(15,23,42,0.85);
    border-left: 5px solid #38bdf8;
    padding: 14px 18px;
    border-radius: 14px;
    font-weight: 700;
    color: #e0f2fe;
}

.achievement {
    display: inline-block;
    padding: 9px 13px;
    border-radius: 999px;
    background: rgba(34,197,94,0.18);
    border: 1px solid rgba(34,197,94,0.45);
    margin: 5px;
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

# =========================================================
# DATA
# =========================================================
CHARACTERS = [
    {"name": "Luffy", "avatar": "🏴‍☠️", "role": "Risk Taker", "bonus": "Boss round +5"},
    {"name": "Zoro", "avatar": "⚔️", "role": "Root Cause Hunter", "bonus": "Analyze +5"},
    {"name": "Sanji", "avatar": "🔥", "role": "Improvement Chef", "bonus": "Improve +5"},
    {"name": "Nami", "avatar": "💰", "role": "Data Navigator", "bonus": "Measure +5"},
    {"name": "Goku", "avatar": "💥", "role": "Power Solver", "bonus": "Random +5"},
    {"name": "Vegeta", "avatar": "👑", "role": "Competitive Analyst", "bonus": "Final +5"},
    {"name": "Elsa", "avatar": "❄️", "role": "Control Specialist", "bonus": "Control +5"},
    {"name": "Ariel", "avatar": "🧜‍♀️", "role": "Flow Optimizer", "bonus": "Improve +5"},
    {"name": "Merida", "avatar": "🏹", "role": "Precision Planner", "bonus": "Define +5"},
    {"name": "Spider-Man", "avatar": "🕷️", "role": "Fast Responder", "bonus": "Warning save"},
    {"name": "Captain America", "avatar": "🛡️", "role": "Process Defender", "bonus": "Control +5"},
    {"name": "Captain Marvel", "avatar": "🌟", "role": "Crisis Leader", "bonus": "Boss +5"},
    {"name": "Batman", "avatar": "🦇", "role": "Root Cause Detective", "bonus": "Analyze +5"},
    {"name": "Wonder Woman", "avatar": "🛡️", "role": "Quality Champion", "bonus": "Final +5"},
    {"name": "Supergirl", "avatar": "☀️", "role": "Stability Guardian", "bonus": "Control +5"},
]

MISSIONS = [
    {
        "stage": "DEFINE", "city": "Dubai", "flag": "🇦🇪", "visual": "🏙️",
        "announcement": "DXB alert: Check-in queues are above target during evening departures.",
        "question": "What is the best problem statement?",
        "answer": "Average check-in waiting time is too high during peak hours",
        "options": [
            "Average check-in waiting time is too high during peak hours",
            "The airport needs better decoration",
            "Passengers dislike boarding passes",
            "The runway is too long"
        ],
        "explain": "Define focuses on the real quality problem, not unrelated issues."
    },
    {
        "stage": "MEASURE", "city": "Doha", "flag": "🇶🇦", "visual": "🕌",
        "announcement": "DOH data team requests the best KPI for the crisis.",
        "question": "Which KPI should be measured?",
        "answer": "Average passenger waiting time by hour",
        "options": [
            "Number of coffee shops",
            "Average passenger waiting time by hour",
            "Pilot names",
            "Terminal wall color"
        ],
        "explain": "Measure collects data directly connected to the problem."
    },
    {
        "stage": "ANALYZE", "city": "London", "flag": "🇬🇧", "visual": "🎡",
        "announcement": "LHR investigation: Waiting time spikes from 6 PM to 9 PM.",
        "question": "What is the most likely root cause?",
        "answer": "Not enough counters open during peak hours",
        "options": [
            "Too many signs",
            "Not enough counters open during peak hours",
            "The airport has too many windows",
            "Passengers are too early"
        ],
        "explain": "Analyze identifies the cause behind the measured problem."
    },
    {
        "stage": "IMPROVE", "city": "Paris", "flag": "🇫🇷", "visual": "🗼",
        "announcement": "CDG management wants an action that actually reduces delay.",
        "question": "Which improvement is strongest?",
        "answer": "Open more counters and guide eligible passengers to self-check-in",
        "options": [
            "Raise ticket prices",
            "Open more counters and guide eligible passengers to self-check-in",
            "Remove queue barriers",
            "Stop measuring the process"
        ],
        "explain": "Improve applies a solution that targets the root cause."
    },
    {
        "stage": "CONTROL", "city": "Tokyo", "flag": "🇯🇵", "visual": "🗻",
        "announcement": "HND improvement worked. Now the airport must prevent the issue from returning.",
        "question": "What is the best control plan?",
        "answer": "Monitor waiting time with control charts and trigger staff support if limits are exceeded",
        "options": [
            "Only check once per year",
            "Wait for complaints",
            "Monitor waiting time with control charts and trigger staff support if limits are exceeded",
            "Delete past data"
        ],
        "explain": "Control keeps the improved process stable over time."
    },
    {
        "stage": "BOSS", "city": "New York", "flag": "🇺🇸", "visual": "🗽",
        "announcement": "JFK boss round: Global delay emergency. Choose the full DMAIC strategy.",
        "question": "Which sequence solves the crisis correctly?",
        "answer": "Define, Measure, Analyze, Improve, Control",
        "options": [
            "Improve, Control, Guess, Stop",
            "Measure, Improve, Delete data",
            "Define, Measure, Analyze, Improve, Control",
            "Control first, then define later"
        ],
        "explain": "DMAIC must follow the structured improvement cycle."
    },
]

# =========================================================
# STATE
# =========================================================
def reset_all():
    st.session_state.players = {}
    st.session_state.game_started = False
    st.session_state.admin = False
    st.session_state.questions = []
    st.session_state.log = []

if "players" not in st.session_state:
    reset_all()

if "questions" not in st.session_state or not st.session_state.questions:
    shuffled = []
    for m in MISSIONS:
        item = m.copy()
        opts = item["options"].copy()
        random.shuffle(opts)
        item["options"] = opts
        shuffled.append(item)
    st.session_state.questions = shuffled

questions = st.session_state.questions

# =========================================================
# HELPERS
# =========================================================
def character_text(c):
    return f"{c['avatar']} {c['name']} — {c['role']}"

def get_character_by_text(text):
    for c in CHARACTERS:
        if character_text(c) == text:
            return c
    return CHARACTERS[0]

def calculate_bonus(character, stage):
    bonus = 0
    rule = character["bonus"].lower()
    if stage.lower() in rule:
        bonus += 5
    if stage == "BOSS" and ("boss" in rule or "final" in rule):
        bonus += 5
    if "random" in rule and random.random() < 0.35:
        bonus += 5
    return bonus

def achievements(score, wrong_count):
    badges = []
    if score >= 75:
        badges.append("🏆 DMAIC Master")
    if score >= 60:
        badges.append("✈️ Airport Hero")
    if wrong_count == 0:
        badges.append("🔥 Perfect Run")
    if score >= 45:
        badges.append("📊 Quality Analyst")
    return badges

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="title">✈️ Airport Quality World Cup</div>
    <div class="subtitle">
        A cinematic multiplayer-style DMAIC game with airport missions, character roles,
        live leaderboard, achievements, and boss round.
    </div>
    <div class="flying-plane">✈️ ・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・ 🌍</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Admin Panel")
admin_pass = st.sidebar.text_input("Admin password", type="password")
if admin_pass == "admin123":
    st.session_state.admin = True
    st.sidebar.success("Admin mode active")

if st.session_state.admin:
    if st.sidebar.button("Reset Game"):
        reset_all()
        st.rerun()

st.sidebar.caption("Admin password: admin123")

# =========================================================
# LOBBY
# =========================================================
if not st.session_state.game_started:
    left, right = st.columns([1.45, 1])

    with left:
        st.markdown("""
        <div class="panel-gold">
            <h2>🌍 Global Mission Lobby</h2>
            <p>
            Enter your name, choose your character, and wait for the admin to start the game.
            Each player becomes a quality engineer travelling through airport missions around the world.
            </p>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Player name")
        selected = st.selectbox("Choose character", [character_text(c) for c in CHARACTERS])
        selected_character = get_character_by_text(selected)

        st.markdown(f"""
        <div class="character-card">
            <div class="character-emoji">{selected_character['avatar']}</div>
            <h2>{selected_character['name']}</h2>
            <p><b>Role:</b> {selected_character['role']}</p>
            <p><b>Bonus:</b> {selected_character['bonus']}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Join Lobby"):
                if name.strip():
                    st.session_state.players[name] = {
                        "character": selected_character,
                        "score": 0,
                        "ready": False,
                        "level": 0,
                        "wrong": 0,
                        "finished": False
                    }
                    st.success("Joined lobby!")
        with c2:
            if name in st.session_state.players:
                if st.button("Ready for Takeoff"):
                    st.session_state.players[name]["ready"] = True
                    st.success("Ready!")

    with right:
        st.markdown("<div class='globe'>🌍</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="panel">
            <h3>🎮 Features</h3>
            <p>🌍 Global airport roadmap</p>
            <p>✈️ Animated flight atmosphere</p>
            <p>🧑 Character roles and bonuses</p>
            <p>🏆 Live leaderboard</p>
            <p>🔥 Boss round</p>
            <p>🎖️ Achievements</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 👥 Lobby Players")

    if not st.session_state.players:
        st.info("No players yet.")
    else:
        cols = st.columns(3)
        for i, (player, data) in enumerate(st.session_state.players.items()):
            ch = data["character"]
            status = "✅ Ready" if data["ready"] else "⏳ Waiting"
            with cols[i % 3]:
                st.markdown(f"""
                <div class="character-card">
                    <div class="character-emoji">{ch['avatar']}</div>
                    <h3>{player}</h3>
                    <p>{ch['name']} — {ch['role']}</p>
                    <b>{status}</b>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.admin:
        if st.button("🚀 START WORLD CUP"):
            st.session_state.game_started = True
            st.session_state.log.append(f"Game started at {datetime.now().strftime('%H:%M:%S')}")
            st.rerun()

# =========================================================
# GAME
# =========================================================
else:
    st.markdown("## 🛫 Mission Control")

    max_level = max([p["level"] for p in st.session_state.players.values()], default=0)

    roadmap = "<div class='roadmap'>"
    for i, q in enumerate(questions):
        if i < max_level:
            cls = "stop stop-done"
        elif i == max_level:
            cls = "stop stop-active"
        else:
            cls = "stop"
        roadmap += f"<div class='{cls}'>{q['flag']}<br>{q['city']}<br>{q['stage']}</div>"
    roadmap += "</div>"
    st.markdown(roadmap, unsafe_allow_html=True)

    main_col, board_col = st.columns([1.65, 1])

    with main_col:
        if not st.session_state.players:
            st.warning("No players joined.")
        else:
            tabs = st.tabs(list(st.session_state.players.keys()))

            for tab, player in zip(tabs, st.session_state.players.keys()):
                with tab:
                    data = st.session_state.players[player]
                    ch = data["character"]

                    if data["level"] >= len(questions):
                        data["finished"] = True
                        st.success("Mission completed!")
                        continue

                    q = questions[data["level"]]

                    st.markdown(f"""
                    <div class="announcement">
                    📢 Airport Announcement: {q['announcement']}
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("")

                    a, b = st.columns([1, 2])

                    with a:
                        st.markdown(f"""
                        <div class="character-card">
                            <div class="character-emoji">{ch['avatar']}</div>
                            <h2>{player}</h2>
                            <p>{ch['name']}</p>
                            <p>{ch['role']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with b:
                        st.markdown(f"""
                        <div class="panel">
                            <span class="badge">{q['stage']}</span>
                            <h2>{q['flag']} {q['city']} Airport</h2>
                            <h3>{q['question']}</h3>
                        </div>
                        """, unsafe_allow_html=True)

                    answer = st.radio(
                        "Choose your decision:",
                        q["options"],
                        key=f"{player}_{data['level']}"
                    )

                    if st.button(f"Submit Decision for {player}", key=f"submit_{player}_{data['level']}"):
                        if answer == q["answer"]:
                            base = 15
                            bonus = calculate_bonus(ch, q["stage"])
                            total = base + bonus
                            st.session_state.players[player]["score"] += total
                            st.success(f"Correct! +{base} points +{bonus} bonus. {q['explain']}")
                        else:
                            st.session_state.players[player]["wrong"] += 1
                            st.error(f"Wrong. Correct answer: {q['answer']}. {q['explain']}")

                        st.session_state.players[player]["level"] += 1
                        st.rerun()

    with board_col:
        st.markdown("<div class='panel-gold'>", unsafe_allow_html=True)
        st.markdown("## 🏆 Live Leaderboard")

        sorted_players = sorted(
            st.session_state.players.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        for i, (player, data) in enumerate(sorted_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "✈️"
            st.markdown(
                f"<div class='rank'>{medal} {data['character']['avatar']} {player} — {data['score']} pts</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("## 🎖️ Achievements")
        for player, data in sorted_players:
            badge_list = achievements(data["score"], data["wrong"])
            if badge_list:
                st.write(f"**{player}**")
                st.markdown(" ".join([f"<span class='achievement'>{b}</span>" for b in badge_list]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        all_finished = all([p["level"] >= len(questions) for p in st.session_state.players.values()])

        if all_finished and st.session_state.players:
            st.balloons()
            st.success("World Cup completed!")
            winner = sorted_players[0][0]
            st.subheader(f"🏆 Winner: {winner}")

            if st.session_state.admin:
                if st.button("Return to Lobby"):
                    reset_all()
                    st.rerun()
