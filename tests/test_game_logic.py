from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# ========== Tests for get_range_for_difficulty ==========

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_default_range():
    # Invalid difficulty should return default (Normal)
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100

# ========== Tests for parse_guess ==========

def test_parse_valid_integer():
    ok, value, error = parse_guess("50")
    assert ok == True
    assert value == 50
    assert error is None

def test_parse_float_to_int():
    ok, value, error = parse_guess("50.7")
    assert ok == True
    assert value == 50
    assert error is None

def test_parse_empty_string():
    ok, value, error = parse_guess("")
    assert ok == False
    assert value is None
    assert error == "Enter a guess."

def test_parse_none():
    ok, value, error = parse_guess(None)
    assert ok == False
    assert value is None
    assert error == "Enter a guess."

def test_parse_invalid_number():
    ok, value, error = parse_guess("abc")
    assert ok == False
    assert value is None
    assert error == "That is not a number."

def test_parse_negative_number():
    ok, value, error = parse_guess("-10")
    assert ok == True
    assert value == -10
    assert error is None

# ========== Tests for check_guess ==========

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_guess_boundary_high():
    # Edge case: guess is just above secret
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"

def test_guess_boundary_low():
    # Edge case: guess is just below secret
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"

# ========== Tests for update_score ==========

def test_update_score_win_first_attempt():
    # Winning on first attempt should give 80 points
    new_score = update_score(0, "Win", 1)
    assert new_score == 80

def test_update_score_win_with_attempts():
    # Winning after many attempts should give lower points
    new_score = update_score(0, "Win", 5)
    assert new_score == 40

def test_update_score_win_many_attempts():
    # Winning after many attempts should floor at 10 points
    new_score = update_score(0, "Win", 20)
    assert new_score == 10

def test_update_score_too_high_even_attempt():
    # Even attempt on "Too High" adds 5 points
    new_score = update_score(100, "Too High", 2)
    assert new_score == 105

def test_update_score_too_high_odd_attempt():
    # Odd attempt on "Too High" subtracts 5 points
    new_score = update_score(100, "Too High", 3)
    assert new_score == 95

def test_update_score_too_low():
    # "Too Low" always subtracts 5 points
    new_score = update_score(100, "Too Low", 2)
    assert new_score == 95

def test_update_score_too_low_odd():
    # "Too Low" always subtracts 5 points (odd attempt too)
    new_score = update_score(100, "Too Low", 3)
    assert new_score == 95

def test_update_score_invalid_outcome():
    # Unknown outcome should not change score
    new_score = update_score(100, "Unknown", 1)
    assert new_score == 100
