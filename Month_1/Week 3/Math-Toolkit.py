def calc_area():
    shape = input("Enter the shape (c)ircle, (r)ectangle, (t)riangle): ").lower()
    if shape == "c":
        radius = float(input("Enter the radius of the circle: "))
        print("Area of the circle is:", 3.14 * radius ** 2)
        return 3.14 * radius ** 2
    elif shape == "r":
        length = float(input("Enter the length of the rectangle: "))
        width = float(input("Enter the width of the rectangle: "))
        print("Area of the rectangle is:", length * width)
        return length * width
    elif shape == "t":
        base = float(input("Enter the base of the triangle: "))
        height = float(input("Enter the height of the triangle: "))
        print("Area of the triangle is:", 0.5 * base * height)  
        return 0.5 * base * height
    else:
        raise ValueError("Unsupported shape")
    
def temp_conversion():
    from_unit = input("Convert from (C)elsius or (F)ahrenheit: ").upper()
    to_unit = input("Convert to (C)elsius or (F)ahrenheit: ").upper()
    temp = float(input("Enter the temperature to convert: "))
    if from_unit == "C" and to_unit == "F":
        print(f"Temperature in Fahrenheit is: {(temp * 9/5) + 32:.2f}")
        return (temp * 9/5) + 32
    elif from_unit == "F" and to_unit == "C":
        print(f"Temperature in Celsius is: {(temp - 32) * 5/9:.2f}")
        return (temp - 32) * 5/9
    else:
        raise ValueError("Unsupported temperature conversion")
    
def bmi_calculator():
    weight = float(input("Enter weight in kilograms: "))
    height = float(input("Enter height in meters: "))
    print("BMI is:", weight / (height ** 2))
    return weight / (height ** 2)

def discount_calculator():
    price = float(input("Enter the original price: "))
    discount_percentage = float(input("Enter the discount percentage: "))   
    print("Discounted price is:", price * (1 - discount_percentage / 100))
    return price * (1 - discount_percentage / 100)

def tip_splitter():
    total_bill = float(input("Enter the total bill amount: "))
    tip_percentage = float(input("Enter the tip percentage: "))
    num_people = int(input("Enter the number of people: "))
    total_with_tip = total_bill * (1 + tip_percentage / 100)
    print("Each person should pay:", total_with_tip / num_people)
    return total_with_tip / num_people

def main():
    while True:
      action = input("Choose an action: (a)rea, (t)emp_conversion, (b)mi, (d)iscount, (tip)_splitter or (q)uit: ")
      if action == "a":
        calc_area()
      elif action == "t": 
        temp_conversion()
      elif action == "b":
        bmi_calculator()
      elif action == "d":
        discount_calculator()
      elif action == "tip":
        tip_splitter()
      elif action == "q":
        print("Exiting the program.")
        break
      else:
        print("Invalid action")



main()