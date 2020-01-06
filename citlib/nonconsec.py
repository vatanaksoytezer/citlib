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
    file = dirname + "/../generated/" + "nonconsec" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    letters = get_letters(t)
    content = ":- "
    order = "order(" + ",".join(letters) + ")},"
    sums = ""
    flows = []
    e_ns = []
    t_ns = []

    for i in range(t-1):
        letter = str(chr(i+65))
        next_letter = str(chr(i+66))
        e_n = "E" + str(i+1)
        t_n = "T" + str(i+1)
        e_ns.append(e_n)
        t_ns.append(t_n)
        flow = "flow(" + letter + "," + next_letter + "," + e_n + "), "
        flows.append(flow)

    # This is not the most efficient way to it
    for i in range(t-1):
        content += t_ns[i] + " = #sum{" + e_ns[i] + ": " + "".join(flows) + order
    
    content += "+".join(t_ns) + ">=" + str(t-1) + "."
    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate()