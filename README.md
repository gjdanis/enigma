# enigma
An Enigma machine simulator written in python. Example of use:

```
>>> r1 = Rotor("VEADTQRWUFZNLHYPXOGKJIMCSB", 1)
>>> r2 = Rotor("WNYPVJXTOAMQIZKSRFUHGCEDBL", 2)
>>> r3 = Rotor("DJYPKQNOZLMGIHFETRVCBXSWAU", 3)
>>> reflector = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
>>> machine = Machine([r1, r2, r3], reflector)
>>> machine.encipher("ATTACK AT DAWN")
'TFKZAX KV LCBG'
>>> machine.decipher('TFKZAX KV LCBG')
'ATTACK AT DAWN'
```
