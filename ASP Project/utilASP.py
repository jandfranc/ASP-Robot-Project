import subprocess

def solve_answer_sets(file, no_of_answer_sets = 9999):
#Takes ASP file as input and returns its answer set
    cmd = 'java -jar sparc.jar {} -A -n {}'.format(file, no_of_answer_sets)
    answer_set = subprocess.check_output(cmd)
    answer_set = answer_set.decode('utf-8')
    return answer_set


def split_answer_sets(set_to_split):
#splits answer sets into individual answer sets, then creates a list of each individual instruction within each answer set
    split_string = set_to_split.splitlines()
    split_string = split_string[::2]
    split_string = list(map(lambda x: x[1:-1], split_string))
    split_string = [x.split(', ') for x in split_string]
    return split_string

def read_file_sp_to_list(file):
#converts file to a list with no empty lines or comments, for better adding of logic later
    read_file = None
    try:
        read_file = open(file,'r')
        file_as_list = read_file.read().splitlines()
    finally:
        read_file.close()

    fixed_list = []
    for it_line in file_as_list:
        if it_line == '' or it_line[0] == '%':
            pass
        else:
            for it_letter in it_line:
                if it_letter != ' ':
                    fixed_list.append(it_line)
                    break
    return fixed_list


def write_list_to_file(file,list):
#does what it says on the tin
    write_file = None
    try:
        write_file = open(file,'w')
        for it_line in list:
            write_file.write(it_line)
            write_file.write('\n')
    finally:
        write_file.close()

def split_asp_sections(input_list):
#takes input from a read asp file and outputs it split into sections (rules, etc.)
    sorts_idx = input_list.index('sorts')
    predicates_idx = input_list.index('predicates')
    rules_idx = input_list.index('rules')
    display_idx = input_list.index('display')
    constants_list = input_list[0:sorts_idx]
    sorts_list = input_list[sorts_idx:predicates_idx]
    predicates_list = input_list[predicates_idx:rules_idx]
    rules_list = input_list[rules_idx:display_idx]
    display_list = input_list[display_idx::]
    return constants_list, sorts_list, predicates_list, rules_list, display_list

def add_rules(rules_list,item_to_add):
    rules_list += item_to_add
    return rules_list

def edit_sorts(sorts_list, sort_to_edit, new_val):
    for iter in range(0,len(sorts_list)):
        if (sort_to_edit + ' =') in sorts_list[iter]:
            sorts_list[iter] = sort_to_edit + ' = [' + sort_to_edit[1] + '][0..' + str(new_val) + '].'
            print(sorts_list[iter])
            return sorts_list

def edit_constant(constants_list, new_val):
    constants_list = ['#const n='+str(new_val) + '.']
    return constants_list

def add_sections_together(*args):
    returned_list = []
    for it in args:
        returned_list += it
    return returned_list

def find_minimal_answersets(file,written_file, max_const, init_const = 0):
#goes from 0 or specified number up until an answer set is returned, first checks if an answer set is possible.
#IF NO ANSWER SET EXISTS WILL NEVER END
    ASP_list = read_file_sp_to_list(file)
    constants_list, sorts_list, predicates_list, rules_list, display_list = split_asp_sections(ASP_list)
    answer_set = ''
    constant_to_add = init_const
    while len(answer_set) < 3:
        constant_to_add += 1
        constants_list = edit_constant(constants_list, constant_to_add)
        combined_ASP_sections = add_sections_together(constants_list, sorts_list, predicates_list, rules_list, display_list)
        write_list_to_file(written_file,combined_ASP_sections)
        answer_set = solve_answer_sets(written_file)
        if constant_to_add > max_const:
            return False
    answer_set = split_answer_sets(answer_set)
    len_answer_sets = 9999
    returned_sets = []
    for it_set in answer_set:
        if len_answer_sets == len(it_set):
            returned_sets.append(it_set)
        elif len_answer_sets > len(it_set):
            len_answer_sets = len(it_set)
            returned_sets = [it_set]

    return returned_sets
