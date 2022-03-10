from argparse import ArgumentParser
import pandas as pd

# Parse arguments
parser = ArgumentParser()
parser.add_argument(
    "-sf",
    "--src_file",
    dest="srcfilename",
    metavar="srcfile",
    type=str,
    help="File to read from",
)
parser.add_argument(
    "-df",
    "--dst_file",
    dest="dstfilename",
    metavar="dstfile",
    type=str,
    help="File to save to",
)
parser.add_argument(
    "-l", "--log", dest="logging", metavar="log", type=bool, help="Enable logging"
)
args = parser.parse_args()

# Read file and create a structure to store results,
# load data from source file and name columns
data = pd.read_csv(args.srcfilename, sep=" ", header=None)
data.columns = ["Name", "Start", "End", "Dict", "Word", "Hamnosys"]

# Duplicate column named Hamnosys to have a copy to work on, and name it "Hamnosys_copy"
data.insert(6, "Hamnosys_copy", data["Hamnosys"], True)
# Prepare a column for Flag that will be set if non dominant hand is analyzed as only
# Fill it with 0s (not set)
data.insert(7, "NonDom first", 0)
# Prepare a column for symmetry operator
data.insert(8, "Symmetry operator", 0)
# Prepare columns for all analyzed features
data.insert(9, "Dominant - Handshape - Baseform", 99)
data.insert(10, "Dominant - Handshape - Thumb position", 0)
data.insert(11, "Dominant - Handshape - Bending", 0)
data.insert(12, "Dominant - Handposition - Extended finger direction", 99)
data.insert(13, "Dominant - Handposition - Palm orientation", 99)
data.insert(14, "Dominant - Handposition - LR", 2)
data.insert(15, "Dominant - Handposition - TB", 14)
data.insert(16, "Dominant - Handposition - Distance", 3)
data.insert(17, "Dominant - Handshape - Baseform2", 0)
data.insert(18, "Dominant - Handshape - Thumb position2", 0)
data.insert(19, "Dominant - Handshape - Bending2", 0)
data.insert(20, "Dominant - Handposition - Extended finger direction2", 0)
data.insert(21, "Dominant - Handposition - Palm orientation2", 0)
data.insert(22, "Dominant - Handposition - LR2", 0)
data.insert(23, "Dominant - Handposition - TB2", 0)
data.insert(24, "Dominant - Handposition - Distance2", 0)
data.insert(25, "NONDominant - Handshape - Baseform", 0)
data.insert(26, "NONDominant - Handshape - Thumb position", 0)
data.insert(27, "NONDominant - Handshape - Bending", 0)
data.insert(28, "NONDominant - Handposition - Extended finger direction", 0)
data.insert(29, "NONDominant - Handposition - Palm orientation", 0)
data.insert(30, "NONDominant - Handposition - LR", 0)
data.insert(31, "NONDominant - Handposition - TB", 0)
data.insert(32, "NONDominant - Handposition - Distance", 0)
data.insert(33, "NONDominant - Handshape - Baseform2", 0)
data.insert(34, "NONDominant - Handshape - Thumb position2", 0)
data.insert(35, "NONDominant - Handshape - Bending2", 0)
data.insert(36, "NONDominant - Handposition - Extended finger direction2", 0)
data.insert(37, "NONDominant - Handposition - Palm orientation2", 0)
data.insert(38, "NONDominant - Handposition - LR2", 0)
data.insert(39, "NONDominant - Handposition - TB2", 0)
data.insert(40, "NONDominant - Handposition - Distance2", 0)
data.insert(41, "ERROR", 0)