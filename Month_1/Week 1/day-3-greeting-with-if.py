
name = input("What's your name? ").strip().title()
girlfriend = input("Do you have a girlfriend? (Leave blank if not) ").strip().title()
age_str = input("How old are you? ")
city = input("Which city are you grinding in? ").strip().title()
fav_food = input("What's your favorite Ghanaian dish? ").title()
age = int(age_str)  

print("\n=== HEYY YO ===")
print(f"Sup' {name.title()} from {city.title()}! 🇬🇭")

# Age-based message
if age < 20:
    print("Young king loading... the future is yours 🔥")
elif age < 30:
    print("Prime grinding years – don't waste them!")
elif age >= 30:
    print("Experienced boss mode – keep leading.")

# Food check example
if "jollof" in fav_food.lower():
    print("Jollof gang! That fuel keeps you unstoppable 🍲")
elif len(fav_food) > 10:
    print(f"{fav_food.title()} sounds fancy – respect the taste.")
else:
    print(f"{fav_food.title()} – simple and solid choice.")

# Girlfriend / motivation
if girlfriend.strip() == "":
    print("Solo mode activated – focus on self first 💪")
else:
    print(f"Shoutout to {girlfriend.title()} – build for her too ❤️")

if name == "rhymer":
    print("Boss vibes only, Rhymer! Keep grinding and shining.")
else:
    print(f"Yo {name}, do you know Rhymer is the boss here?")
print("Locked in. No retreat, no surrender.")