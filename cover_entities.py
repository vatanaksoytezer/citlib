from system_generator import ASPGenerator
import os
import sys

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

def find_word_fixed(word, output, order):
    idx = output.find(word)
    len_word = len(word)
    words = []
    while(idx >= 0):
        edges = ""
        lookup = output[idx:idx+len_word+order*5]
        for i in range(order):
            if i==0:
                edges += lookup.split(",")[i].split("(")[1]
            elif i==order-1:
                edges += lookup.split(",")[i].split(")")[0]
            else:
                edges += lookup.split(",")[i]
        words.append(output[idx:idx+len_word+len(edges)+order])
        output = output[idx+1:]
        idx = output.find(word)
    return words

def parse_entities(output, order):
    word = "entity_covered("
    # get order somehow
    # length = 15 + 2*order
    # entities = find_word(word, length, output)
    entities = find_word_fixed(word, output, order)
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


def delete_coverage_criterion(file):
    with open(file, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if "entity" in i and ":-" in i:
                if "covered" in i:
                    f.write(i)
                else:
                    pass
            else:    
                f.write(i)
        f.truncate()

if __name__ == "__main__":
    generator = ASPGenerator()
    arg_count = len(sys.argv) - 1
    file_int = 0
    file1 = "entities0.lp"
    # big while starts here
    dirname, _ = os.path.split(os.path.abspath(__file__))
    user_file = dirname + "/" + "user.lp"
    order = parse_order(user_file)
    while True:
        # generator.generate("generated.lp", "system_model.lp", "testcase.lp", "maximize.lp", "coverage_criterion.lp", file1)
        # generator.generate("generated.lp", "system_model.lp", "testcase.lp", "coverage_criterion.lp", file1)

        if arg_count == 3:
            generator.generate("generated.lp", sys.argv[1],  sys.argv[2],  sys.argv[3], file1)
        elif arg_count == 0:
            generator.generate("generated.lp", "system_model.lp", "testcase.lp", "coverage_criterion.lp", file1)
        else:
            print("Please enter necessary files as arguments ")
            
        # Delete annnoying line
        delete_coverage_criterion("generated.lp")
        # Get order here
        output = generator.run()
        print(output)
        testcase_file = dirname + "/" + "testcase" + "_" + str(file_int)
        write_to_file(output,testcase_file)
        lines = output.split("\n")
        # This means we found an optimum solution
        line_idx = get_line_idx(lines)
        if line_idx > 0:
            entities = parse_entities(lines[line_idx], order)
            # print(entities)
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