#%%
from typing import List, Callable, Dict
import random
import unittest



class PrettyRandom():
    def __init__(self, **kwargs) -> None:
        """
        Initializes an instance of the PrettyRandom class and
        sets up the available rules and character sets.
        By default, the character set includes numbers and uppercase letters.
        
        Args:
            use_numbers: A boolean indicating whether to include numbers in the character set.
            use_lowercase: A boolean indicating whether to include lowercase letters in the character set.
            use_uppercase: A boolean indicating whether to include uppercase letters in the character set.
        
        Raises:
            AssertionError: If none of the options (numbers, lowercase, uppercase) are set to True.
        """

        self.rules: List[Callable] = [self.repeat, self.alternate, self.pairs, self.outlier, self.zerofill]
        self.numbers : List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.lowercase : List[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.uppercase : List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        # Define default values for keyword arguments
        # Default behavior: The character set includes numbers and uppercase letters only.
        default_values: Dict[str, bool] = {
            'use_numbers': True,
            'use_lowercase': False,
            'use_uppercase': True
        }

        # Merge default values with provided keyword arguments
        config = {**default_values, **kwargs}
        assert (config['use_numbers'] or config['use_lowercase'] or config['use_uppercase']) == True, "At least one of the options has to be set to True."

        # Use the config dictionary to set up the character set
        self.character_set = (
            self.numbers * config['use_numbers'] +
            self.lowercase * config['use_lowercase'] +
            self.uppercase * config['use_uppercase']
        )



    def repeat(self, char1: str, char2: str, blocksize: int) -> str:
        """
        Generates a repeated pattern of characters based on random selection between two characters (AAAA).

        Args:
            char1: The first character to be used in the pattern.
            char2: The second character to be used in the pattern.
            blocksize: The desired size of the block or pattern.

        Returns:
            A string representing the generated repeated pattern.
        """
        char: str = random.choice([char1, char2])
        return str(char) * blocksize
    

    def alternate(self, char1: str, char2: str, blocksize: int) -> str:
        """
        Generates an alternating pattern of characters (ABAB).

        Args:
            char1: The first character to be used in the pattern.
            char2: The second character to be used in the pattern.
            blocksize: The desired size of the block or pattern.

        Returns:
            A string representing the generated alternating pattern.
        """
        return "".join([str(char1) if i % 2 == 0 else str(char2) for i in range(blocksize)])
    

    def pairs(self, char1: str, char2: str, blocksize: int) -> str:
        """
        Generates a pattern of repeating pairs of characters, switching between char1 and char2 (AABB AABB).

        Args:
            char1: The first character to be used in the pattern.
            char2: The second character to be used in the pattern.
            blocksize: The desired size of the block or pattern.

        Returns:
            A string representing the generated pattern of repeating character pairs.
        """
        res = (str(char1) * 2 + str(char2) * 2) * (blocksize // 4 + 1)
        return res[:blocksize] 
    

    def outlier(self, char1: str, char2: str, blocksize: int) -> str:
        """
        Generates a pattern with an outlier character (char2) randomly placed within char1 characters (AABA).

        Args:
            char1: The character to be used as the majority in the pattern.
            char2: The character to be used as the outlier in the pattern.
            blocksize: The desired size of the block or pattern.

        Returns:
            A string representing the generated pattern with an outlier character.
        """
        collection = [str(char1)] * blocksize
        position = random.randint(0,blocksize - 1)
        collection[position] = str(char2)
        return "".join(collection)
    

    def zerofill(self, char1: str, char2: str, blocksize: int) -> str:
        """
        Generates a pattern with characters randomly chosen between char1 and char2, zero-filled to the blocksize (000A).

        Args:
            char1: The first character to be used in the pattern.
            char2: The second character to be used in the pattern.
            blocksize: The desired size of the block or pattern.

        Returns:
            A string representing the generated pattern with zero-filled characters.
        """
        char: str = random.choice([char1, char2])
        res = str(char).zfill(blocksize)
        return res if random.randint(0,10) % 2 == 0 else res[-1::-1]
    

    def random_rule(self) -> Callable:
        """
        Randomly selects a rule function from the available rules.
        """
        return random.choice(self.rules)


    def __call__(self, blocksize: int, length: int) -> str:
        """
        Generates a pretty random string based on the specified blocksize and length.

        Args:
            blocksize: The size of each block or pattern within the string.
            length: The desired length of the generated string.

        Returns:
            A string representing the generated pretty random string.

        Raises:
            AssertionError: If the length is smaller than the blocksize.
            AssertionError: If either the length or blocksize is zero.
        """
        assert length > 0 and blocksize > 0, f"Length and Blocksize must be larger than zero, but got Length ({length}) and Blocksize ({blocksize}))!"
        assert length >= blocksize, f"Length ({length}) must be larger or equal than the Blocksize ({blocksize})!"
        num_blocks = length // blocksize
        rest = length % blocksize

        # Generate complete blocks
        blocks = [self.random_rule()(random.choice(self.character_set), random.choice(self.character_set), blocksize) for _ in range(num_blocks)]
        res = " ".join(blocks)

        # Fill up remaining characters with alternate pattern
        if rest != 0: res += " " + self.alternate(random.choice(self.character_set), random.choice(self.character_set), rest)
        return str(res)
        


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.prettyrandom = PrettyRandom()


    def test_length(self) -> None:
        """
        Test case to ensure that the generated pretty random string has the correct length.

        Iterates over different lengths and block sizes, generating pretty random strings and removing spaces.
        Asserts that the length of each string matches the expected length.
        """
        for length in range(1, 100):
            for blocksize in range(1, length+1):
                x: str = self.prettyrandom(blocksize, length)
                x = x.replace(" ","") 
        self.assertEqual(len(x), length)


    def test_blocksize(self) -> None:
        """
        Test case to ensure that each block in the generated pretty random string has the correct block size.

        Iterates over different lengths and block sizes, generating pretty random strings and splitting them into blocks.
        Removes leading/trailing whitespaces and checks if each block has the expected block size.
        """
        for length in range(1, 100):
            for blocksize in range(1, length+1):
                x: str = self.prettyrandom(blocksize, length)
                x = x.strip() 
                blocks: List[str] = x.split(" ")
                if len(blocks) > 1 and len(blocks[-1]) != len(blocks[-2]): blocks = blocks[:-1]
                for b in blocks: self.assertEqual(len(b), blocksize)


if __name__ == "__main__":

    # -------- Example 1 --------
    prettyrandom = PrettyRandom()

    # Generating a pretty random string with a block size of 4 and a length of 22
    result = prettyrandom(blocksize=4, length=22)
    print(result)
    # Output: LWLW 6464 II88 QQ4Q 4S4S X0
    

    # -------- Example 2 --------
    # Configuring the character set to only include lowercase letters
    prettyrandom = PrettyRandom(use_numbers=False, use_lowercase=True, use_uppercase=False)

    # Generating a pretty random string with a block size of 3 and a length of 12
    result = prettyrandom(blocksize=3, length=12)
    print(result)
    # Output: rrh wvw rwr ono


    # -------- Example 3 --------
    prettyrandom = PrettyRandom()

    # Generating a pretty random string with block sizes ranging from 1 to 5 and a fixed length of 20
    for blocksize in range(1, 6):
        result = prettyrandom(blocksize=blocksize, length=20)
        print(f"Block Size: {blocksize}, Result: {result}")


    # -------- Example 4 --------
    # >>> python3 -m unittest prettyrandom.py
    # Output: Ran 2 tests in 0.085s OK


# %%
