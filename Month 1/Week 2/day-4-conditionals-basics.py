
age = int(input("Your age: "))
mood = int(input("Mood 1–10: "))
has_girlfriend = input("Have girlfriend? (yes/no): ").lower().strip()
city = input("From which city?").strip().title()
goal = input("What is your main goal?")
country = input("Which country?").title()

if goal != '':
    print(f"Do well in {goal}")
else:
    print("You are not serious in life!!!")

if country == "Ghana":
    if city == "Kumasi":
        print("The pride of Ashanti")
    else:
        print("A proud Ghanaian")
else:
    print("I hpoe your country is peaceful like Ghana.")

if age < 18:
    print("Underage – focus on school first!")
elif age >= 18 and age < 25:
    print("Young adult zone – grind hard now!")
else:
    print("Experienced – lead the way.")


if mood >= 7:
    if has_girlfriend =="yes":
        print("High mood + relationship = unstoppable combo")
    else:
        print("High mood solo mode – dangerous energy ")
elif mood <= 4:
    print("Low mood detected – small wins only today.")
else:
    print("Balanced mood – keep steady.")


if age >= 21 and mood >= 8 or has_girlfriend.lower() == "yes":
    print("VIP status tonight – legend behavior")