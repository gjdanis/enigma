import string

ALPHABET = string.ascii_uppercase

class Rotor:
    TURN_FREQUENCY = len(ALPHABET)
    
    """
    Models a 'rotor' in an Enigma machine

    Rotor("BCDA", 1) means that A->B, B->C, C->D, D->A and the rotor has been
    rotated once from ABCD (the clear text character 'B' is facing the user)

    Args:
        mappings (string) encipherings for the machine's alphabet.
        offset (int) the starting position of the rotor
    """

    def __init__(self, mappings, offset=0):
        self.initial_offset = offset
        self.reset()
        self.forward_mappings = dict(zip(self.alphabet, mappings))
        self.reverse_mappings = dict(zip(mappings, self.alphabet))

    def reset(self):
        """
        Helper to re-initialize the rotor to its initial configuration

        Returns: void
        """
        self.rotations = 0
        self.alphabet = ALPHABET
        self.rotate(self.initial_offset)

    def rotate(self, num_rotations=1):
        """
        Rotates the rotor the given number of characters

        Args: num_rotations (int)

        Returns: int
        """
        self.alphabet = self.alphabet[num_rotations:] + self.alphabet[:num_rotations]
        self.rotations += num_rotations
        return self.rotations

    def encipher(self, character):
        """
        Gets the cipher text mapping of a plain text character

        Args: character (char)

        Returns: char
        """
        return self.forward_mappings[character]

    def decipher(self, character):
        """
        Gets the plain text mapping of a cipher text character

        Args: character (char)

        Returns: char
        """
        return self.reverse_mappings[character]

    def translate(self, contact_index, right=True):
        """
        Translate contact with the rotor to the right or left. Return
        the resulting point of contact

        Args:
            contact_index (int) point of contact with the rotor
            right (bool) direction to move the contact over the rotor

        Returns: int
        """
        x = self.alphabet[contact_index]
        x = self.encipher(x) if right else self.decipher(x)
        return self.alphabet.index(x)

class Reflector:
    """
    Models a 'reflector' in the Enigma machine. Reflector("CDAB")
    means that A->C, C->A, D->B, B->D

    Args: mappings (string) bijective map representing the reflection
          of a character
    """

    def __init__(self, mappings):
        self.mappings = dict(zip(ALPHABET, mappings))

        for x, y in self.mappings.items():
            if x != self.mappings[y]:
                raise ValueError('Mapping for {0} and {1} is invalid'.format(x, y))

    def translate(self, contact_index):
        """
        Translate contact with the reflector. Return
        the resulting point of contact

        Args: contact_index (int) point of contact with the rotor

        Returns: int
        """
        x = self.mappings[ALPHABET[contact_index]]
        return ALPHABET.index(x)

class Machine:
    """
    Models an Enigma machine (https://en.wikipedia.org/wiki/Enigma_machine)

    Args:
        rotors (list[Rotor]) the configured rotors
        reflector (Reflector) to use
    """

    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def reset(self):
        """
        Resets the machine's rotors

        Returns: void
        """
        for rotor in self.rotors:
            rotor.reset()

    def encipher(self, text):
        """
        Encipher the given input

        Args: text (string)

        Returns: string
        """
        return ''.join(self.encipher_character(x) for x in text)

    def decipher(self, text):
        """
        Deccipher the given input

        Args: text (string)

        Returns: string
        """
        self.reset()
        return self.encipher(text)

    def encipher_character(self, x):
        """
        Runs a character through the machine's cipher algorithm

        1. If x is not in the known character set, don't encipher it
        2. For each of the rotors, determine the character in contact with x.
           Determine the enciphering for that character, and use it as the next
           letter to pass through to the next rotor in the machine's sequence
        3. Once we get to the reflector, get the reflection and repeat the above
           in reverse
        4. Rotate the first rotor, and check if any other rotor should be rotated
        5. Return the character at the terminating contact position as the input
           character's enciphering

        Args: x (char) the character to encipher

        Returns: char
        """

        x = x.upper()
        if x not in ALPHABET:
            return x

        contact_index = ALPHABET.index(x)
        for rotor in self.rotors:
            contact_index = rotor.translate(contact_index)

        contact_index = self.reflector.translate(contact_index)

        for rotor in reversed(self.rotors):
            contact_index = rotor.translate(contact_index, False)

        for rotor in self.rotors:
            if rotor.rotate() % Rotor.TURN_FREQUENCY != 0:
                break

        return ALPHABET[contact_index]

if __name__ == "__main__":
    pass
