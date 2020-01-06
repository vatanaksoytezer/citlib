import os
import sys

def get_letters(t):
    letters = []
    t = int(t)
    for i in range(t):
        letter = str(chr(i+65))
        letters.append(letter)
    return letters

def add_n_times(str, letter, times, end):
    # if end = 0 add to begining
    # if end = 1 add to end
    for i in range(times):
        str += letter
        if (i == times-1) and end == 1:
            pass
        else:
            str += ","
    return str

def generate(t=3):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    file = dirname + "/../generated/" + "maximize" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    content = "#maximize{1@1,"
    letters = get_letters(t)
    for i in range(len(letters)):
        if i == t-1:
            content += letters[i]  + ":"
        else:
            content += letters[i]  + ","

    content += " entity_covered("

    for i in range(len(letters)):
        if i == t-1:
            content += letters[i]  + ")}."
        else:
            content += letters[i]  + ","

    print(content)
    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate()