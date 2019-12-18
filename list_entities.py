from system_generator import ASPGenerator
import os

def find_word(word, len, output):
    idx = output.find(word)
    words = []
    while(idx >= 0):
        words.append(output[idx:idx+len])
        output = output[idx+1:]
        idx = output.find(word)
    return words

def parse_entities(output, order):
    word = "entity("
    # get order somehow
    len = 7 + 2*order
    entities = find_word(word, len, output)
    return entities

def list_to_str(ls):
    str = ""
    for i in ls:
        str += i + ".\n"
    return str

def write_to_file(content, filename):
    file = open(filename, "w")
    file.write(content)
    file.close()

def read_file(filename):
    file = open(filename, "r")
    lines = []
    for line in file:
        lines.append(line)
    file.close()
    return lines

def parse_order(file):
    content = read_file(file)
    for line in content:
        idx = line.find("t=")
        if line[0] != "%" and idx != -1:
            order = line[idx+2]
            return int(order)

if __name__ == "__main__":
    generator = ASPGenerator()
    generator.generate("generated.lp", "user.lp", "coverage_criterion.lp", "system_model.lp")
    output = generator.run()
    # Get order here
    dirname, _ = os.path.split(os.path.abspath(__file__))
    user_file = dirname + "/" + "user.lp"
    order = parse_order(user_file)
    # order = 3

    # List Entities
    entities = parse_entities(output, order)
    entities_str = list_to_str(entities)
    write_to_file(entities_str, "entities0.lp")
    # generator.clean()
