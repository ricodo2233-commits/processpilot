import streamlit as st
import random

st.set_page_config(
    page_title="Airport Quality Quest",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------
# Styling + animations
# ---------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 20% 20%, rgba(56,189,248,0.25), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(251,191,36,0.20), transparent 25%),
        linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e293b 100%);
    color: white;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1250px;
}

@keyframes floatPlane {
    0% { transform: translateX(-5%) translateY(0px) rotate(3deg); }
    50% { transform: translateX(45%) translateY(-18px) rotate(7deg); }
    100% { transform: translateX(95%) translateY(0px) rotate(3deg); }
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(56,189,248,0.6); }
    70% { box-shadow: 0 0 0 18px rgba(56,189,248,0); }
    100% { box-shadow: 0 0 0 0 rgba(56,189,248,0); }
}

@keyframes glow {
    0% { opacity: 0.45; }
    50% { opacity: 1; }
    100% { opacity: 0.45; }
}

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(255,255,255,0.16), rgba(255,255,255,0.05));
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 22px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 44px;
    font-weight: 950;
    margin-bottom: 4px;
}

.hero-sub {
    font-size: 18px;
    color: #dbeafe;
}

.plane {
    font-size: 45px;
    animation: floatPlane 6s infinite ease-in-out;
    margin-top: 20px;
}

.globe-card {
    background: radial-gradient(circle, #38bdf8 0%, #1e40af 45%, #020617 78%);
    border-radius: 50%;
    width: 230px;
    height: 230px;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 94px;
    border: 3px solid rgba(255,255,255,0.35);
    box-shadow: 0 0 50px rgba(56,189,248,0.35);
    animation: pulse 2.5s infinite;
}

.card {
    background: rgba(255,255,255,0.11);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.22);
    backdrop-filter: blur(10px);
}

.city-card {
    background: linear-gradient(135deg, rgba(14,165,233,0.25), rgba(15,23,42,0.6));
    border: 1px solid rgba(125,211,252,0.35);
    border-radius: 22px;
    padding: 22px;
    min-height: 210px;
}

.score-card {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

.score-num {
    font-size: 30px;
    font-weight: 950;
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

.character {
    font-size: 70px;
    text-align: center;
    animation: glow 2s infinite;
}

.character-name {
    text-align: center;
    font-weight: 900;
    font-size: 18px;
}

.roadmap {
    display: flex;
    gap: 10px;
    justify-content: space-between;
    margin: 15px 0 25px 0;
}

.stop {
    flex: 1;
    text-align: center;
    padding: 10px;
    border-radius: 14px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.14);
    font-size: 13px;
}

.stop-active {
    background: #38bdf8;
    color: #020617;
    font-weight: 900;
    animation: pulse 2s infinite;
}

.stop-done {
    background: #22c55e;
    color: #052e16;
    font-weight: 900;
}

.mission-title {
    font-size: 30px;
    font-weight: 950;
}

.country-visual {
    font-size: 56px;
    margin-bottom: 8px;
}

.small-muted {
    color: #cbd5e1;
}

div.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #fbbf24);
    color: #020617;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
    font-weight: 900;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #7dd3fc, #fde68a);
    color: #020617;
}

.stRadio label {
    color: white !important;
}

