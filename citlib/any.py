import os
import sys

def generate(t=3):
    # generate for t order
    dirname, _ = os.path.split(os.path.abspath(__file__))
    file = dirname + "/../generated/" + "any" + str(t) + ".lp"
    print("Generating " + file + " as requested from the user...")
    content = ":- T = #sum{E,"
    flows = []
    order = "order("
    for i in range(t):
        letter = str(chr(i+65))
        flow = "flow(_," + letter + ",E)," 
        flows.append(flow)
        if (i == t-1):
            order += letter + ")"
            content += letter + ": "
        else:
            order += letter + ","
            content += letter + ","
    content += "".join(flows) + order + "}, T!=1."
    # Write to file
    f = open(file, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Arg is order
    generate()