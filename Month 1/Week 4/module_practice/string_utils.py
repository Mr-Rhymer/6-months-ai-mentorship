

def reverse_string(s):
    """
    Reverses the input string.

    Args:
        s (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    return s[::-1]

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
    return s.title()