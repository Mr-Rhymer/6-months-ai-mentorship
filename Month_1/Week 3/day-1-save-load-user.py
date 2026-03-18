import json

    
def save_user_data():
    try:
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        fav_food = input("Enter your favorite food: ")
    except ValueError:
        print("Invalid input! Please enter the correct data types.")
        
    data = {
        "name": name,
        "age": age,
        "city": city,
        "favorite_food": fav_food
    }
    with open("user_data.json", "w") as f:
        json.dump(data, f)

def load_user_data():
    try:
        with open("user_data.json", "r") as f:
            data = json.load(f)
            print("\nLoaded User Data:")
            print(f"Name: {data['name']}")
            print(f"Age: {data['age']}")
            print(f"City: {data['city']}")
            print(f"Favorite Food: {data['favorite_food']}")
    except FileNotFoundError:
        print("No saved user data found. Please save your data first.")


def main():
    while True:
      action = input("Do you want to save (s) user data, load (l) user data or quit (q)? ").strip().lower()
      if action == 's':
          save_user_data()
      elif action == 'l':
          load_user_data()
      elif action == 'q':
          print("Exiting the program. Goodbye!")
          break
      else:
          print("Invalid action. Please enter 's' to save or 'l' to load user data.")


main()
