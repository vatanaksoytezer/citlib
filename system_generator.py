from subprocess import Popen, PIPE
import os, glob, importlib, sys
from compile_bool_exprs import *

class ASPGenerator:

    def __init__(self):
        self.keywords = ["##", "bool_expr", "edge_guard"]
        self.output_file = ""
        self.output_content = ""
        self.dirname, _ = os.path.split(os.path.abspath(__file__))
        self.timeout = 0
        self.bool_exprs = []
        self.edge_pairs = []

    def read_file(self, filename):
        file = open(filename, "r")
        lines = []
        for line in file:
            lines.append(line)
        file.close()
        return lines

    def file_to_str(self, filename):
        file = open(filename, "r")
        data = file.read()
        file.close()
        return data

    def append_to_file(self, content, filename):
        file = open(filename, "a")
        file.write(content)
        file.close()
    
    def write_to_file(self, content, filename):
        file = open(filename, "w")
        file.write(content)
        file.close()
    
    def get_file(self, line):
        command = line[9:len(line)-2]
        filename = self.dirname + "/"
        names = command.split(".")
        keyword_hash = {}
        for name in names:
            if name == names[-1]:
                hash_str = name
                while "," in hash_str:
                    idx = name.index(",")
                    hash_str = name[idx+1:]
                    element = hash_str.split(",")[0]
                    # do the split here
                    try:
                        key, val = element.split("=")
                        keyword_hash[key] = val
                    except:
                        # print("Paramater not in correct format !")
                        break
                
                if "t" in keyword_hash.keys():
                    num = int(name.split("=")[1])
                    if num >= 2:
                        f = name.split(",")[0]
                        self.generate_file(f, num)
                        filename += f + str(num) + ".lp"
                    else:
                        print("Order is less than 2, exiting!")
                        sys.exit()
                else:
                    filename += name + ".lp"
            else:
                if ",t=" in names[-1]:
                    filename += "generated" + "/"
                else:
                    filename += name + "/"
        return filename

    def generate_file(self, func, t):
        # Meta function to generate new clingo files
        filename = self.dirname + "/generated/" + func + str(t) + ".lp"
        if not os.path.isfile(filename):
            pyfilename = self.dirname + "/citlib/" + func + ".py"
            if os.path.isfile(pyfilename):
                module_name = "citlib." + func
                module = importlib.import_module(module_name)
            else:
                module_name = "citlib.generic"
                module = importlib.import_module(module_name)
            module.generate(t)
        else:
            pass

    # This is not the most efficient way to do it
    def get_letters(self, t):
        letters = []
        for i in range(t):
            letter = str(chr(i+65))
            letters.append(letter)
        return letters

    def parse_input(self, content):
        for line in content:
            if line[0] == "%":
                self.append_to_file(line, self.output_file)
                # pass
            elif self.keywords[0] in line:
                if "import" in line:
                    file = self.get_file(line)
                    file_content = "\n\n%%%%%%%%%% Auto Generated from " + file + " %%%%%%%%%%%%\n\n"
                    file_content += self.file_to_str(file)
                    self.append_to_file(file_content, self.output_file)
                    self.append_to_file("\n", self.output_file)
                elif "def" in line:
                    self.timeout = line.split("=")[1].strip("\n")
            elif self.keywords[1] in line:
                self.bool_exprs.append(line)
            # elif self.keywords[2] in line:
            #     pairs = self.parse_edge_pairs(line)
            #     if pairs:
            #         self.edge_pairs.append(pairs)
            else:
                # print(line)
                self.append_to_file(line, self.output_file)

    def parse_coverage(self, content):
        # find order first
        for line in content:
            idx = line.find("entity(")
            if line[0] != "%" and idx != -1:
                entity_part = line[idx:]
                # print(entity_part)
                entity_content = entity_part.split(")")[0]
                order = entity_content.count(",") + 1   
                break
        
        output = ""
        for line in content:
            line_output = "entity_covered(" + entity_content[7:] + ") :- "
            if line[0] == "%":
                self.append_to_file(line, self.output_file)
            else:
                if line.find("entity(") != -1:
                    line_output += line.replace(":-", ",") + "\n"
                    output += line_output
        
        output += "\n" + "#show entity_covered/" + str(order) + "."
        # print(output)
        self.append_to_file(output, self.output_file)
            

    def add_bool_exprs(self):
        content = compile_bool_exprs(self.bool_exprs)
        self.append_to_file(content, self.output_file)

    # Detonates edges
    def detonate_edge(self, s1, s2):
        with open(self.output_file, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if "edge" in i:
                    if str(s1) in i and str(s2) in i:
                        pass
                    else:
                        f.write(i)
                else:    
                    f.write(i)
            f.truncate()

    def parse_edge_pairs(self, content):
        # if contains f (smthng like d1f)
        if "f" in content:
            edges_str = content.split(")")[0].split("(")[1]
            edges = edges_str.split(",")
            return edges
        else:
            return None

    def clean_file(self, filename):
        file = open(filename, "w")
        file.close()

    # TODO: Check correctness of *args
    def generate(self, _output_file, *args):
        self.output_file = self.dirname + "/" + _output_file
        self.clean_file(self.output_file)
        for input_file in args:
            # Special case
            # print(input_file)
            # TODO: Change this
            if input_file == "coverage_criterion.lp":
            # if input_file == "nothing.lp":
                input_file = self.dirname + "/" + input_file
                input_content = self.read_file(input_file)
                self.parse_input(input_content)
                self.parse_coverage(input_content)
            else:
                input_file = self.dirname + "/" + input_file
                input_content = self.read_file(input_file)
                self.parse_input(input_content)
        # Bool adder :P
        self.add_bool_exprs()
        # Edge remover xD
        # for edge_pair in self.edge_pairs:
        #     s1 = edge_pair[0]
        #     s2 = edge_pair[1]
        #     self.detonate_edge(s1, s2)


    def get_response(self, script):
        response = Popen([script],stdout=PIPE,shell=True)
        output = response.communicate()[0].decode()
        return output

    def run(self, file1=None):
        # Run clingo here
        # clingo_script = "clingo -n 0 --time-limit 0 " + self.output_file
        if not file1:
            # clingo_script = "clingo -n 0 --time-limit " + self.timeout + " " + self.output_file
            clingo_script = "clingo -n 0 --project --time-limit " + self.timeout + " " + self.output_file
        else:
            pass
            # clingo_script = "clingo -n 0 --time-limit " + self.timeout + " " + self.output_file + "" + file1
        print(clingo_script)
        output = self.get_response(clingo_script)
        return output
        
    def clean(self):
        file = self.output_file
        os.remove(file)
        folder = self.dirname + "/generated/*"
        files = glob.glob(folder)
        for f in files:
            os.remove(f)

if __name__ == "__main__":
    generator = ASPGenerator()
    # generator.generate("generated.lp", "user.lp", "coverage_criterion.lp", "testcase.lp")
    generator.generate("generated.lp", "generate.lp", "coverage_criterion.lp", "system_model.lp")
    output = generator.run()
    # print(output)
    # Clean all generated files
    # generator.clean()
