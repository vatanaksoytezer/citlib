from system_generator import ASPGenerator
import os

def read_file(filename):
    file = open(filename, "r")
    lines = []
    for line in file:
        lines.append(line)
    file.close()
    return lines
    
def find_word(word, len, output):
    words = []
    idx = output.find(word)
    words = []
    while(idx >= 0):
        words.append(output[idx:idx+len])
        output = output[idx+1:]
        idx = output.find(word)
    return words

def parse_entities(output, order):
    word = "entity_covered("
    # get order somehow
    length = 15 + 2*order
    entities = find_word(word, length, output)
    # print(entities)
    for i in range(len(entities)):
        entity = entities[i]
        # print(entity)
        entities[i] = entity[0:6] + entity[14:]# entity # 
    # print(entities)

    return entities

def get_line_idx(lines):
    line_idx = -1
    for i in range(len(lines)):
        if "entity_covered" in lines[i]:
            line_idx = i
    return line_idx

def list_to_str(ls):
    str = ""
    for i in ls:
        str += i + ".\n"
    return str

def write_to_file(content, filename):
    file = open(filename, "w")
    file.write(content)
    file.close()


def file_to_str(filename):
    file = open(filename, "r")
    data = file.read()
    file.close()
    return data

# File vs entites list
# Will write the diffe
def get_diff_entities(file1, current_entities):
    entities_list_1 = file_to_str(file1).split(".\n")[:-1] # discard the last line
    diff_entities = []

    for entity in entities_list_1:
        if entity in current_entities:
            pass
        else:
            diff_entities.append(entity)
    return diff_entities

def parse_order(file):
    content = read_file(file)
    for line in content:
        idx = line.find("t=")
        if line[0] != "%" and idx != -1:
            order = line[idx+2]
            return int(order)

if __name__ == "__main__":
    generator = ASPGenerator()
    file_int = 0
    file1 = "entities0.lp"
    # big while starts here
    dirname, _ = os.path.split(os.path.abspath(__file__))
    user_file = dirname + "/" + "user.lp"
    order = parse_order(user_file)
    while True:
        generator.generate("generated.lp", "system_model.lp", "user.lp", "testcase.lp", file1)
        # Get order here
        output = generator.run()
        print(output)
        lines = output.split("\n")
        # This means we found an optimum solution
        line_idx = get_line_idx(lines)
        if line_idx > 0:
            entities = parse_entities(lines[line_idx], order)
            print(entities)
            diff_entities = get_diff_entities(file1,entities)
            # print(diff_entities)
            entities_str = list_to_str(diff_entities)
            file2 = "entities"
            file_int += 1
            file2 += str(file_int) + ".lp"
            write_to_file(entities_str, file2)
            print("The remaining entities are put in", file2)
            # print("Diff Len:", diff_entities)
        else:
            print("All entities that are coverable are covered")
            break

        file1 = file2
        # input()
    
    # generator.clean()
    # Parse optimized entitites