hr {
    border-color: rgba(255,255,255,0.18);
}
</style>
""", unsafe_allow_html=True)


# ---------------------------
# Missions
# ---------------------------
MISSIONS = [
    {
        "country": "UAE",
        "city": "Dubai",
        "flag": "🇦🇪",
        "visual": "🏙️",
        "stage": "DEFINE",
        "character": "👩‍💼",
        "character_name": "Airport Operations Manager",
        "story": "Dubai International is facing long check-in queues during evening departures. Passengers are complaining online.",
        "question": "What is the correct quality problem to define?",
        "options": [
            "Average check-in waiting time is too high",
            "The airport needs more decoration",
            "Passengers do not like flying",
            "The aircraft colors are not attractive"
        ],
        "answer": "Average check-in waiting time is too high",
        "explain": "Define means identifying the real quality problem clearly."
    },
    {
        "country": "Qatar",
        "city": "Doha",
        "flag": "🇶🇦",
        "visual": "🕌",
        "stage": "MEASURE",
        "character": "👨‍💻",
        "character_name": "Data Analyst",
        "story": "Doha airport wants evidence before changing staffing plans.",
        "question": "Which measurement is most useful?",
        "options": [
            "Passenger waiting time by hour",
            "Color of boarding passes",
            "Number of airport shops",
            "Pilot age"
        ],
        "answer": "Passenger waiting time by hour",
        "explain": "Measure focuses on collecting data connected to the problem."
    },
    {
        "country": "UK",
        "city": "London",
        "flag": "🇬🇧",
        "visual": "🎡",
        "stage": "ANALYZE",
        "character": "🕵️",
        "character_name": "Root Cause Investigator",
        "story": "London airport data shows delays spike between 6 PM and 9 PM.",
        "question": "What is the most likely root cause?",
        "options": [
            "Not enough counters open during peak hours",
            "Too many airport signs",
            "The runway is too long",
            "Passengers carry passports"
        ],
        "answer": "Not enough counters open during peak hours",
        "explain": "Analyze means finding the cause behind the quality problem."
    },
    {
        "country": "France",
        "city": "Paris",
        "flag": "🇫🇷",
        "visual": "🗼",
        "stage": "IMPROVE",
        "character": "👷",
        "character_name": "Process Improvement Lead",
        "story": "Paris airport wants to reduce check-in delays without creating extra confusion.",
        "question": "Which improvement is best?",
        "options": [
            "Open more counters during peak hours and guide passengers to self-check-in",
            "Remove queue barriers",
            "Stop collecting data",
            "Close the check-in area"
        ],
        "answer": "Open more counters during peak hours and guide passengers to self-check-in",
        "explain": "Improve means applying a solution that targets the root cause."
    },
    {
        "country": "Japan",
        "city": "Tokyo",
        "flag": "🇯🇵",
        "visual": "🗻",
        "stage": "CONTROL",
        "character": "👨‍✈️",
        "character_name": "Quality Control Captain",
        "story": "Tokyo airport improved the process. Now they need to keep it stable.",
        "question": "What is the best control plan?",
        "options": [
            "Monitor waiting time using control charts and trigger extra staff if limits are exceeded",
            "Wait for complaints again",
            "Delete the data",
            "Only check the process once a year"
        ],
        "answer": "Monitor waiting time using control charts and trigger extra staff if limits are exceeded",
        "explain": "Control means maintaining the improvement using monitoring and response plans."
    },
    {
        "country": "USA",
        "city": "New York",
        "flag": "🇺🇸",
        "visual": "🗽",
        "stage": "FINAL MISSION",
        "character": "🧑‍🚀",
        "character_name": "Global Quality Commander",
        "story": "The global airport network asks you to choose the best full DMAIC strategy.",
        "question": "Which sequence is correct?",
        "options": [
            "Define the problem, measure data, analyze causes, improve the process, control results",
            "Improve first, then define later",
            "Control without measuring",
            "Guess the cause and stop"
        ],
        "answer": "Define the problem, measure data, analyze causes, improve the process, control results",
        "explain": "This is the full DMAIC cycle."
    },
]


# ---------------------------
# Game functions
# ---------------------------
def reset_game():
    st.session_state.started = False
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.finished = False
    st.session_state.history = []
    st.session_state.feedback = ""


if "started" not in st.session_state:
    reset_game()


# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">✈️ Airport Quality Quest</div>
    <div class="hero-sub">
        Travel around the world as a quality engineer and solve airport problems using DMAIC.
    </div>
    <div class="plane">✈️ ・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・🌍</div>
</div>
""", unsafe_allow_html=True)


