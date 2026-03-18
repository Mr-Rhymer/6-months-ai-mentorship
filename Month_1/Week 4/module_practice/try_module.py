from string_utils import reverse_string, count_vowels, capitalize_words


print("Welcome to the String Utilities Program!")
print("Please choose an option:")
print("1. Reverse a string")
print("2. Count vowels in a string")
print("3. Capitalize words in a string")
choice = input("Enter your choice (1, 2, or 3): " )
s = input("Enter a string to process1: ")
if choice == '1':
   
    result = reverse_string(s)
    print(f"Reversed string: {result}")
elif choice == '2':
    
    result = count_vowels(s )
    print(f"Number of vowels: {result}")
elif choice == '3':
    
    result = capitalize_words(s)
    print(f"Capitalized string: {result}")
else:
    print("Invalid choice. Please enter 1, 2, or 3.")

