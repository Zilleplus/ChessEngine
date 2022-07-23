from multiprocessing import get_context
from typing import Any, Awaitable, Optional
import chess
from mmEngine.agents import Agent, RandomAgent, MinMaxAgent, MinMaxAlphaBetaAgent
from mmEngine.value_funtions import MaterialCount, NNKerasValueFunction, ValueFunctionMaterial
from dataclasses import dataclass

import asyncio
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from pathlib import Path

@dataclass
class Result:
    score_white: int
    score_black: int
    error: Optional[str]
    winner: Optional[bool]

def simulate(agent1: Agent, agent2: Agent, seed: int, num_moves: int = 50):
    np.random.seed(seed)
    b = chess.Board()
    error: Optional[str] = None
    for i in range(num_moves):
        if b.is_game_over():
            break
        m1 = agent1.select_move(b)
        if m1 is None:
            error = "agent1 can't find move"
            break
        b.push(m1)

        if b.is_game_over():
            break
        m2 = agent2.select_move(b)
        if m2 is None:
            error = "agent2 can't find move"
            break
        b.push(m2)


    (white_score, black_score) = MaterialCount(b)

    winner: Optional[bool] = None
    outcome = b.outcome()
    if outcome is not None:
        winner = outcome.winner
    return Result(white_score, black_score, error, winner)

async def simulate_games(agent1_factory, agent2_factory, num_games: int=10) -> list[Result]:
    context = get_context('spawn')
    with ProcessPoolExecutor(mp_context=context) as process_pool:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        sims = [partial(simulate, agent1_factory(), agent2_factory(), seed=i) for i in range(num_games)]

        coros: list[Awaitable[Result]] = [loop.run_in_executor(process_pool, call) for call in sims]
        results: list[Result] = await asyncio.gather(*coros)


        avg_white_score = sum([x.score_white for x in results])/len(results)
        print(f"average white score={avg_white_score}")
        avg_black_score = sum([x.score_black for x in results])/len(results)
        print(f"average black score={avg_black_score}")

        white_wins: int = sum([1 if x.winner is not None and x.winner else 0 for x in results])
        print(f"white has {white_wins} wins")

        black_wins: int = sum([1 if x.winner is not None and not x.winner else 0 for x in results])
        print(f"black has {black_wins} wins")

        return results


def main() -> None:
    # At the moment tensorflow can't seem to allocate the memory in multiprocesssing,
    # use the simulate_serial instead...
    nn_location = Path("./trial_network.keras")
    # nnEvalFunc = NNKerasValueFunction(nn_location)

    fac1 = lambda: MinMaxAlphaBetaAgent(evaluation_function=ValueFunctionMaterial(), depth=3)
    fac2 = lambda: RandomAgent()
    results = asyncio.run(simulate_games(fac1, fac2,num_games=20))

    for r in results:
        print(r)

if __name__ == "__main__":
    main()