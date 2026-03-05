

ghana_cities = ["Accra", "Kumasi", "Takoradi", "Tamale"]
print("Cities:", ghana_cities)
print("First city:", ghana_cities[0])
print("Last city:", ghana_cities[-1])


ghana_cities[2] = "Cape Coast"
print("Updated:", ghana_cities)


ghana_cities.append("Ho")
print("Added Ho:", ghana_cities)
ghana_cities.extend(["Walewale","Damango","Wa"])
ghana_cities.insert(0,"Bolgatanga")
ghana_cities.remove("Cape Coast")
print("After modifications:", ghana_cities)

print("Number of cities:", len(ghana_cities))
if "Kumasi" in ghana_cities:
    print("Ashanti capital is in the list! 🇬🇭")


print("First 3:", ghana_cities[:3])
print("Last 2:", ghana_cities[-2:])