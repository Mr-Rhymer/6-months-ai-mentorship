import random
k=1
while k <= 5:
    print("Your 5 lucky numbers are:")
    for i in range(1, 6):
      num = random.randint(1, 100)
      print(f"{i}. {num}")
    k += 2