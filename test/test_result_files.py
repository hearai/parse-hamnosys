import difflib
import sys
import os

test_file = "test_result.txt"
result_file = "../parsed_hamnosys.txt"
diff_file = "diff.txt"

def compare_files():
    diffs = []
    i = 0

    # remove file with differences from previous run
    if os.path.exists(diff_file):
        os.remove(diff_file)
        
    # read test and result file
    with open(test_file) as file1:
        file1_text = file1.readlines()

    with open(result_file) as file2:
        file2_text = file2.readlines()

    for line in difflib.unified_diff(
        file1_text, file2_text, fromfile=test_file, tofile=result_file):
            i = i + 1
            if(line[0] == "+" or line[0] == "-"):
                diffs.append(line)

    if(i != 0):
        with open(diff_file, 'w') as f:
            f.write(str(diffs))

if __name__ == "__main__":
    compare_files()
