import os
import sys

def get_letters(t):
    letters = []
    t = int(t)
    for i in range(t):
        letter = str(chr(i+65))
        letters.append(letter)
    return letters

def generate(t=3):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    file = dirname + "/../generated/" + "path_dependent_order" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    content = "{order("
    letters = get_letters(t)
    for i in range(len(letters)):
        if i == t-1:
            content += letters[i]  + "):"
        else:
            content += letters[i]  + ","

    for i in range(t-1):
        content += "flow(" + letters[i] + ",_,_), "
        if i==t-2:
            content += "flow(_," + letters[i+1] + ",_)}."
        else:
            content += "flow(_," + letters[i+1] + ",_), "

    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate()