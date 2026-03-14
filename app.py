import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# Made a slight change to the UI layout by moving the "New Game" button above the guess input. The "New Game" button is now more prominently placed at the top of the game interface for better accessibility.
new_game = st.button("New Game 🔁")

# Calculate remaining attempts for display in the UI.
# Streamlit reruns the script from top to bottom whenever a button is clicked.
# Because the attempt counter is incremented later in the script, the UI would
# normally display the old value on the first guess. We calculate the remaining
# attempts here so the interface can immediately reflect the submitted guess.
remaining_attempts = attempt_limit - st.session_state.attempts

# Display the guessing range and instructions at the top of the game interface. This message remains static and does not change with each guess, providing a consistent reminder of the game's objective and the valid input range for the user.
st.info(
    f"Guess a number between {low} and {high}. ")

# Create UI controls (Submit, New Game, Show Hint).
# Buttons must be defined before we reference their values.
# We keep them here to preserve the original UI layout of the app.

# Form allows pressing Enter to submit the guess
with st.form("guess_form"):

    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )

    col1, col2= st.columns(2)

    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")

    with col2:
        show_hint = st.checkbox("Show hint", value=True)


# If the user clicks "Submit", Streamlit reruns the script immediately.
# The attempt counter is incremented later in the logic, so we temporarily
# subtract 1 here to show the correct remaining attempts in the UI.
# This prevents the first guess from incorrectly showing the full attempt count.
if submit:
    remaining_attempts -= 1
    
# Ensure remaining attempts doesn't go negative, which could happen if the user clicks "Submit" after reaching the attempt limit.
remaining_attempts = max(0, remaining_attempts)

# We have moved the info message about the guessing range to the top of the interface for better visibility. The remaining attempts info is now displayed separately below the input controls, allowing it to update dynamically with each guess while keeping the instructions consistently visible at the top.
# Display the guessing range and remaining attempts.
# This message updates dynamically based on the current difficulty
# and the calculated number of attempts left.
st.info(
    f"Attempts left: {remaining_attempts}"
)



# raw_guess = st.text_input(
#     "Enter your guess:",
#     key=f"guess_input_{difficulty}"
# )

if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )


# We have moved the developer debug info to the bottom of the script so it reflects the latest state after processing the user's guess. This way, when a user submits a guess, they can see how the internal state (like attempts and score) has changed in response to their action.

# Note: the developer debug panel shows the actual session_state values.
# The attempts counter is incremented later in the script, so the debug
# info may briefly show the previous value during the same rerun.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
