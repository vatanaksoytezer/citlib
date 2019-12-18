import os
import sys

def get_letters(t):
    letters = []
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
    file = dirname + "/../generated/" + "order" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    letters = get_letters(t)
    reaches = ""
    orders = []
    not_orders = []
    content = "{order(" + ",".join(letters) + ") : "

    for i in range(t):
        letter = str(chr(i+65))
        next_letter = str(chr(i+66))
        not_orders.append("_")
        count = i+1
        if i < t-1:
            reaches += "reaches(" + letter + "," + next_letter + ")"    
        # First order
        order = ":-order("
        order = add_n_times(order, "_", count-1, 0)
        order += letter
        if(i != t-1):
            order += ","
        order = add_n_times(order, "_", t-count, 1)
        # Second order
        order += "), order("
        order = add_n_times(order, "_", count-1, 0)
        order += letter + "1"
        if(i != t-1):
            order += ","
        order = add_n_times(order, "_", t-count, 1)
        order += "), " + letter + "!=" + letter + "1."
        orders.append(order)
        if i < t-2:
            reaches += ","
    content += reaches + "} :- vertex(A).\n" + "\n".join(orders)
    content += "\n:- not order(" + ",".join(not_orders) + ").\n#show order/" + str(t) + "."
    # Write to file
    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate(sys.argv[0])