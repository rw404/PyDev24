import argparse
import random
from collections import Counter
from io import StringIO
from typing import Callable, List, Tuple
from urllib import request

import cowsay


def bullcows(guess: str, secret: str) -> Tuple[int, int]:
    if len(guess) != len(secret):
        return -1, -1
    bulls = sum(
        1
        for (guess_letter, secret_letter) in zip(guess, secret)
        if guess_letter == secret_letter
    )

    cows = sum((Counter(guess) & Counter(secret)).values())

    return bulls, cows


def gameplay(ask: Callable, inform: Callable, words: List[str]) -> int:
    secret = random.choice(words)

    guession_count = 0
    guess = ""
    while guess != secret:
        guess = ask("Введите слово: ", words)
        bulls, cows = bullcows(guess, secret)

        inform("Быки: {}, Коровы: {}", bulls, cows)
        guession_count += 1

    ask(f"Слово угадано! Попыток сделано: {guession_count}.")
    return guession_count


def ask(prompt: str, valid: List[str] = None) -> str:
    cow = cowsay.read_dot_cow(
        StringIO(
            """
$the_cow = <<EOC;
         $thoughts
          $thoughts
             __
            /  \\
            |  |
            @  @
            |  |
            || |/
            || ||
            |\\_/|
            \\___/
EOC
"""
        )
    )

    print(
        cowsay.cowsay(
            message=prompt,
            cowfile=cow,
            preset=None,
            eyes=cowsay.Option.eyes,
            tongue=cowsay.Option.tongue,
            width=40,
            wrap_text=True,
        )
    )
    guess = ""
    if valid is not None:
        guess = input()
        while guess not in valid:
            print(
                cowsay.cowsay(
                    message="Слово не в словаре! " + prompt,
                    cowfile=cow,
                    preset=None,
                    eyes=cowsay.Option.eyes,
                    tongue=cowsay.Option.tongue,
                    width=40,
                    wrap_text=True,
                )
            )
            guess = input()

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(
        cowsay.cowsay(
            message=format_string.format(bulls, cows),
            cow=cowsay.get_random_cow(),
            preset=None,
            eyes=cowsay.Option.eyes,
            tongue=cowsay.Option.tongue,
            width=40,
            wrap_text=True,
            cowfile=None,
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", type=str)
    parser.add_argument("length", nargs="?", default=5, type=int)

    args = parser.parse_args()

    if ":" in args.dictionary:
        # Url parser
        words = request.urlopen(args.dictionary).read()
        words = words.decode().split()
    else:
        # File reading
        with open(args.dictionary) as file:
            words = file.readlines()

    words = [i.strip() for i in words if len(i) == args.length]

    gameplay(ask, inform, words)


if __name__ == "__main__":
    main()
