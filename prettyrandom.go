package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

type PrettyRandom struct {
	rules        map[string]func(char1, char2 string, blocksize int) string
	characterSet []string
}

func NewPrettyRandom(config map[string]bool) (*PrettyRandom, error) {
	// Define default values for keyword arguments
	// By default, the character set includes numbers and uppercase letters only.
	defaultValues := map[string]bool{
		"use_numbers":   true,
		"use_lowercase": false,
		"use_uppercase": true,
	}

	// Merge default values with provided keyword arguments
	mergedConfig := make(map[string]bool)
	for k, v := range defaultValues {
		mergedConfig[k] = v
	}
	for k, v := range config {
		mergedConfig[k] = v
	}
	if !(mergedConfig["use_numbers"] || mergedConfig["use_lowercase"] || mergedConfig["use_uppercase"]) {
		return nil, fmt.Errorf("At least one of the options has to be set to true.")
	}

	// Initialize PrettyRandom instance
	pr := &PrettyRandom{
		rules: make(map[string]func(char1, char2 string, blocksize int) string),
	}

	// Available pattern generation rules
	pr.rules["repeat"] = pr.repeat
	pr.rules["alternate"] = pr.alternate
	pr.rules["pairs"] = pr.pairs
	pr.rules["outlier"] = pr.outlier
	pr.rules["zerofill"] = pr.zerofill

	// Construct the character set based on configuration options
	characterSet := make([]string, 0)
	if mergedConfig["use_numbers"] {
		characterSet = append(characterSet, []string{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}...)
	}
	if mergedConfig["use_lowercase"] {
		characterSet = append(characterSet, []string{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}...)
	}
	if mergedConfig["use_uppercase"] {
		characterSet = append(characterSet, []string{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}...)
	}

	if len(characterSet) == 0 {
		return nil, fmt.Errorf("At least one character set option must be enabled.")
	}
	pr.characterSet = characterSet

	return pr, nil
}

func (pr *PrettyRandom) repeat(char1, char2 string, blocksize int) string {
	// Generates a repeated pattern of characters based on random selection between two characters (AAAA)
	char := char1
	if rand.Float64() < 0.5 {
		char = char2
	}
	return strings.Repeat(char, blocksize)
}

func (pr *PrettyRandom) alternate(char1, char2 string, blocksize int) string {
	// Generates an alternating pattern of characters (ABAB)
	var builder strings.Builder
	for i := 0; i < blocksize; i++ {
		if i%2 == 0 {
			builder.WriteString(char1)
		} else {
			builder.WriteString(char2)
		}
	}
	return builder.String()
}

func (pr *PrettyRandom) pairs(char1, char2 string, blocksize int) string {
	// Generates a pattern of repeating pairs of characters, switching between char1 and char2 (AABB AABB)
	block := strings.Repeat(char1, 2) + strings.Repeat(char2, 2)
	repetitions := blocksize / 4
	return block[:blocksize] + strings.Repeat(block, repetitions)[:blocksize]
}

func (pr *PrettyRandom) outlier(char1, char2 string, blocksize int) string {
	// Generates a pattern with an outlier character (char2) randomly placed within char1 characters (AABA)
	block := strings.Repeat(char1, blocksize)
	randIndex := rand.Intn(blocksize)
	block = block[:randIndex] + char2 + block[randIndex+1:]
	return block
}

func (pr *PrettyRandom) zerofill(char1, char2 string, blocksize int) string {
	// Generates a pattern with characters randomly chosen between char1 and char2, zero-filled to the blocksize (000A)
	char := char1
	if rand.Float64() < 0.5 {
		char = char2
	}
	block := fmt.Sprintf("%0*d", blocksize, char)
	if rand.Intn(10)%2 == 0 {
		return block
	}
	reversed := make([]byte, 0, len(block))
	for i := len(block) - 1; i >= 0; i-- {
		reversed = append(reversed, block[i])
	}
	return string(reversed)
}

func (pr *PrettyRandom) randomRule() func(char1, char2 string, blocksize int) string {
	// Randomly selects a rule function from the available rules
	ruleNames := make([]string, 0, len(pr.rules))
	for ruleName := range pr.rules {
		ruleNames = append(ruleNames, ruleName)
	}
	randIndex := rand.Intn(len(ruleNames))
	randomRuleName := ruleNames[randIndex]
	return pr.rules[randomRuleName]
}

func (pr *PrettyRandom) Generate(blocksize, length int) (string, error) {
	// Generates a pretty random string based on the specified blocksize and length
	if length <= 0 || blocksize <= 0 {
		return "", fmt.Errorf("Length and Blocksize must be larger than zero.")
	}
	if length < blocksize {
		return "", fmt.Errorf("Length must be larger or equal to the Blocksize.")
	}

	numBlocks := length / blocksize
	rest := length % blocksize

	rand.Seed(time.Now().UnixNano())

	// Generate complete blocks
	blocks := make([]string, numBlocks)
	for i := 0; i < numBlocks; i++ {
		rule := pr.randomRule()
		char1 := pr.characterSet[rand.Intn(len(pr.characterSet))]
		char2 := pr.characterSet[rand.Intn(len(pr.characterSet))]
		blocks[i] = rule(char1, char2, blocksize)
	}
	output := strings.Join(blocks, " ")

	// Fill up remaining characters with alternate pattern
	if rest != 0 {
		char1 := pr.characterSet[rand.Intn(len(pr.characterSet))]
		char2 := pr.characterSet[rand.Intn(len(pr.characterSet))]
		output += " " + pr.alternate(char1, char2, rest)
	}

	return output, nil
}

func main() {
	// Example usage
	pr, err := NewPrettyRandom(map[string]bool{
		"use_numbers":    true,
		"use_lowercase":  false,
		"use_uppercase":  true,
	})
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Generating a pretty random string with a block size of 4 and a length of 22
	result, err := pr.Generate(4, 22)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println(result)
}
