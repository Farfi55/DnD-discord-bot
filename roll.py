from random import randint


def d(facce=6, volte=1):
    val = 0
    for _ in range(volte):
        val += randint(1, facce)
    return val
