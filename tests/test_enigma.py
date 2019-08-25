#!/usr/bin/env python3

"""
    test.py
        testing enigma
"""

from enigma import Rotor, Reflector, Enigma
import unittest

class EnigmaTest(unittest.TestCase):

    def setUp(self):
        self.enigma1_rotorI = Rotor(list("ekmflgdqvzntowyhxuspaibrcj"), turnover_notch=["q"])
        self.enigma1_rotorII = Rotor(list("ajdksiruxblhwtmcqgznpyfvoe"), turnover_notch=["e"])
        self.enigma1_rotorIII = Rotor(list("bdfhjlcprtxvznyeiwgakmusqo"), turnover_notch=["v"])
        self.enigma1_wide_B_reflector = Reflector(list("yruhqsldpxngokmiebfzcwvjat"))

        self.my_enigma = Enigma(
            self.enigma1_wide_B_reflector,
            self.enigma1_rotorI,
            self.enigma1_rotorII,
            self.enigma1_rotorIII,
            double_step=True,
        )


    def test_positions_getset(self):
        """ Test set/get rotor positions """
        for char1 in range(ord("a"), ord("z")+1):
            char1 = chr(char1)
            for char2 in range(ord("a"), ord("z")+1):
                char2 = chr(char2)
                for char3 in range(ord("a"), ord("z")+1):
                    char3 = chr(char3)
                    self.my_enigma.set_position(char1+char2+char3)
                    self.assertEqual(self.my_enigma.left_rotor.current_position(), char1)
                    self.assertEqual(self.my_enigma.mid_rotor.current_position(), char2)
                    self.assertEqual(self.my_enigma.right_rotor.current_position(), char3)



    def test_encryption_decryption(self):
        """ Test long_text.txt for mistakes in encryption/decryption """
        with open("tests/test_lowercase.txt", "r") as f:
            data = f.read()

        self.my_enigma.set_position("AAA")
        encrypted = self.my_enigma.encrypt(data)
        self.my_enigma.set_position("AAA")
        decrypted = self.my_enigma.encrypt(encrypted)

        self.assertEqual(decrypted, data) 
