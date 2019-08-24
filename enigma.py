#!/usr/bin/env python3

"""
    enigma.py
    2019.08
    v0.9
"""


class Rotor:
    def __init__(
        self, mapping: list, turnover_notch: list = [], start_position: str = "a"
    ):
        self.mapping = mapping
        self.offset = ord(start_position) - ord("a")
        self.turnover_notch = turnover_notch

    def __getitem__(self, char):
        index = (ord(char.lower()) - ord("a") + self.offset) % 26
        return self.mapping[index]

    def rotate(self):
        self.offset = (self.offset + 1) % 26

    def current_position(self):
        return chr(self.offset + ord("a"))


class Reflector(Rotor):
    def __init__(self, mapping):
        self.mapping = mapping
        self.offset = 0

        for idx, to_ in enumerate(mapping):
            from_ = chr(idx + ord("a"))
            if self[from_] != to_:
                raise ValueError("Wrong mapping. Reflector must have 2-way mapping.")


class Enigma:
    def __init__(
        self,
        reflector: Reflector,
        left_rotor: Rotor,
        mid_rotor: Rotor,
        right_rotor: Rotor,
        double_step: bool = False,
    ):
        self.left_rotor = left_rotor
        self.mid_rotor = mid_rotor
        self.right_rotor = right_rotor
        self.reflector = reflector

        self.double_step = double_step

    def __getitem__(self, char):
        if not char.isalpha():
            return char

        self.rotate_mechanism()

        righttoleft = self.left_rotor[self.mid_rotor[self.right_rotor[char]]]
        reflected = self.reflector[righttoleft]
        lefttoright = self.right_rotor[self.mid_rotor[self.left_rotor[reflected]]]

        return lefttoright

    def rotate_mechanism(self):
        L = self.left_rotor
        M = self.mid_rotor
        R = self.right_rotor

        m_should_rotate = False
        l_should_rotate = False

        if self.double_step:
            if R.current_position() in R.turnover_notch:
                m_should_rotate = True
            if M.current_position() in M.turnover_notch:
                m_should_rotate = True
                l_should_rotate = True

        else:
            if R.current_position() in R.turnover_notch:
                m_should_rotate = True
                if M.current_position() in M.turnover_notch:
                    l_should_rotate = True

        R.rotate()
        if m_should_rotate:
            M.rotate()
        if l_should_rotate:
            L.rotate()

    def display_position(self):
        left = self.left_rotor.current_position()
        mid = self.mid_rotor.current_position()
        right = self.right_rotor.current_position()

        print(f"{left.upper()}{mid.upper()}{right.upper()}")

    def encrypt(self, text):
        return "".join([self[char] for char in text])


def main():
    enigma1_rotorI = Rotor(list("ekmflgdqvzntowyhxuspaibrcj"), turnover_notch=["q"])
    enigma1_rotorII = Rotor(list("ajdksiruxblhwtmcqgznpyfvoe"), turnover_notch=["e"])
    enigma1_rotorIII = Rotor(list("bdfhjlcprtxvznyeiwgakmusqo"), turnover_notch=["v"])
    enigma1_wide_B_reflector = Reflector(list("yruhqsldpxngokmiebfzcwvjat"))

    my_enigma = Enigma(
        enigma1_wide_B_reflector,
        enigma1_rotorI,
        enigma1_rotorII,
        enigma1_rotorIII,
        double_step=True,
    )

    print(my_enigma.encrypt("hello."))


if __name__ == "__main__":
    main()
