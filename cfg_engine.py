#rulare cod terminal
#python cfg_engine.py exfile.txt
import random
import sys


def get_section(section_name, lines): 
    ok = 0
    section_lines = []
    for line in lines:
        if line.lower() == section_name.lower() + ":":
            ok = 1
            continue
        if line.lower() == "end":
            ok = 0
        if ok:
            section_lines.append(line)
    return section_lines

def get_cfg_from_file(file_name): 
    with open(file_name, "r") as file:
        lines = [line.strip() for line in file if len(line.strip()) > 0]

    variables = get_section("variables", lines)
    terminals = get_section("terminals", lines)
    rules_lines = get_section("rules", lines)

    rules = {}
    for rule in rules_lines:
        left, right = rule.split("=")
        left, right = left.strip(), right.strip()
        if left not in rules:
            rules[left] = []
        rules[left].append(right)

    for left, right_list in rules.items():
        if left not in variables:
            print(f"error: variabila \"{left}\" nu exista")
            exit()
        for right in right_list:
            for symbol in list(right):
                if symbol not in variables and symbol not in terminals:
                    print(f"error: terminalul \"{symbol}\" nu exista")
                    exit()

    start_variable = variables[0]

    for terminal in terminals:
        if terminal in variables:
            print("error: terminalii si variabilele trebuie sa fie distincte")
            exit()

    return start_variable, variables, terminals, rules

def cfg_process(start_variable, variables, terminals, rules):
    generated_strings = []
    current_string = start_variable

    while any(variable in current_string for variable in variables):
        applicable_rules = []
        for variable in variables:
            if variable in current_string:
                applicable_rules.extend((variable, production) for production in rules[variable])

        random_rule = random.choice(applicable_rules)
        current_string = current_string.replace(random_rule[0], random_rule[1], 1)
        while "_" in current_string:
            current_string = current_string.replace("_", "")

    generated_strings.append(current_string)

    return generated_strings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input: python cfg_engine.py exfile.txt")
        sys.exit(1)

    cfg_config_file = sys.argv[1]

    start_variable, variables, terminals, rules = get_cfg_from_file(cfg_config_file)

    print(f"Start variable: {start_variable}")
    print(f"Variables: {variables}")
    print(f"Terminals: {terminals}")
    print(f"Rules: {rules}")

    generated_strings = cfg_process(start_variable, variables, terminals, rules)
    print(f"String generat aleator: {generated_strings}")
