import json

def greet_user(name,city):
    print(f"Hello {name} from {city}!")

def cal_future_age (current_age, years):
    future_age = current_age + years
    print(f"In 5 years, you will be {future_age} years old.")
    

def save_to_file(name,age,city):
    data = {"name": name, "age": age, "city": city}
    with open("userdata.json", "w") as f:
        json.dump(data, f)

greet_user("Alice", "New York")
future_age = cal_future_age(30, 5)
save_to_file("Alice", 30, "New York")
