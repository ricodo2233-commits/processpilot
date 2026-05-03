import streamlit as st

st.set_page_config(
    page_title="Airport Quality Crisis",
    page_icon="✈️",
    layout="centered"
)

st.markdown("""
<style>
.main-box {
    background: #f7f9fc;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
}
.title {
    font-size: 34px;
    font-weight: 800;
}
.sub {
    color: #555;
    font-size: 17px;
}
.score-box {
    background: #111827;
    color: white;
    padding: 14px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


questions = [
    {
        "stage": "DEFINE",
        "scenario": "Passenger complaints are increasing because check-in queues are too long.",
        "question": "What is the main quality problem?",
        "options": [
            "Long waiting time at check-in",
            "High ticket prices",
            "Weather delays",
            "Airport decoration"
        ],
        "answer": "Long waiting time at check-in",
        "explanation": "The Define step identifies the main problem clearly."
    },
    {
        "stage": "MEASURE",
        "scenario": "The airport needs data to understand the current process performance.",
        "question": "Which metric should be measured?",
        "options": [
            "Average passenger waiting time",
            "Number of airplanes parked",
            "Pilot experience",
            "Restaurant sales"
        ],
        "answer": "Average passenger waiting time",
        "explanation": "The Measure step collects data related to the problem."
    },
    {
        "stage": "ANALYZE",
        "scenario": "Data shows queues become very long during peak hours.",
        "question": "What is the most likely root cause?",
        "options": [
            "Not enough check-in counters open during peak hours",
            "Too many empty counters",
            "Too many pilots",
            "Bad weather"
        ],
        "answer": "Not enough check-in counters open during peak hours",
        "explanation": "The Analyze step finds the cause of the problem."
    },
    {
        "stage": "IMPROVE",
        "scenario": "Management wants to reduce passenger waiting time.",
        "question": "What is the best improvement action?",
        "options": [
            "Open more check-in counters during peak hours",
            "Ignore the complaints",
            "Close the airport earlier",
            "Increase ticket prices"
        ],
        "answer": "Open more check-in counters during peak hours",
        "explanation": "The Improve step selects an action that directly solves the root cause."
    },
    {
        "stage": "CONTROL",
        "scenario": "The new process is working, but the airport wants to keep it stable.",
        "question": "How should the airport control the improvement?",
        "options": [
            "Monitor waiting time using control charts",
            "Stop collecting data",
            "Wait for more complaints",
            "Remove check-in staff"
        ],
        "answer": "Monitor waiting time using control charts",
        "explanation": "The Control step makes sure the improvement continues over time."
    }
]


if "level" not in st.session_state:
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.feedback = ""


st.markdown("<div class='title'>✈️ Airport Quality Crisis</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>A DMAIC problem-solving game for quality engineering</div>", unsafe_allow_html=True)
st.write("")

st.markdown(
    f"<div class='score-box'>Score: {st.session_state.score} / 100</div>",
    unsafe_allow_html=True
)

st.write("")

if not st.session_state.finished:
    q = questions[st.session_state.level]

    st.markdown("<div class='main-box'>", unsafe_allow_html=True)

    st.subheader(f"Level {st.session_state.level + 1}: {q['stage']}")
    st.write(q["scenario"])

    choice = st.radio(q["question"], q["options"], key=f"q_{st.session_state.level}")

    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.session_state.score += 20
            st.session_state.feedback = "✅ Correct! " + q["explanation"]
        else:
            st.session_state.feedback = "❌ Not correct. " + q["explanation"]

        if st.session_state.level < len(questions) - 1:
            st.session_state.level += 1
        else:
            st.session_state.finished = True

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.feedback:
        st.info(st.session_state.feedback)

else:
    st.success("Game completed!")

    final_score = st.session_state.score

    if final_score >= 80:
        st.balloons()
        st.subheader("🏆 Excellent Quality Engineer!")
        st.write("You applied DMAIC correctly and improved the airport process.")
    elif final_score >= 60:
        st.subheader("👍 Good Attempt")
        st.write("You understood most DMAIC steps, but some decisions need improvement.")
    else:
        st.subheader("📘 Needs Improvement")
        st.write("Review the DMAIC steps and try again.")

    st.write(f"Final Score: **{final_score}/100**")

    if st.button("Restart Game"):
        st.session_state.level = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.feedback = ""
        st.rerun()
