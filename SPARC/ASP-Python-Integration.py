import subprocess

def solveAnswerSets(file, no_of_answer_sets = 9999999999999):
#Takes ASP file as input and returns its answer set
    cmd = 'java -jar sparc.jar {} -A -n {}'.format(file, no_of_answer_sets)
    answer_set = subprocess.check_output(cmd)
    answer_set = answer_set.decode('utf-8')
    return answer_set


def splitAnswerSets(set_to_split):
#splits answer sets into individual answer sets, then creates a list of each individual instruction within each answer set
    split_string = set_to_split.splitlines()
    split_string = split_string[::2]
    split_string = list(map(lambda x: x[1:-1], split_string))
    split_string = [x.split(', ') for x in split_string]
    return split_string

def removeNotRelevant(answerset):
    #NoT NECCESSARY
#removes all values not part of the plan - must be a list of answer sets inputted
    for i_sets in range(0,len(answerset)):
        answerset[i_sets] = [x for x in answerset[i_sets] if x[0] != '-']
        answerset[i_sets] = [x for x in answerset[i_sets] if x[0:6] == 'occurs']
    return answerset

def getAnswerSet(file):
#performs all steps in getting instructions
    returned_val = solveAnswerSets(file)
    returned_val = splitAnswerSets(returned_val)
    return answer_set_list

if __name__ == "__main__":
    #get_answer_set("s_ancestors.sp")
    #a = splitAnswerSets(getAnswerSets("s_bwplan.sp"))
    #a = removeNotTrue(a)
    a = getAnswerSet('testplan.sp')
    print(a)
