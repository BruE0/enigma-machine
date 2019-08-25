#!/usr/bin/env python3

"""
    enigma.py
    2019.08
    v1.2
"""


from string import ascii_lowercase
from collections import deque


class Rotor:
    def __init__(
        self, listmapping: list, turnover_notch: list = [], start_position: str = "a"
    ):
        self.mapping_ahead = deque(listmapping, maxlen=26)
        self.mapping_back = deque(ascii_lowercase, maxlen=26)
        offset = self.mapping_back.index(start_position)
        self.mapping_ahead.rotate(-offset)
        self.mapping_back.rotate(-offset)
        self.turnover_notch = turnover_notch

    def mapping(self, char, backwards=False):
        if backwards:
            mapp = self.mapping_back
            other = self.mapping_ahead
        else:
            mapp = self.mapping_ahead
            other = self.mapping_back

        index = mapp.index(char)
        return other[index]

    def rotate(self):
        self.mapping_back.rotate(-1)

    def current_position(self):
        return self.mapping_back[0]


class Reflector:
    def __init__(self, listmapping: list):
        self.mapping_twoway = dict(zip(ascii_lowercase, listmapping))

        for k, v in self.mapping_twoway.items():
            if self.mapping_twoway[v] != k:
                raise ValueError("Wrong mapping. Reflector must have 2-way mapping.")

    def mapping(self, char):
        return self.mapping_twoway[char]


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

        output = self.right_rotor.mapping(char.lower())
        output = self.mid_rotor.mapping(output)
        output = self.left_rotor.mapping(output)
        output = self.reflector.mapping(output)
        output = self.left_rotor.mapping(output, backwards=True)
        output = self.mid_rotor.mapping(output, backwards=True)
        output = self.right_rotor.mapping(output, backwards=True)

        return output

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

    def set_position(self, position):
        L, M, R = [char.lower() for char in position]

        while self.left_rotor.current_position() != L:
            self.left_rotor.rotate()
        while self.mid_rotor.current_position() != M:
            self.mid_rotor.rotate()
        while self.right_rotor.current_position() != R:
            self.right_rotor.rotate()

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


    word = "hello"

    my_enigma.set_position("AAA")
    encrypted = my_enigma.encrypt(word)

    print(f"{word} was encrypted to {encrypted} !")

    my_enigma.set_position("AAA")
    decrypted = my_enigma.encrypt(encrypted)

    print(f"{encrypted} was decrypted to {decrypted} !")


if __name__ == "__main__":
    main()
