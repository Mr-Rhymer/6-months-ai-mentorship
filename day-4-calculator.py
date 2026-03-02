
print("=== Simple Ghana Grind Calculator ===")
print("Enter two numbers and operation (+ - * ** % /)")
print("Type 'q' to quit anytime\n")

while True:
    num1_input = input("First number (or 'q' to quit): ").strip()

    if num1_input.lower() == 'q' or num1_input.lower() == 'quit':
        print("Calculator closed. Good grind today!")
        break

    num2_input = input("Second number: ").strip()
    operation = input("Operation (+ - * /): ").strip()

   
    try:
        num1 = float(num1_input)
        num2 = float(num2_input)
    except ValueError:
        print("Invalid number(s) – please enter numbers only.\n")
        continue

   
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '**':
        result = num1 ** num2
    elif operation== '%':
        if num2 == 0:
            print("Cannot modulo by zero! Try again.\n")
            continue
        result = num1 % num2
    elif operation == '/':
        if num2 == 0:
            print("Cannot divide by zero! Try again.\n")
            continue
        result = num1 / num2
    else:
        print("Invalid operation – use + - * / only.\n")
        continue

    
    print(f"\n{num1} {operation} {num2} = {result:.2f}")
    if result > 100:
        print("Big number!")
    elif result < 0:
        print("Negative vibes... ")
    print("-" * 40 + "\n")
