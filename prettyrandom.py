from typing import List, Callable, Dict
import random


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

        # Define default values for keyword arguments
        # By default, the character set includes numbers and uppercase letters only.
        default_values: Dict[str, bool] = {
            'use_numbers': True,
            'use_lowercase': False,
            'use_uppercase': True
        }

        # Merge default values with provided keyword arguments
        config = {**default_values, **kwargs}
        if not (config['use_numbers'] or config['use_lowercase'] or config['use_uppercase']):
            raise ValueError("At least one of the options has to be set to True.")

        # Available pattern generation rules
        self.rules: Dict[str, Callable] = {
            'repeat': self.repeat,
            'alternate': self.alternate,
            'pairs': self.pairs,
            'outlier': self.outlier,
            'zerofill': self.zerofill
        }

        # Initialize sets
        self.numbers: set[str] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        self.lowercase: set[str] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
        self.uppercase: set[str] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}

        # Use set operations to construct the character set
        self.character_set = list(
            (self.numbers if config['use_numbers'] else set()) |
            (self.lowercase if config['use_lowercase'] else set()) |
            (self.uppercase if config['use_uppercase'] else set())
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
        block: str = (str(char1) * 2 + str(char2) * 2) * (blocksize // 4 + 1)
        return block[:blocksize] 
    

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
        block: List[str] = [str(char1)] * blocksize
        block[random.randint(0, blocksize-1)] = str(char2)
        return "".join(block)
    

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
        block: str = str(char).zfill(blocksize)
        return block if random.randint(0,10) % 2 == 0 else block[-1::-1]
    

    def random_rule(self) -> Callable:
        """
        Randomly selects a rule function from the available rules.
        """
        return self.rules[random.choice(list(self.rules.keys()))]


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

        if length <= 0 or blocksize <= 0:
            raise ValueError("Length and Blocksize must be larger than zero.")
        if length < blocksize:
            raise ValueError("Length must be larger or equal to the Blocksize.")

        num_blocks: int = length // blocksize
        rest: int = length % blocksize

        # Generate complete blocks
        blocks: List[str] = [self.random_rule()(random.choice(self.character_set), random.choice(self.character_set), blocksize) for _ in range(num_blocks)]
        output: str = " ".join(blocks)

        # Fill up remaining characters with alternate pattern
        if rest != 0: output += " " + self.alternate(random.choice(self.character_set), random.choice(self.character_set), rest)
        return str(output)
        

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
    # >>> python3 -m unittest test.py
    # Output: Ran 2 tests in 0.085s OK

