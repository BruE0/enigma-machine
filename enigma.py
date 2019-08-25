#!/usr/bin/env python3

"""
    enigma.py
    2019.08
    v1.3
"""


from string import ascii_lowercase


def chr2int(char):
    return ord(char.lower()) - ord("a")


def int2char(intt):
    return chr(intt + ord("a"))


class Rotor:
    def __init__(
        self, listmapping: list, turnover_notch: list = [], start_position: str = "a"
    ):
        self.mapping = dict(zip(ascii_lowercase, listmapping))
        self.backmapping = dict(zip(listmapping, ascii_lowercase))
        self.offset = ord(start_position) - ord("a")
        self.turnover_notch = turnover_notch

    def forward_mapping(self, char):
        offsetted_char = int2char((chr2int(char) + self.offset)%26)
        rotor_internal_mapping = self.mapping[offsetted_char]
        end_position_for_next = int2char((chr2int(rotor_internal_mapping) - self.offset)%26)
        return end_position_for_next

    def backward_mapping(self, char):
        offsetted_char = int2char((chr2int(char) + self.offset)%26)
        rotor_internal_mapping = self.backmapping[offsetted_char]
        end_position_for_next = int2char((chr2int(rotor_internal_mapping) - self.offset)%26)
        return end_position_for_next

    def rotate(self):
        self.offset = (self.offset + 1) % 26

    def current_position(self):
        return chr(self.offset + ord("a"))

    def set_position(self, char):
        self.offset = ord(char) - ord("a")


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

        output = self.right_rotor.forward_mapping(char.lower())
        output = self.mid_rotor.forward_mapping(output)
        output = self.left_rotor.forward_mapping(output)
        output = self.reflector.mapping(output)
        output = self.left_rotor.backward_mapping(output)
        output = self.mid_rotor.backward_mapping(output)
        output = self.right_rotor.backward_mapping(output)

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

        self.left_rotor.set_position(L)
        self.mid_rotor.set_position(M)
        self.right_rotor.set_position(R)

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

    my_enigma.set_position("aaa")
    encrypted = my_enigma.encrypt(word)

    print(f"{word} was encrypted to {encrypted} !")

    my_enigma.set_position("aaa")
    decrypted = my_enigma.encrypt(encrypted)

    print(f"{encrypted} was decrypted to {decrypted} !")


if __name__ == "__main__":
    main()
