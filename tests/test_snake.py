from quantumfx.snake import SnakeGame


def test_reverse_and_double_turn_rejected():
    game = SnakeGame()
    game.turn((-1, 0))
    assert game.queued == (1, 0)
    game.turn((0, -1))
    game.turn((-1, 0))
    assert game.queued == (0, -1)


def test_food_grows_and_scores():
    game = SnakeGame()
    x, y = game.body[0]
    game.food = (x+1, y)
    game.step()
    assert len(game.body) == 4 and game.score == 10
    assert game.food not in game.body


def test_wall_and_reset():
    game = SnakeGame()
    game.body = [(19, 1), (18, 1), (17, 1)]
    game.step()
    assert game.over
    game.reset()
    assert not game.over and game.score == 0


def test_tail_cell_allowed_when_tail_moves():
    game = SnakeGame()
    game.body = [(1, 1), (1, 2), (0, 2), (0, 1)]
    game.direction = game.queued = (-1, 0)
    game.food = (5, 5)
    game.step()
    assert not game.over and game.body[0] == (0, 1)


def test_self_collision():
    game = SnakeGame()
    game.body = [(1, 1), (1, 2), (2, 2), (2, 1), (3, 1)]
    game.step()
    assert game.over


def test_full_board_wins():
    game = SnakeGame(size=3)
    game.body = [(x, y) for x in range(3) for y in range(3)]
    game.spawn()
    assert game.won and game.over and game.food is None
