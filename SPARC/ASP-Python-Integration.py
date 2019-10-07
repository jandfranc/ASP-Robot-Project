import subprocess

def getAnswerSets(file):
#Takes ASP file as input and returns its answer set
    cmd = 'java -jar sparc.jar {} -A'.format(file)
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

def removeNotTrue(answerset):
    


if __name__ == "__main__":
    #get_answer_set("s_ancestors.sp")
    a = splitAnswerSets(getAnswerSets("s_bwplan.sp"))
    print(a[0])
