from argparse import ArgumentParser
import difflib
import sys
import os


def get_args_parser():
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument(
        "-tf",
        "--test_file",
        dest="testfilename",
        metavar="test_file",
        type=str,
        help="File to read from",
    )
    parser.add_argument(
        "-rf",
        "--result_file",
        dest="resultfilename",
        metavar="result_file",
        type=str,
        help="File to save to",
    )
    return parser


def main(args):
    diff_file = os.path.join("test", "diff.txt")
    diffs = []
    i = 0

    # Parse test and result files
    test_file = args.testfilename
    result_file = args.resultfilename

    # Remove file with differences from previous run
    if os.path.exists(diff_file):
        os.remove(diff_file)

    # Read test and result file
    with open(test_file) as file1:
        file1_text = file1.readlines()

    with open(result_file) as file2:
        file2_text = file2.readlines()

    for line in difflib.unified_diff(
        file1_text, file2_text, fromfile=test_file, tofile=result_file
    ):
        i = i + 1
        if line[0] == "+" or line[0] == "-":
            diffs.append(line)

    if i != 0:
        with open(diff_file, "w") as f:
            f.write(str(diffs))
        print("Different test and result files")
    else:
        print("Test and result files are the same")

if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)
