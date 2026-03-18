# Day 2 – String methods & formatting practice

text = "  I love myself, anime and Tracy.  "

print("Original:", text)
print("Upper:", text.upper())
print("Lower:", text.lower())
print("Title:", text.title())
print("Stripped:", text.strip())          # removes leading/trailing spaces
print("Length:", len(text.strip()))

# Replace
replaced = text.replace("anime", "music")
print("Replaced:", replaced.strip())

# Find position
position = text.find("love")
print("Position of 'love':", position)   # -1 if not found

# Slicing [start:end]
name = "Clifford Rhymer"
first_name = name[:8]     # from start to index 7 (not including 7)
last_name = name[9:]      # from index 8 to end
print("First:", first_name)
print("Last:", last_name)