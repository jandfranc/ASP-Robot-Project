import subprocess

def get_answer_set(file):
    cmd = 'java -jar sparc.jar {} -A'.format(file)
    answer_set = subprocess.check_output(cmd)
    print(answer_set)


if __name__ == "__main__":
    get_answer_set("s_ancestors.sp")
