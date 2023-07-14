class PrettyRandom {
    constructor(config = {}) {
      // Define default values for configuration options
      // By default, the character set includes numbers and uppercase letters only
      const defaultValues = {
        useNumbers: true,
        useLowercase: false,
        useUppercase: true,
      };
  
      // Merge default values with provided configuration options
      const mergedConfig = { ...defaultValues, ...config };
      if (
        !mergedConfig.useNumbers &&
        !mergedConfig.useLowercase &&
        !mergedConfig.useUppercase
      ) {
        throw new Error("At least one of the options has to be set to true.");
      }
  
      // Available pattern generation rules
      this.rules = {
        repeat: this.repeat,
        alternate: this.alternate,
        pairs: this.pairs,
        outlier: this.outlier,
        zerofill: this.zerofill,
      };
  
      // Initialize character sets
      this.numbers = new Set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]);
      this.lowercase = new Set([
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
      ]);
      this.uppercase = new Set([
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
      ]);
  
      // Construct the character set based on configuration options
      this.characterSet = Array.from(
        new Set([
          ...(mergedConfig.useNumbers ? this.numbers : []),
          ...(mergedConfig.useLowercase ? this.lowercase : []),
          ...(mergedConfig.useUppercase ? this.uppercase : []),
        ])
      );
    }
  
    repeat(char1, char2, blocksize) {
      // Generates a repeated pattern of characters based on random selection between two characters (AAAA)
      const char = Math.random() < 0.5 ? char1 : char2;
      return char.repeat(blocksize);
    }
  
    alternate(char1, char2, blocksize) {
      // Generates an alternating pattern of characters (ABAB)
      let result = "";
      for (let i = 0; i < blocksize; i++) {
        result += i % 2 === 0 ? char1 : char2;
      }
      return result;
    }
  
    pairs(char1, char2, blocksize) {
      // Generates a pattern of repeating pairs of characters, switching between char1 and char2 (AABB AABB)
      const block = (char1.repeat(2) + char2.repeat(2)).repeat(blocksize / 4 + 1);
      return block.substring(0, blocksize);
    }
  
    outlier(char1, char2, blocksize) {
      // Generates a pattern with an outlier character (char2) randomly placed within char1 characters (AABA)
      const block = char1.repeat(blocksize).split("");
      block[Math.floor(Math.random() * blocksize)] = char2;
      return block.join("");
    }
  
    zerofill(char1, char2, blocksize) {
      // Generates a pattern with characters randomly chosen between char1 and char2, zero-filled to the blocksize (000A)
      const char = Math.random() < 0.5 ? char1 : char2;
      let block = char.repeat(blocksize).padStart(blocksize, "0");
      if (Math.random() < 0.5) {
        block = block.split("").reverse().join("");
      }
      return block;
    }
  
    randomRule() {
      // Randomly selects a rule function from the available rules
      const ruleNames = Object.keys(this.rules);
      const randomRuleName = ruleNames[Math.floor(Math.random() * ruleNames.length)];
      return this.rules[randomRuleName];
    }
  
    generate(blocksize, length) {
      // Generates a pretty random string based on the specified blocksize and length
      if (length <= 0 || blocksize <= 0) {
        throw new Error("Length and Blocksize must be larger than zero.");
      }
      if (length < blocksize) {
        throw new Error("Length must be larger or equal to the Blocksize.");
      }
  
      const numBlocks = Math.floor(length / blocksize);
      const rest = length % blocksize;
  
      // Generate complete blocks
      const blocks = Array.from({ length: numBlocks }, () =>
        this.randomRule()(
          this.characterSet[Math.floor(Math.random() * this.characterSet.length)],
          this.characterSet[Math.floor(Math.random() * this.characterSet.length)],
          blocksize
        )
      );
      let result = blocks.join(" ");
  
      // Fill up remaining characters with alternate pattern
      if (rest !== 0) {
        const restBlock = this.alternate(
          this.characterSet[Math.floor(Math.random() * this.characterSet.length)],
          this.characterSet[Math.floor(Math.random() * this.characterSet.length)],
          rest
        );
        result += " " + restBlock;
      }
  
      return result;
    }
  }
  
  // Example usage
  const prettyRandom = new PrettyRandom();
  
  // Generating a pretty random string with a block size of 4 and a length of 12
  const result = prettyRandom.generate(4, 22);
  console.log(result);
  
  // Configuring the character set to only include lowercase letters
  const prettyRandomWithLowerCase = new PrettyRandom({
    useNumbers: false,
    useLowercase: true,
    useUppercase: false,
  });
  
  // Generating a pretty random string with a block size of 3 and a length of 12
  const resultWithLowerCase = prettyRandomWithLowerCase.generate(3, 12);
  console.log(resultWithLowerCase);
  