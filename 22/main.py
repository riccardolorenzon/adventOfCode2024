from collections import defaultdict
import math
import sys
from typing import Generator


def read_input() -> Generator:
    with open(sys.argv[1]) as f:
        while line := f.readline():
            yield line.strip()


class Secret:
    def __init__(self, secret: str):
        self.secret = int(secret)
        self.last_digits_by_sequence = defaultdict(lambda: None)

    def evolve(self, n_times):
        sequence = []
        previous_digit = None
        for _ in range(n_times):
            self.evolve_secret_phase_1()
            self.evolve_secret_phase_2()
            self.evolve_secret_phase_3()
            current_digit = int(str(self.secret)[-1:])
            if previous_digit is not None:
                sequence.append(current_digit - previous_digit)
            previous_digit = current_digit
            if len(sequence) == 4:
                if self.last_digits_by_sequence[tuple(sequence)] is None:
                    self.last_digits_by_sequence[tuple(sequence)] = current_digit
                sequence = sequence[1:]
        return self.secret

    def evolve_secret_phase_1(self):
        value = self.secret * 64
        self.mix(value)
        self.prune()

    def evolve_secret_phase_2(self):
        value = math.floor(self.secret / 32)
        self.mix(value)
        self.prune()

    def evolve_secret_phase_3(self):
        self.value = self.secret * 2048
        self.mix(self.value)
        self.prune()

    def mix(self, value):
        self.secret = self.secret ^ value

    def prune(self):
        self.secret = self.secret % 16777216


def main():
    print("part 1")
    res = 0
    secrets: list[Secret] = []
    all_sequences = set()
    for secret in read_input():
        s = Secret(secret)
        res += s.evolve(2000)
        secrets.append(s)
        for seq in s.last_digits_by_sequence.keys():
            all_sequences.add(seq)
    max_gain = 0
    print(res)
    print("part 2")
    for sequence in all_sequences:
        gain = 0
        for secret in secrets:
            if secret.last_digits_by_sequence[sequence] is None:
                pass
            else:
                gain += secret.last_digits_by_sequence[sequence]
        max_gain = max(max_gain, gain)
    print(max_gain)


if __name__ == "__main__":
    main()
