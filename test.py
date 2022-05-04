import re
import os

for i in range(99):
	word_lower = chr(i % 26 + 97) + chr(i % 26 + 97 + 1)
	print(word_lower)
	if re.match(r"^[a-d1-1].*",word_lower):
		print("SAVE 1")
	elif re.match(r"^[e-k2-3].*",word_lower):
		print("SAVE 2")
	elif re.match(r"^[l-q4-7].*",word_lower):
		print("SAVE 3")
	elif re.match(r"^[r-z8-9].*",word_lower):
		print("SAVE 4")

path = "data/DEV/"
print(os.listdir(path))