grade_tracker = {}

def add_student(name):
    if name in grade_tracker:
        print(f"{name} is already in the grade tracker.")
    else:
        try:
            grade_tracker[name] = []
            print(f"{name} has been added to the grade tracker.")
        except Exception as e:
            print("Enter a valid name.")
            

def add_grade(name, grade):
    if name not in grade_tracker:
        print(f"{name} is not in the grade tracker. Please add the student first.")
        return
    try:
        if isinstance(grade, list):
            # extend with every element in the list
            grade_tracker[name].extend(grade)
            print(f"Added grades {grade} for {name}.")
        else:
            grade_tracker[name].append(grade)
            print(f"Added grade {grade} for {name}.")
    except Exception as e:
        print(f"An error occurred while adding grade for {name}: {e}")


def calculate_average(name):
    if name in grade_tracker:
        try:
         grades = grade_tracker[name]
         if grades:
            average = sum(grades) / len(grades)
            print(f"The average grade for {name} is {average:.2f}.")
         else:
            print(f"{name} has no grades to calculate an average.")
        except Exception as e:
         print(f"An error occurred while calculating average for {name}: {e}")
    else:
        print(f"{name} is not in the grade tracker. Please add the student first.")


def main():
    while True:
        print("\nStudent Grade Tracker")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. Calculate Average")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter the student's name: ")
            add_student(name)
        elif choice == '2':
         name = input("Enter the student's name: ")
         text = input("Enter the grades (comma-separated): ")
         try:
          grades = [float(x.strip()) for x in text.split(',') if x.strip()]
          add_grade(name, grades)
         except ValueError:
          print("Please enter valid numbers separated by commas.")
        elif choice == '3':
            name = input("Enter the student's name: ")
            calculate_average(name)
        elif choice == '4':
            print("Exiting the grade tracker.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":    main()
