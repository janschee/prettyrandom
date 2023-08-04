# PrettyRandom: Aesthetic and User-Friendly Number Generator

## Generate Aesthetically Pleasing and User-Friendly Numbers or Identifiers.

Have you ever wanted to generate random numbers for a project while ensuring they look good? If so, you're not alone! Welcome to PrettyRandom, a number generator designed to enhance the user experience by providing visually appealing numbers for various purposes like generating user-IDs, ticket numbers, order numbers, card numbers, and more.

## Getting Started
To begin using PrettyRandom, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/janschee/prettyrandom.git
   ```

2. In your project, import the PrettyRandom number generator:

   ```python
   import prettyrandom
   prettyrandom = PrettyRandom()
   ```

3. Call the PrettyRandom generator and specify the desired length and block size of the output:

   ```python
   pretty_number = prettyrandom(blocksize=22, length=4)
   print(pretty_number)
   ```
   ``` 
   Output: VVVV A000 33YY 0003 4040 3C
   ```

## Customize the Output
By default, the PrettyRandom number generator uses numbers and capital letters for generating the output. However, you can customize this behavior by specifying the character sets to be used:

```python
prettyrandom = PrettyRandom(use_numbers=False, use_lowercase=True, use_uppercase=False)
```

## Test Cases
The repository includes two test cases, one for checking the length and another for checking the block size of the output. You can run these tests using Python's unittest module:

```shell
python3 -m unittest test.py
```

Enjoy generating aesthetically pleasing and user-friendly numbers with PrettyRandom! Feel free to contribute and make the generator even better!
