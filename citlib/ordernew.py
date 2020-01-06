import os
import sys

def get_letters(t):
    letters = []
    for i in range(t):
        letter = str(chr(i+65))
        letters.append(letter)
    return letters

def generate(t=3):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    file = dirname + "/../generated/" + "ordernew" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    letters = get_letters(t)
    content = "1{order("
    for letter in letters:
        content += letter + ","
    
    content = content[:-1] + ")}1 :- "
    for i in range(t-1):
        letter = str(chr(i+65))
        next_letter = str(chr(i+66))
        reaches_str = "reaches(" + letter + "," + next_letter +"),"
        content += reaches_str

    content = content[:-1] + "."
    # print(content)
    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate()
    