from game.api import Actions, Entities


def script(check, x, y):
    return Actions.RIGHT if check(Entities.LEVEL) == 1 else Actions.PASS
