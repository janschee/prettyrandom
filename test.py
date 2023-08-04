import unittest
from typing import List
import prettyrandom

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.prettyrandom_generator = prettyrandom.PrettyRandom()


    def test_length(self) -> None:
        """
        Test case to ensure that the generated pretty random string has the correct length.

        Iterates over different lengths and block sizes, generating pretty random strings and removing spaces.
        Asserts that the length of each string matches the expected length.
        """
        for length in range(1, 100):
            for blocksize in range(1, length+1):
                x: str = self.prettyrandom_generator(blocksize, length)
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
                x: str = self.prettyrandom_generator(blocksize, length)
                x = x.strip() 
                blocks: List[str] = x.split(" ")
                if len(blocks) > 1 and len(blocks[-1]) != len(blocks[-2]): blocks = blocks[:-1]
                for b in blocks: self.assertEqual(len(b), blocksize)
