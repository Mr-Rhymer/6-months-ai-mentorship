

def reverse_string(s):
    """
    Reverses the input string.

    Args:
        s (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    reversed_str = ""
    for char in range(len(s) - 1, -1, -1):
        reversed_str += s[char]
    return reversed_str

def count_vowels(s):
    """
    Counts the number of vowels in the input string.

    Args:
        s (str): The string to count vowels in.

    Returns:
        int: The number of vowels in the string.
    """
    
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

def capitalize_words(s):
    """
    Capitalizes the first letter of each word in the input string.

    Args:
        s (str): The string to capitalize.

    Returns:
        str: The string with each word capitalized.
    """
    words = s.split()
    capitalized_words = []
    for word in words:
        if word:  # Check if the word is not empty
            capitalized_word = word[0].upper() + word[1:].lower()
        else:
            capitalized_word = word  # Handle empty words (rare, but safe)
        capitalized_words.append(capitalized_word)
    return ' '.join(capitalized_words)


if __name__ == "__main__":
    print("Testing string_utils module directly...")
    test_string = "hello world"
    print(f"Original: {test_string}")
    print(f"Reversed: {reverse_string(test_string)}")
    print(f"Vowels: {count_vowels(test_string)}")
    print(f"Capitalized: {capitalize_words(test_string)}")