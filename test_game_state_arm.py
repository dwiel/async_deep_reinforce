import game_state_arm


def test_game_state_arm_easy():
    assert game_state_arm.best_score(0, 0) == 0
    assert game_state_arm.best_score(0, 1) == 1
    assert game_state_arm.best_score(0, 2) == 2


def test_game_state_arm_one_step():
    assert game_state_arm.best_score(0.01, 0) == 0
    assert game_state_arm.best_score(0.01, 1) == 1
    assert game_state_arm.best_score(0.01, 2) == 2


def test_game_state_arm_two_step():
    assert game_state_arm.best_score(0.02, 0) == 0
    assert game_state_arm.best_score(0.02, 1) == 0
    assert game_state_arm.best_score(0.02, 2) == 1
