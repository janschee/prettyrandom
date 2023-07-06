#%%
from typing import Any, List, Dict, Callable
import random
import unittest



class PrettyRandom():
    def __init__(self) -> None:
        self.rules: List[Callable] = [self.repeat, self.alternate, self.pairs, self.outlier, self.zerofill]
        self.numbers : List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.letters : List[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.capitals : List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def repeat(self, char1: str, char2: str, blocksize: int) -> str:
        char: str = random.choice([char1, char2])
        return str(char) * blocksize
    
    def alternate(self, char1: str, char2: str, blocksize: int) -> str:
        res = ""
        for i in range(blocksize):
            res += str(char1) if i % 2 == 0 else str(char2)
        return res
    
    def pairs(self, char1: str, char2: str, blocksize: int) -> str:
        res = (str(char1) * 2 + str(char2) * 2) * (blocksize // 4 + 1)
        res = res[:blocksize] 
        return res
    
    def outlier(self, char1: str, char2: str, blocksize: int) -> str:
        collection = [str(char1)] * blocksize
        position = random.randint(0,blocksize - 1)
        collection[position] = str(char2)
        res = ""
        for c in collection:
            res += c
        return res
    
    def zerofill(self, char1: str, char2: str, blocksize: int) -> str:
        char: str = random.choice([char1, char2])
        res = str(char).zfill(blocksize)
        return res if random.randint(0,10) % 2 == 0 else res [-1::-1]
    
    def random_rule(self) -> Callable:
        return random.choice(self.rules)
    
    def random_char(self, numbers: bool, letters: bool, capitals: bool) -> str:
        pool: List[str] =[]
        if numbers: pool += self.numbers
        if letters: pool += self.letters
        if capitals: pool += self.capitals
        return random.choice(pool)

    def __call__(self, blocksize: int, length: int) -> str:
        assert length >= blocksize, f"Length ({length}) must be larger or equal than the block size ({blocksize})!"
        num_blocks = length // blocksize
        rest = length % blocksize
        res = ""
        for _ in range(num_blocks):
            randchar1 = self.random_char(numbers=True, letters=False, capitals=True)
            randchar2 = self.random_char(numbers=True, letters=False, capitals=True)
            rule = self.random_rule()
            res += rule(randchar1, randchar2, blocksize)
            res += " "

        if rest != 0:
            randchar1 = self.random_char(numbers=True, letters=False, capitals=True)
            randchar2 = self.random_char(numbers=True, letters=False, capitals=True)
            res += self.alternate(randchar1, randchar2, rest)
        return str(res)
        

class Test(unittest.TestCase):
    def test_length(self) -> None:
        prettyrandom = PrettyRandom()
        for length in range(1, 100):
            for blocksize in range(1, length+1):
                x: str = prettyrandom(blocksize, length)
                x = x.replace(" ","") #remove spaces
        self.assertEqual(len(x), length)

    def test_blocksize(self) -> None:
        prettyrandom = PrettyRandom()
        for length in range(1, 100):
            for blocksize in range(1, length+1):
                x: str = prettyrandom(blocksize, length)
                x = x.strip() #remove whitespaces
                blocks: List[str] = x.split(" ")
                if len(blocks) > 1 and len(blocks[-1]) != len(blocks[-2]): blocks = blocks[:-1]
                print(blocks)
                for b in blocks:
                    self.assertEqual(len(b), blocksize)


if __name__ == "__main__":
    prettyrandom = PrettyRandom()
    blocksize = 4
    length = 22
    print(prettyrandom(blocksize, length))


# %%
