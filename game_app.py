import streamlit as st
import random

st.set_page_config(
    page_title="Airport Quality Crisis",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #06111f 0%, #0f2a44 45%, #152f4f 100%);
    color: white;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}

.game-card {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
}

.choice-card {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 16px;
    margin-top: 10px;
}

.big-title {
    font-size: 42px;
    font-weight: 900;
}

.subtitle {
    font-size: 18px;
    color: #d8e7ff;
}

.badge {
    display: inline-block;
    background: #fbbf24;
    color: #111827;
    padding: 8px 14px;
    border-radius: 999px;
    font-weight: 800;
    margin-right: 8px;
}

.score {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 900;
}

.small-muted {
    color: #cbd5e1;
    font-size: 14px;
}

div.stButton > button {
    background: #38bdf8;
    color: #03111f;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 800;
}

div.stButton > button:hover {
    background: #7dd3fc;
    color: #03111f;
}

.stRadio label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


MISSIONS = [
    {
        "stage": "DEFINE",
        "location": "Terminal 3 Check-in Hall",
        "story": "Passengers are angry because the check-in queue is taking too long. Social media complaints are increasing.",
        "question": "What should the quality team define as the main problem?",
        "options": [
            "Average passenger waiting time is too high",
            "The airport logo needs redesigning",
            "The weather is bad",
            "Passengers are arriving too early"
        ],
        "answer": "Average passenger waiting time is too high",
        "explain": "The Define stage must clearly identify the quality problem."
    },
    {
        "stage": "DEFINE",
        "location": "Airport Operations Room",
        "story": "Management wants a clear project goal before approving the improvement project.",
        "question": "Which goal is best?",
        "options": [
            "Reduce average check-in waiting time by 30% within 4 weeks",
            "Make the terminal look nicer",
            "Tell passengers to wait patiently",
            "Increase ticket prices"
        ],
        "answer": "Reduce average check-in waiting time by 30% within 4 weeks",
        "explain": "A good goal is specific, measurable, and linked to the problem."
    },
    {
        "stage": "MEASURE",
        "location": "Check-in Counter Data Desk",
        "story": "You need to collect data before making decisions.",
        "question": "Which data should be collected first?",
        "options": [
            "Passenger waiting time by hour",
            "Color of staff uniforms",
            "Number of coffee shops",
            "Pilot names"
        ],
        "answer": "Passenger waiting time by hour",
        "explain": "The Measure stage collects data related directly to the process problem."
    },
    {
        "stage": "MEASURE",
        "location": "Baggage Drop Area",
        "story": "The team wants to visualize delays across the day.",
        "question": "Which tool is most useful?",
        "options": [
            "Run chart",
            "Random drawing",
            "Logo chart",
            "Seat map"
        ],
        "answer": "Run chart",
        "explain": "A run chart shows how waiting time changes over time."
    },
    {
        "stage": "ANALYZE",
        "location": "Peak-Hour Investigation",
        "story": "Data shows delays increase sharply from 6 PM to 9 PM.",
        "question": "What is the most likely root cause?",
        "options": [
            "Not enough check-in counters open during peak hours",
            "Too many empty gates",
            "The runway is too long",
            "Passengers like waiting"
        ],
        "answer": "Not enough check-in counters open during peak hours",
        "explain": "The Analyze stage identifies the cause behind the performance issue."
    },
    {
        "stage": "ANALYZE",
        "location": "Cause-and-Effect Room",
        "story": "The manager asks which category this root cause belongs to.",
        "question": "Which cause category fits best?",
        "options": [
            "Manpower / staffing",
            "Weather",
            "Airport decoration",
            "Aircraft design"
        ],
        "answer": "Manpower / staffing",
        "explain": "Insufficient counter staffing is a manpower-related cause."
    },
    {
        "stage": "IMPROVE",
        "location": "Action Planning Room",
        "story": "You must choose the best improvement action.",
        "question": "What should the airport do?",
        "options": [
            "Open more counters during peak hours",
            "Ignore the complaints",
            "Close the terminal",
            "Remove self-check-in kiosks"
        ],
        "answer": "Open more counters during peak hours",
        "explain": "The Improve stage chooses an action that directly addresses the root cause."
    },
    {
        "stage": "IMPROVE",
        "location": "Passenger Flow Zone",
        "story": "The airport also wants to reduce pressure on counters.",
        "question": "Which additional improvement helps?",
        "options": [
            "Encourage self-check-in kiosks for eligible passengers",
            "Remove queue signs",
            "Turn off screens",
            "Stop measuring waiting time"
        ],
        "answer": "Encourage self-check-in kiosks for eligible passengers",
        "explain": "Self-check-in can reduce demand at manual counters."
    },
    {
        "stage": "CONTROL",
        "location": "Control Tower Dashboard",
        "story": "The improvement worked. Now the airport must maintain performance.",
        "question": "How should the process be controlled?",
        "options": [
            "Monitor waiting time with control charts",
            "Stop tracking data",
            "Wait for complaints again",
            "Only check once per year"
        ],
        "answer": "Monitor waiting time with control charts",
        "explain": "The Control stage uses monitoring to keep the improved process stable."
    },
    {
        "stage": "CONTROL",
        "location": "Final Quality Audit",
        "story": "The quality team needs a response plan if waiting time rises again.",
        "question": "What is the best control plan?",
        "options": [
            "Set a trigger level and add staff when waiting time exceeds it",
            "Ignore the dashboard",
            "Blame passengers",
            "Delete old data"
        ],
        "answer": "Set a trigger level and add staff when waiting time exceeds it",
        "explain": "A good control plan defines what action to take when performance worsens."
    }
]


