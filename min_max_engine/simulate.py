from dataclasses import dataclass
from optparse import Option
from typing import Optional, Coroutine
import chess
from mmEngine.agents import Agent, RandomAgent, MinMaxAgent
from numpy import blackman
from mmEngine.value_funtions import MaterialCount
import asyncio

@dataclass
class Result:
    score_white: int
    score_black: int
    error: Optional[str]

def simulate(agent1: Agent, agent2: Agent, num_moves: int = 20):
    b = chess.Board()
    error: Optional[str] = None
    for i in range(num_moves):
        m1 = agent1.select_move(b)
        if m1 is None:
            error = "m1 can't find move"
            break
        b.push(m1)

        m2 = agent2.select_move(b)
        if m2 is None:
            error = "m2 can't find move"
            break
        b.push(m2)


    (white_score, black_score) = MaterialCount(b)

    return Result(white_score, black_score, error)

def simulate_games(agent1_factory, agent2_factory, num_games: int=10):
    # todo: do this is parallle, takes way to long otherwise
    # -> Find out for asyncio works.
    # simulations: list[Coroutine] = []
    # res = asyncio.gather(*simulations)

    results: list[Result] = []
    for i in range(num_games):
        a1 = agent1_factory()
        a2 = agent2_factory()
        res = simulate(a1, a2, num_moves=30)
        results.append(res)

    avg_white_score = sum([x.score_white for x in results])/num_games
    print(f"average white score={avg_white_score}")
    avg_black_score = sum([x.score_black for x in results])/num_games
    print(f"average black score={avg_black_score}")

    return results


fac1 = lambda: MinMaxAgent()
fac2 = lambda: RandomAgent()
results = simulate_games(fac1, fac2,num_games=2)

print(results[0])
print(results[1])