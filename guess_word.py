import random
# Word list
words = [
    "APPLE", "ANT", "AIR", "BALL", "BOOK", "BIRD",
    "CAT", "CAR", "CLOUD", "DOG", "DOOR", "DANCE",
    "EGG", "EARTH", "EYE", "FISH", "FLOWER", "FIRE",
    "GOAT", "GRASS", "GOLD", "HOUSE", "HORSE", "HAT",
    "ICE", "IRON", "ISLAND", "JUICE", "JUMP", "JEWEL",
    "KING", "KITE", "KEY", "LION", "LEAF", "LIGHT",
    "MOON", "MOUNTAIN", "MILK", "NEST", "NIGHT", "NOSE",
    "ORANGE", "OCEAN", "OWL", "PEN", "PLANT", "PARK",
    "QUEEN", "QUILT", "QUICK", "RABBIT", "RIVER", "RAIN",
    "SUN", "STAR", "SAND", "TREE", "TIGER", "TABLE",
    "UMBRELLA", "UNCLE", "UNIFORM", "VAN", "VOICE", "VALLEY",
    "WATER", "WIND", "WOLF", "XBOX", "XRAY", "XENON",
    "YELLOW", "YAHOO", "YEAR", "ZEBRA", "ZOO", "ZERO"
]
# Random word selection
word = random.choice(words)
# Check guess
def check_guess(word, user_word):
    result = ["R"] * len(word)  # Default to "R"
    word_counts = {}  # Count letters in target word
    # Mark correct letters ("G")
    for i in range(len(word)):
        if word[i] == user_word[i]:
            result[i] = "G"
        else:
            word_counts[word[i]] = word_counts.get(word[i], 0) + 1
    # Mark misplaced letters ("Y")
    for i in range(len(word)):
        if result[i] == "R" and user_word[i] in word_counts and word_counts[user_word[i]] > 0:
            result[i] = "Y"
            word_counts[user_word[i]] -= 1
    return "".join(result)
# Display word with "_"
hide_word = "_ " * len(word)
print(hide_word)
# Get user input (8 attempts)
for attempt in range(8):
    user_word = input(f"Attempt {attempt + 1}/8 - Enter your guess: ").upper()
    # Validate input length
    if len(user_word) != len(word):
        print("Invalid guess")
        continue
    result = check_guess(word, user_word)
    if result == "G" * len(word):
        print("You win!")
        break
    else:
        print(result)
else:
    print(f"You lose... The correct word was: {word}")
