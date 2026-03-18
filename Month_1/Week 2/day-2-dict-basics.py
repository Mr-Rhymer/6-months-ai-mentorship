

student = {
    "name": "Clifford",
    "age": 22,
    "city": "Accra",
    "courses": ["Python", "AI"],
    "dream": "Billonaire",
     "mindset": "Make money",
     "fav_person": "Mom"
}

print(student["name"])
student["age"] = 23
student.setdefault("gpa", 3.5) 

print("Full student:", student)
print("Courses:", student["courses"])

for key, value in student.items():
    print(f"{key}: {value}")

print(f"I {student['name']} have a dream to become a {student['dream']} my daily motivation is to  "
      f"{student['mindset']} for my {student['fav_person']} to enjoy.")