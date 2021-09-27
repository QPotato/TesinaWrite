from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, List, NewType

import pandas

from numpy import array, transpose, zeros, dot, matmul, set_printoptions

Action = NewType("Action", int)
MixedStrategy = NewType("MixedStrategy", array)


@dataclass
class Game:
    name: str
    A: array
    B: array


def identical_interests(name: str, A: array) -> Game:
    return Game(name=name, A=A, B=A)


def zero_sum(name: str, A: array) -> Game:
    return Game(name=name, A=A, B=-A)


def symmetric(name: str, A: array) -> Game:
    return Game(name=name, A=A, B=transpose(A))


prisoners_dilemma = Game(
    name="prisoners_dilemma",
    A=array([
        [2, 0],
        [3, 1]
    ]),
    B=array([
        [2, 3],
        [0, 1]
    ])
)

rock_paper_scissors = zero_sum(
    name="rock_paper_scissors",
    A=array([
        [0, -1, 1],
        [1, 0, -1],
        [-1, 1, 0]
    ]),
)

shapley = Game(
    name="shapley",
    A=array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    B=array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ])
)


def theorem_4_4_1(eps: float) -> Game:
    return symmetric(
        name=f"theorem_4_4_1_eps_{eps}",
        A=array([
            [0,   -1,  -eps],
            [1,   0,   -eps],
            [eps, eps, 0]
        ]),
    )


def theorem_4_4_2(eps: float) -> Game:
    return identical_interests(
        name=f"theorem_4_4_2_eps_${eps}",
        A=array([
            [1, 2,       0],
            [0, 2 + eps, 2 + 2 * eps],
        ]),
    )


def theorem_4_4_3(eps: float) -> Game:
    return identical_interests(
        name=f"theorem_4_4_3_eps_{eps}",
        A=array([
            [1, 2,       0],
            [0, 2 + eps, 3],
        ]),
    )


class FictitiousPlay(ABC):
    def __init__(self, game: Game, fp_variant_name):
        self._game = game
        self._i: List[Action] = []
        self._j: List[Action] = []
        self._x: List[MixedStrategy] = []
        self._y: List[MixedStrategy] = []
        self._fp_variant_name = fp_variant_name

    @abstractmethod
    def run_learning_process(self, iterations) -> None:
        pass

    def print_process(self):
        iterations = len(self._y)
        i = correct_offset(self._i)
        j = correct_offset(self._j)
        Ay = [matmul(self._game.A, y_t) for y_t in self._y]
        xB = [matmul(x_t, self._game.B) for x_t in self._x]

        table = pandas.DataFrame(
            data=zip(zip(i, j), self._x, xB, self._y, Ay),
            columns=["$(i, j)$", "$x$", "$xB$", "$y$", "$Ay$"],
            index=range(1, iterations + 1)
        )
        table.index.name = "Iteration"
        pandas.options.display.float_format = '{:, .2f}'.format
        set_printoptions(formatter={'float_kind': "{:.2f}".format})

        print(f"\nGame: {self._game.name} || FP Variant: {self._fp_variant_name}")
        print(table.to_string(
            formatters=[lambda p: f"$(i_{p[0]},\ j_{p[1]})$", format_beliefs_1, format_beliefs_1,
                        format_beliefs_2, format_beliefs_2],
            float_format="{:.2f}".format,
        ))

    def _update_beliefs_1(self):
        y = sum(self._player_2_pure_strategy(action) for action in self._j) / len(self._j)
        self._y.append(y)

    def _choose_actions_1(self):
        y = self._y[-1]
        i = self._d_1(self._best_response_1(y))
        self._i.append(i)

    def _update_beliefs_2(self):
        x = sum(self._player_1_pure_strategy(i) for i in self._i) / len(self._i)
        self._x.append(x)

    def _choose_actions_2(self):
        x = self._x[-1]
        j = self._d_2(self._best_response_2(x))
        self._j.append(j)

    def _best_response_1(self, y: MixedStrategy) -> Set[Action]:
        N = self._player_1_actions_set()
        A = self._game.A
        pure = self._player_1_pure_strategy
        payoff = self._compute_payoff

        return argmax(N, lambda i: payoff(pure(i), A, y))

    def _best_response_2(self, x: MixedStrategy) -> Set[Action]:
        M = self._player_2_actions_set()
        B = self._game.B
        pure = self._player_2_pure_strategy
        payoff = self._compute_payoff

        return argmax(M, lambda j: payoff(x, B, pure(j)))

    def _compute_payoff(self, action_a, matrix, action_b):
        return dot(action_a, dot(matrix, action_b))

    def _player_1_pure_strategy(self, i: Action) -> MixedStrategy:
        n, _ = self._game.A.shape
        pure = zeros((1, n))
        pure[0][i] = 1
        return MixedStrategy(pure)

    def _player_2_pure_strategy(self, j: Action) -> MixedStrategy:
        _, m = self._game.B.shape
        pure = zeros((m, 1))
        pure[j][0] = 1
        return MixedStrategy(pure)

    def _player_1_actions_set(self) -> Set[Action]:
        n, _ = self._game.A.shape
        return set(range(n))

    def _player_2_actions_set(self) -> Set[Action]:
        _, m = self._game.B.shape
        return set(range(m))

    def _d_1(self, best_response_set: Set[Action]) -> Action:
        return min(best_response_set)

    def _d_2(self, best_response_set: Set[Action]) -> Action:
        return min(best_response_set)

    def _is_nash_equilibrium(self) -> bool:
        i = self._i[-1]
        j = self._j[-1]

        return i in self._best_response_1(self._player_2_pure_strategy(j)) \
            and j in self._best_response_2(self._player_1_pure_strategy(i))


