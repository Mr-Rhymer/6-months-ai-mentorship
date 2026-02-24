# Day 2 – Motivation Generator using strings & math

name = input("Your name: ").strip()
mood_str = input("Mood today 1-10: ").strip()
goal = input("One goal for today: ").strip()

mood = int(mood_str)   # assume valid for now

print("\n=== Daily Motivation for " + name.upper() + " ===")
print("Mood level:".ljust(15) + str(mood))
print("Goal:".ljust(15) + goal.title())

if mood >= 7:
    message = "You're on fire! Keep pushing."
else:
    message = "Low energy day – small wins matter most."

print("\nMessage: " + message)
print("In Ghana style: " + name.title() + ", you're a legend in the making! 🇬🇭")