def reset_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.finished = False
    st.session_state.started = False
    st.session_state.feedback = ""
    st.session_state.history = []


if "level" not in st.session_state:
    reset_game()


st.markdown("""
<div class="hero">
    <div class="big-title">✈️ Airport Quality Crisis</div>
    <div class="subtitle">
        A DMAIC quality engineering game where you play as the airport quality manager.
        Fix delays, reduce complaints, and save the terminal operation.
    </div>
</div>
""", unsafe_allow_html=True)


if not st.session_state.started:
    left, right = st.columns([2, 1])

    with left:
        st.markdown("""
        <div class="game-card">
        <h2>Mission Brief</h2>
        <p>
        Passenger complaints are rising at a busy international airport.
        Your job is to use the DMAIC method to identify the problem, measure it,
        analyze root causes, improve the process, and control the results.
        </p>
        <p><b>Win condition:</b> finish the mission with the highest score possible.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="game-card">
        <h3>Game Rules</h3>
        <p>✅ Correct answer: +10 points</p>
        <p>❌ Wrong answer: -1 life</p>
        <p>🏆 80+ score: Excellent</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Start Mission"):
        st.session_state.started = True
        st.rerun()

else:
    total = len(MISSIONS)
    level = st.session_state.level

    if not st.session_state.finished:
        mission = MISSIONS[level]

        top1, top2, top3 = st.columns(3)

        with top1:
            st.markdown(f"<div class='score'>Score<br>{st.session_state.score}</div>", unsafe_allow_html=True)
        with top2:
            st.markdown(f"<div class='score'>Lives<br>{'❤️' * st.session_state.lives}</div>", unsafe_allow_html=True)
        with top3:
            st.markdown(f"<div class='score'>Level<br>{level + 1} / {total}</div>", unsafe_allow_html=True)

        st.progress((level + 1) / total)

        st.markdown(f"""
        <div class="game-card">
            <span class="badge">{mission["stage"]}</span>
            <span class="small-muted">{mission["location"]}</span>
            <h2>{mission["story"]}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='choice-card'>", unsafe_allow_html=True)
        choice = st.radio(mission["question"], mission["options"], key=f"mission_{level}")
        st.markdown("</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns([1, 1])

        with col_a:
            if st.button("Submit Decision"):
                correct = choice == mission["answer"]

                if correct:
                    st.session_state.score += 10
                    st.session_state.feedback = "✅ Correct decision. " + mission["explain"]
                    st.session_state.history.append((mission["stage"], "Correct"))
                else:
                    st.session_state.lives -= 1
                    st.session_state.feedback = "❌ Wrong decision. " + mission["explain"]
                    st.session_state.history.append((mission["stage"], "Wrong"))

                if st.session_state.lives <= 0:
                    st.session_state.finished = True
                elif st.session_state.level < total - 1:
                    st.session_state.level += 1
                else:
                    st.session_state.finished = True

                st.rerun()

        with col_b:
            if st.button("Restart"):
                reset_game()
                st.rerun()

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    else:
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)

        st.header("🏁 Mission Complete")

        final_score = st.session_state.score

        if st.session_state.lives <= 0:
            st.error("The airport crisis was not solved. You ran out of lives.")
        elif final_score >= 80:
            st.balloons()
            st.success("Excellent work! You successfully managed the airport quality crisis.")
        elif final_score >= 60:
            st.warning("Good attempt. You solved part of the crisis, but some decisions can improve.")
        else:
            st.error("Needs improvement. Review the DMAIC steps and try again.")

        st.subheader(f"Final Score: {final_score} / 100")

        st.write("### Decision Summary")
        for i, item in enumerate(st.session_state.history, start=1):
            st.write(f"{i}. {item[0]} — {item[1]}")

        st.write("### What this game teaches")
        st.write("- Define the correct quality problem")
        st.write("- Measure the right process metric")
        st.write("- Analyze the root cause")
        st.write("- Improve the process using targeted actions")
        st.write("- Control the process using monitoring and response plans")

        if st.button("Play Again"):
            reset_game()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
