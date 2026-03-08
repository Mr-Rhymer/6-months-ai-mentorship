import random
import json
import os

filename = "best_score.json"

# Load best score
if os.path.exists(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        best_score = data.get("best_score", float('inf'))
else:
    best_score = float('inf')

print("===Guessing Game ===")
if best_score != float('inf'):
    print(f"Current best score: {best_score} guesses")

while True:
    difficulty = input("Choose difficulty (easy/medium/hard): ").lower().strip()
    if difficulty == "easy":
        max_num = 50
        max_guesses = 10
    elif difficulty == "hard":
        max_num = 200
        max_guesses = 7
    else:
        max_num = 100
        max_guesses = 8

    secret = random.randint(1, max_num)
    guesses = 0
    wrong_guesses = 0

    print(f"Guess the number between 1 and {max_num} ({max_guesses} attempts)")

    while guesses < max_guesses:
        try:
            guess = int(input(f"Attempt {guesses+1}/{max_guesses}: "))
            guesses += 1

            if guess == secret:
                print(f"You got it in {guesses} guesses!")
                if guesses < best_score:
                    best_score = guesses
                    print(f"New best score: {best_score} guesses!")
                break
            elif guess < secret:
                print("Too low!")
                wrong_guesses += 1
            else:
                print("Too high!")
                wrong_guesses += 1
            
            # Offer hint after 3 wrong guesses
            if wrong_guesses == 3:
                hint = "even" if secret % 2 == 0 else "odd"
                print(f"Hint: The number is {hint}.")
        except:
            print("Enter a valid number!")

    if guesses == max_guesses:
        print(f"Game over! The number was {secret}")

    play_again = input("Play again? (yes/no): ").lower().strip()
    if play_again != "yes":
        print("See you next time!")
        break

# Save best score
with open(filename, "w") as f:
    json.dump({"best_score": best_score}, f, indent=2)