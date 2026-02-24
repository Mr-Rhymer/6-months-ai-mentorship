# Day 1 - Personalized Greeting + Basic Math
# Clifford - 6-Month AI Mentorship

name = input("What is your full name? ").strip()
age_str = input("How old are you? ").strip()
city = input("Which city in Ghana? ").strip()

# Convert age to number (we'll handle errors later)
age = int(age_str)  # this will crash if not number — that's ok for now

print("\n=== Welcome to the Grind ===")
print(f"Big up {name.upper()} from {city.title()}!")
print(f"You're {age} years young → in {5} years you'll be {age + 5}")
print("Locked in for AI automation.\n No retreat, no surrender.\n")