class SFP(FictitiousPlay):
    def __init__(self, game: Game, i_0: Action, j_0: Action):
        super().__init__(game, "SFP")
        self._i = [i_0]
        self._j = [j_0]

    def run_learning_process(self, iterations) -> None:
        for _ in range(iterations):
            self._update_beliefs_1()
            self._update_beliefs_2()
            if self._is_nash_equilibrium():
                break
            self._choose_actions_1()
            self._choose_actions_2()


class AFP(FictitiousPlay):
    def __init__(self, game: Game, i_0: Action):
        super().__init__(game, "AFP")
        self._i = [i_0]
        self._j = []

    def run_learning_process(self, iterations) -> None:
        for _ in range(iterations):
            self._update_beliefs_2()
            self._choose_actions_2()
            self._update_beliefs_1()
            if self._is_nash_equilibrium():
                break
            self._choose_actions_1()


def argmax(args: Set[Action], f) -> Set[Action]:
    by_result = {arg: f(arg) for arg in args}
    maximum = max(by_result.values())
    return set(k for (k, v) in by_result.items() if v == maximum)


def correct_offset(actions):
    return [i + 1 for i in actions]


def format_beliefs_1(beliefs):
    formated_floats = "".join(
        f"{x:.2f},\ "
        for x in beliefs[0]
    )
    return f"$({formated_floats[:-3]})$"


def format_beliefs_2(beliefs):
    formated_floats = "".join(
        f"{x[0]:.2f},\ "
        for x in beliefs
    )
    return f"$({formated_floats[:-3]})$"


if __name__ == "__main__":
    i_0 = Action(0)
    j_0 = Action(0)
    epsilon = 2**-5
    games = [
        prisoners_dilemma,
        rock_paper_scissors,
        shapley,
        theorem_4_4_1(epsilon),
        theorem_4_4_2(epsilon),
        theorem_4_4_3(epsilon)
    ]
    iterations = 20

    for game in games:
        sfp = SFP(game, i_0, j_0)
        sfp.run_learning_process(iterations)
        sfp.print_process()

        afp = AFP(game, i_0)
        afp.run_learning_process(iterations)
        afp.print_process()