import string_utils as su

test_string = "hello world"
print(f"Original: {test_string}")
print(f"Reversed: {su.reverse_string(test_string)}")
print(f"Vowels: {su.count_vowels(test_string)}")
print(f"Capitalized: {su.capitalize_words(test_string)}")

import string_utils
othr_string = "python programming"
print(f"\nOriginal: {othr_string}")
print(f"Reversed: {string_utils.reverse_string(othr_string)}")
print(f"Vowels: {string_utils.count_vowels(othr_string)}")
print(f"Capitalized: {string_utils.capitalize_words(othr_string)}")

from string_utils import capitalize_words, reverse_string, count_vowels
another_string = "importing functions"
print(f"\nOriginal: {another_string}")
print(f"Reversed: {reverse_string(another_string)}")
print(f"Vowels: {count_vowels(another_string)}")
print(f"Capitalized: {capitalize_words(another_string)}")