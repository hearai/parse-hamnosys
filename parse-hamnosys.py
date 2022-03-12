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

if args.logging:
    print("Symetry operator:")

for index, row in data.iterrows():
    # Search for symmetry operators that consists of 3 symbols, remove if found
    char = row["Hamnosys_copy"][0:3]
    if (char == SymmetryOperatorsDict["1"]) or (char == SymmetryOperatorsDict["10"]):
        data.at[index, "Symmetry operator"] = 1
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][3:]
        continue
    elif (char == SymmetryOperatorsDict["2"]) or (char == SymmetryOperatorsDict["11"]):
        data.at[index, "Symmetry operator"] = 2
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][3:]
        continue

    # Search for symmetry operators that consists of 2 symbols, remove if found
    char = row["Hamnosys_copy"][0:2]
    if char == SymmetryOperatorsDict["3"]:
        data.at[index, "Symmetry operator"] = 3
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][2:]
        continue
    elif char == SymmetryOperatorsDict["4"]:
        data.at[index, "Symmetry operator"] = 4
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][2:]
        continue
    elif char == SymmetryOperatorsDict["5"]:
        data.at[index, "Symmetry operator"] = 5
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][2:]
        continue
    elif char == SymmetryOperatorsDict["6"]:
        data.at[index, "Symmetry operator"] = 6
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][2:]
        continue

    # Search for symmetry operators that consists of 1 symbol, remove if found
    char = row["Hamnosys_copy"][0:1]
    if char == SymmetryOperatorsDict["7"]:
        data.at[index, "Symmetry operator"] = 7
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        continue
    elif char == SymmetryOperatorsDict["8"]:
        data.at[index, "Symmetry operator"] = 8
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        continue
    # Check if non dominan hand is analyzed as only and set flag to 1 if this is true
    elif char == "":
        data.at[index, "Symmetry operator"] = 0
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        data.at[index, "NonDom first"] = 1
        continue

    # If no symmetry operators were found mark class as 0
    else:
        data.at[index, "Symmetry operator"] = 0

# Log analysis result if logging is enabled
if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Symmetry operator"])
        )

# Remove unknown signs - do it many times as you never know the order;
for i in range(len(UnknownSymbols1Dict)):
    for index, row in data.iterrows():
        char = row["Hamnosys_copy"][0:1]
        for key, value in UnknownSymbols1Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

if args.logging:
    print("Dominant - Handshape - Baseform:")

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandshapeBaseformsDict.items():
        if char == value:
            data.at[index, "Dominant - Handshape - Baseform"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
            continue
    if data.at[index, "Dominant - Handshape - Baseform"] == 99:
        data.at[index, "ERROR"] = 1

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handshape - Baseform"])
        )

if args.logging:
    print("Dominant - Handshape - Thumb position:")

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandshapeThumbPositionDict.items():
        if char == value:
            data.at[index, "Dominant - Handshape - Thumb position"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
            continue

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handshape - Thumb position"])
        )

if args.logging:
    print("Dominant - Handshape - Bending")

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandshapeBendingDict.items():
        if char == value:
            data.at[index, "Dominant - Handshape - bending"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
            continue

# This code removes duplicated bendings
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandshapeBendingDict.items():
        if char == value:
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
            continue

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handshape - Bending"])
        )

if args.logging:
    print("Dominant - Handshape - Thumb position - second try:")

# For some entries thumb is placed after the bending sign, so let's go back to thumb
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandshapeThumbPositionDict.items():
        if char == value:
            data.at[index, "Dominant - Handshape - Thumb position"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
            continue

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handshape - Thumb position"])
        )