# ---------------------------
# Start screen
# ---------------------------
if not st.session_state.started:
    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("""
        <div class="card">
            <h2>🎮 Mission Brief</h2>
            <p>
            You are the new Global Airport Quality Engineer. A network of airports is facing long queues,
            delays, and passenger complaints. Your job is to travel from country to country and solve each
            quality crisis using the DMAIC method.
            </p>
            <p>
            Each country represents a stage of the improvement journey. Make the right decisions, keep your
            passengers happy, and finish with the highest score possible.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Game Features</h3>
            <p>🌍 Global airport roadmap</p>
            <p>✈️ Animated flight atmosphere</p>
            <p>🧑‍💼 Moving mission characters</p>
            <p>🏆 Score, lives, and final ranking</p>
            <p>📘 DMAIC learning at each level</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div class='globe-card'>🌍</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="card">
            <h3>Rules</h3>
            <p>✅ Correct answer: +15 points</p>
            <p>❌ Wrong answer: -1 life</p>
            <p>❤️ You have 3 lives</p>
            <p>🏆 75+ = Excellent</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Start Global Mission"):
        st.session_state.started = True
        st.rerun()


# ---------------------------
# Main game
# ---------------------------
else:
    total = len(MISSIONS)
    level = st.session_state.level

    if not st.session_state.finished:
        mission = MISSIONS[level]

        # Score row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='score-card'>Score<br><div class='score-num'>{st.session_state.score}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='score-card'>Lives<br><div class='score-num'>{'❤️' * st.session_state.lives}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='score-card'>Level<br><div class='score-num'>{level + 1}/{total}</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='score-card'>Stage<br><div class='score-num'>{mission['stage']}</div></div>", unsafe_allow_html=True)

        st.write("")

        # Roadmap
        roadmap_html = "<div class='roadmap'>"
        for i, m in enumerate(MISSIONS):
            if i < level:
                cls = "stop stop-done"
            elif i == level:
                cls = "stop stop-active"
            else:
                cls = "stop"
            roadmap_html += f"<div class='{cls}'>{m['flag']}<br>{m['city']}</div>"
        roadmap_html += "</div>"
        st.markdown(roadmap_html, unsafe_allow_html=True)

        st.progress((level + 1) / total)

        # Mission area
        left, middle, right = st.columns([1, 1.4, 0.8])

        with left:
            st.markdown(f"""
            <div class="city-card">
                <div class="country-visual">{mission["visual"]}</div>
                <h2>{mission["flag"]} {mission["city"]}, {mission["country"]}</h2>
                <p class="small-muted">Current airport mission location</p>
            </div>
            """, unsafe_allow_html=True)

        with middle:
            st.markdown(f"""
            <div class="card">
                <span class="badge">{mission["stage"]}</span>
                <h2 class="mission-title">{mission["story"]}</h2>
                <hr>
            </div>
            """, unsafe_allow_html=True)

            choice = st.radio(
                mission["question"],
                mission["options"],
                key=f"choice_{level}"
            )

            submit_col, restart_col = st.columns([1, 1])

            with submit_col:
                if st.button("Submit Decision"):
                    if choice == mission["answer"]:
                        st.session_state.score += 15
                        st.session_state.feedback = "✅ Correct! " + mission["explain"]
                        st.session_state.history.append((mission["city"], mission["stage"], "Correct"))
                    else:
                        st.session_state.lives -= 1
                        st.session_state.feedback = "❌ Wrong. " + mission["explain"]
                        st.session_state.history.append((mission["city"], mission["stage"], "Wrong"))

                    if st.session_state.lives <= 0:
                        st.session_state.finished = True
                    elif level < total - 1:
                        st.session_state.level += 1
                    else:
                        st.session_state.finished = True

                    st.rerun()

            with restart_col:
                if st.button("Restart Mission"):
                    reset_game()
                    st.rerun()

        with right:
            st.markdown(f"""
            <div class="card">
                <div class="character">{mission["character"]}</div>
                <div class="character-name">{mission["character_name"]}</div>
                <p class="small-muted" style="text-align:center;">
                    Mission advisor
                </p>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    # End screen
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.header("🏁 Global Mission Complete")

        final_score = st.session_state.score

        if st.session_state.lives <= 0:
            st.error("Mission failed. The airport quality crisis was not fully solved.")
        elif final_score >= 75:
            st.balloons()
            st.success("Excellent! You completed the global airport DMAIC mission successfully.")
        elif final_score >= 50:
            st.warning("Good attempt. You solved several problems, but some decisions can improve.")
        else:
            st.error("Needs improvement. Review the DMAIC cycle and try again.")

        st.subheader(f"Final Score: {final_score} / 90")

        st.write("### Travel Summary")
        for i, item in enumerate(st.session_state.history, start=1):
            st.write(f"{i}. {item[0]} — {item[1]} — {item[2]}")

        st.write("### What the game teaches")
        st.write("- Define the correct airport quality problem")
        st.write("- Measure the right performance metric")
        st.write("- Analyze the root cause")
        st.write("- Improve the process using targeted actions")
        st.write("- Control the results with monitoring tools")

        if st.button("Play Again"):
            reset_game()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
