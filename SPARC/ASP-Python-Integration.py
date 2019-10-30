import subprocess

def solve_answre_sets(file, no_of_answer_sets = 9999999999999):
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

def remove_not_relevant(answerset):
    #NoT NECCESSARY
#removes all values not part of the plan - must be a list of answer sets inputted
    for i_sets in range(0,len(answerset)):
        answerset[i_sets] = [x for x in answerset[i_sets] if x[0] != '-']
        answerset[i_sets] = [x for x in answerset[i_sets] if x[0:6] == 'occurs']
    return answerset

def get_answer_set(file):
#performs all steps in getting instructions
    returned_val = solve_answer_sets(file)
    returned_val = split_answer_sets(returned_val)
    return answer_set_list

def read_file_sp_to_list(file):
#converts file to a list with no empty lines or comments, for better adding of logic later
    read_file = None
    write_file = None
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

if __name__ == "__main__":
    #get_answer_set("s_ancestors.sp")
    #a = splitAnswerSets(getAnswerSets("s_bwplan.sp"))
    #a = removeNotTrue(a)
    a = read_file_sp_to_list('robot_give.sp')
    split_asp_sections(a)
