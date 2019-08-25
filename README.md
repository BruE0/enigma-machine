# enigma-machine

https://en.wikipedia.org/wiki/Enigma_rotor_details

https://en.wikipedia.org/wiki/Enigma_machine

- [X] Rotor substitution cypher (duh).
- [X] Proper 3 rotors + reflector setup, i.e., will go right to left, then reflector, then left to right as per usual.
- [X] Ring offset and rotation, considering the **double-step** anomaly.
- [ ] Ring "settings". 
I'm still confused about this, it seems like an aditional offset that is added on top of the regular one.
Internet says it is an internal wire offset not accounted for in the rotor character display.


---

## Basic primer on enigma (I may get some detail wrong but bear with me, the general gist is rather simple):

Most enigma machines had 3 working rotors (right, middle, and left) and a reflector.
Each rotor is like a substitution cypher, and the reflector is the same, except that there is a 2 way mapping required.
That is, if the reflector maps "A" to "H", "H" must map to "A". That is not necessary for the normal rotors.

How a letter is "processed":


<image src="https://github.com/BruE0/enigma-machine/blob/media/enigma_rotors.png" width="300">

Each rotor has its position (offset). 
If the rotor is in A-position, then there's no offset and the mappings are normal.

If the rotor is in B-position, then there is an offset that needs to be accounted for. 
If the input signal was the letter "F", then you'd need to check
which letter "G" maps to to get your rotor output, since "G" is 1 offset of "F".


Each rotor has its turnover notch positions, which signal when the next rotor must move.

Kinda like AAZ becoming ABA, but rotors have notch positions in different letters. There's also the double-step issue.


### Important Detail:

When a key is pressed, the rotors rotate first, then the wirings process the input/output. So if the rotors were at positions
AAA, and you pressed a key, the output would follow the internal wirings of the AAB rotor positions.

