wiring_r1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
wiring_r2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
wiring_r3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
wiring_re = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
wiring_pl = {}


def charToNum(x):
    return ord(x) - 65

def numToChar(x):
    return chr(x + 65)

class Enigma():
    def __init__(self, left_r, middle_r, right_r, left_pos, middle_pos, right_pos, plugboard):
        self.wiring_left = left_r
        self.wiring_middle = middle_r
        self.wiring_right = right_r
        self.left_pos = left_pos
        self.middle_pos = middle_pos
        self.right_pos = right_pos
        self.wiring_pl = plugboard

    def mapRightToLeft(self, wiring, top_letter, input_pos):
        offset = top_letter
        out_contact = wiring[(input_pos + offset) % 26] 
        return (charToNum(out_contact) - offset) % 26

    def mapLeftToRight(self, wiring, top_letter, input_pos):
        offset = top_letter
        out_contact = wiring.index(numToChar((input_pos + offset) % 26))
        return (out_contact - offset) % 26
        
    def reflector(self, wiring, input_pos):
        return charToNum(wiring[input_pos])

    def plugboard(self, wiring, input_pos):
        return wiring.get(input_pos, input_pos) # Uses a dictionary 
        
    def encode(self, char):
        
        # Stepping
        self.right_pos = (self.right_pos + 1) % 26
        if self.right_pos == 22:
            self.middle_pos = (self.middle_pos + 1) % 26
        elif self.middle_pos == 4:
            self.left_pos = (self.left_pos + 1) % 26
            self.middle_pos = (self.middle_pos + 1) % 26

        position = charToNum(char)
        # Plugboard
        position = self.plugboard(self.wiring_pl, position)
        # Rotors right to left
        right_forward = self.mapRightToLeft(self.wiring_right, self.right_pos, position)
        middle_forward = self.mapRightToLeft(self.wiring_middle, self.middle_pos, right_forward)
        left_forward = self.mapRightToLeft(self.wiring_left, self.left_pos, middle_forward)
        # Reflection
        reflection = self.reflector(wiring_re, left_forward)
        # Rotors left to right
        left_backward = self.mapLeftToRight(self.wiring_left, self.left_pos, reflection)
        middle_backward = self.mapLeftToRight(self.wiring_middle, self.middle_pos, left_backward)
        right_backward = self.mapLeftToRight(self.wiring_right, self.right_pos, middle_backward)
        # Plugboard
        output = self.plugboard(self.wiring_pl, right_backward)

        return numToChar(output)
    
plugboard = {}
n = int(input("How many plugboard switches do you want to make?\n"))
for i in range(1, n+1):
    print(f"Switch {i}")
    l1 = input("Letter 1: ")
    l2 = input("Letter 2: ")
    plugboard[charToNum(l1)] = charToNum(l2)
    plugboard[charToNum(l2)] = charToNum(l1)
    
top = input("What are the top letters?\n")
    
machine = Enigma(wiring_r1, wiring_r2, wiring_r3, charToNum(top[0]), charToNum(top[1]), charToNum(top[2]), plugboard)


message = input("What do you want to encode?\n")
ciphertext = ""

for letter in message:
    if letter == " ":
        ciphertext += letter
    else:
        ciphertext += machine.encode(letter)
        
print(ciphertext)
        
