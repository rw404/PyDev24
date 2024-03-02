import argparse
import random
from typing import Callable, List, Tuple
from urllib import request


def bullcows(guess: str, secret: str) -> Tuple[int, int]:
    if len(guess) != len(secret):
        return -1, -1
    bulls = sum(
        1
        for (guess_letter, secret_letter) in zip(guess, secret)
        if guess_letter == secret_letter
    )

    cows = len(set(guess) & set(secret))

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
    print(prompt)
    guess = ""
    if valid is not None:
        guess = input()
        while guess not in valid:
            guess = input()

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


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
