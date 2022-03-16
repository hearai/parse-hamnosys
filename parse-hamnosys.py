from argparse import ArgumentParser
from hamnosys_dicts import HandLocationFronalPlaneTB, HandshapeBaseformsDict, \
                           HandshapeBendingDict, \
                           HandpositionFingerDirectionDict, \
                           HandpositionPalmOrientationDict, \
                           HandshapeThumbPositionDict, \
                           HandLocationDistanceDict, MovementSigns, \
                           SymmetryOperatorsDict, UnknownSymbols1Dict, \
                           UnknownSymbols2Dict, UnknownSymbols3Dict, \
                           UnknownSymbols4Dict

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
    "-l",
    "--log",
    dest="logging",
    metavar="log",
    type=bool,
    help="Enable logging"
)
args = parser.parse_args()

# Read file and create a structure to store results,
# load data from source file and name columns
data = pd.read_csv(args.srcfilename, sep=" ", header=None)
data.columns = ["Name", "Start", "End", "Dict", "Word", "Hamnosys"]

# Duplicate column named Hamnosys to have a copy to work on
# and name it "Hamnosys_copy"
data.insert(6, "Hamnosys_copy", data["Hamnosys"], True)
# Prepare a column for Flag that will be set if non dominant hand is
# analyzed as only. Fill it with 0s (not set).
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
    if ((char == SymmetryOperatorsDict["1"]) or
            (char == SymmetryOperatorsDict["10"])):
        data.at[index, "Symmetry operator"] = 1
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][3:]
        continue
    elif ((char == SymmetryOperatorsDict["2"]) or
          (char == SymmetryOperatorsDict["11"])):
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
    # Check if non dominan hand is analyzed as only and set flag to 1 if true
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

# Handshape base form occurs always after the symmetry operator
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

# For some entries thumb is placed after the bending sign,
# so let's go back to thumb
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

# Remove signs that may appear in this place
# In most cases those are fingers with separate bending signs
for index, row in data.iterrows():
    for i in range(len(UnknownSymbols1Dict)):
        char = row["Hamnosys_copy"][0:1]
        for key, value in UnknownSymbols2Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Analyze second description of a dominant hand.
# For example in notation 
# Dominant hand is described as in beetween 
# In this case  goes to the first description field,
#  goes to the second one.
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "Dominant - Handshape - Baseform2"] = 99
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeBaseformsDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Baseform2"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Thumb position2"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - bending2"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        # for some entries thumb is placed after the bending sign,
        # so let's go back to thumb
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Thumb position2"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        # if base form was not found after "" announce an error
        if data.at[index, "Dominant - Handshape - Baseform2"] == 99:
            data.at[index, "ERROR"] = 2
        char = row["Hamnosys_copy"][0:1]
        # Remove closing bracket if there
        if char == "":
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Analyze non dominat hand description if placed here
# For example in notation  dominant hand
# is described as , and the nondominant hand is described as 
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "Dominant - Handshape - Baseform2"] = 99
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeBaseformsDict.items():
            if char == value:
                data.at[index, "NONominant - Handshape - Baseform"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "NONominant - Handshape - Thumb position"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "NONominant - Handshape - bending"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        # for some entries thumb is placed after the bending sign,
        # so let's go back to thumb
        char = row["Hamnosys_copy"][0:1]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "NONominant - Handshape - Thumb position"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
        # if base form was not found after "" announce an error
        if data.at[index, "NONominant - Handshape - Baseform"] == 99:
            data.at[index, "ERROR"] = 3
        # Remove closing bracket if there
        if char == "":
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Removing "" to be able to analyze examples like the one below
# 
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Remove signs that may appear in beetwen
# In most cases those are fingers with separate bending signs
for index, row in data.iterrows():
    for i in range(len(UnknownSymbols1Dict)):
        char = row["Hamnosys_copy"][0:1]
        for key, value in UnknownSymbols1Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        for key, value in UnknownSymbols2Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

if args.logging:
    print("Dominant - Handposition - extended finger direction:")

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionFingerDirectionDict.items():
        if char == value:
            data.at[index, "Dominant - Handposition - "
                           "extended finger direction"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    if data.at[index, "Dominant - Handposition - "
                      "extended finger direction"] == 99:
        data.at[index, "ERROR"] = 4

# If there are two in a row
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionFingerDirectionDict.items():
        if char == value:
            data.at[index, "Dominant - Handposition - "
                           "extended finger direction2"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# take care of two in a row with "" sign (two for dominant)
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        if data.at[index, "Dominant - Handposition - "
                          "extended finger direction2"] != 0:
            data.at[index, "ERROR"] = 5
        data.at[index, "Dominant - Handposition - "
                       "extended finger direction2"] = 99
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionFingerDirectionDict.items():
        if char == value:
            data.at[index, "Dominant - Handposition - "
                           "extended finger direction2"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    if data.at[index, "Dominant - Handposition - "
                      "Extended finger direction2"] == 99:
        data.at[index, "ERROR"] = 6

# take care of nondominant hand
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "NONDominant - Handposition - "
                       "extended finger direction"] = 99
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionFingerDirectionDict.items():
        if char == value:
            data.at[index, "NONDominant - Handposition - "
                           "extended finger direction"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    if data.at[index, "NONDominant - Handposition - "
                      "Extended finger direction"] == 99:
        data.at[index, "ERROR"] = 7

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handposition - "
                                 "extended finger direction"])
        )

# Remove unnecesairy bracket or some strange dots
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "" or char == "" or char == "":
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

if args.logging:
    print("Dominant - Handposition - Palm Orientation:")

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionPalmOrientationDict.items():
        if char == value:
            data.at[index, "Dominant - Handposition - "
                           "extended finger direction"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# take care of two in a row with "" sign (two for dominant)
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "NONDominant - Handposition - palm orientation"] = 99
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        char = row["Hamnosys_copy"][0:1]
    for key, value in HandpositionPalmOrientationDict.items():
        if char == value:
            data.at[index, "NONDominant - Handposition - "
                           "palm orientation"] = key
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    if data.at[index, "NONDominant - Handposition - Palm orientation"] == 99:
        data.at[index, "ERROR"] = 7

if args.logging:
    for index, row in data.iterrows():
        print(
            str(index)
            + ": "
            + data.at[index, "Hamnosys"]
            + " -> "
            + data.at[index, "Hamnosys_copy"]
            + " = "
            + str(data.at[index, "Dominant - Handposition - "
                                 "extended finger direction"])
        )

# Remove unknown signs
for i in range(5):
    for index, row in data.iterrows():
        char = row["Hamnosys_copy"][0:1]
        for key, value in UnknownSymbols3Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        for key, value in UnknownSymbols4Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Check if handposition left symbol is placed here
for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if char == "":
        data.at[index, "Dominant - Handposition - LR"] = 0
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
    elif char == "":
        data.at[index, "Dominant - Handposition - LR"] = 1
        data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# Removing some signs.."
for i in range(10):
    for index, row in data.iterrows():
        char = row["Hamnosys_copy"][0:1]
        for key, value in UnknownSymbols3Dict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

if args.logging:
    print("Hand location - fronal plane t/b")

# check 4 next signs searching for Handlocation Frontal Plane Top/bottom
for index, row in data.iterrows():
    for i in range(4):
        char = row["Hamnosys_copy"][i: i + 1]
        for key, value in HandLocationFronalPlaneTB.items():
            if char == value:
                data.at[index, "Dominant - Handposition - TB"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
                break
        if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 99:
            break
        for key, value in MovementSigns.items():
            if char == value:
                data.at[index, "Dominant - Handposition - TB"] = 0
                break
        if char == "":
            data.at[index, "Dominant - Handposition - TB"] = 0
            break
        if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 99:
            break

for index, row in data.iterrows():
    char = row["Hamnosys_copy"][0:1]
    if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 99:
        if char == "":
            data.at[index, "Dominant - Handposition - LR"] = "3"
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
        if char == "":
            data.at[index, "Dominant - Handposition - LR"] = "4"
            data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]

# check 4 next signs searching for distance
for index, row in data.iterrows():
    for i in range(4):
        char = row["Hamnosys_copy"][i: i + 1]
        for key, value in HandLocationDistanceDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - Distance"] = key
                data.at[index, "Hamnosys_copy"] = row["Hamnosys_copy"][1:]
                break
        if pd.to_numeric(data.at[index, "Dominant - Handposition - "
                                        "Distance"]) != 3:
            break
        for key, value in MovementSigns.items():
            if char == value:
                data.at[index, "Dominant - Handposition - Distance"] = 3
                break
        if char == "":
            data.at[index, "Dominant - Handposition - Distance"] = 3
            break
        if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 3:
            break

# Save resultant file
f = open(args.dstfilename, "w")

for index, row in data.iterrows():
    f.write(
        str(data.at[index, "Name"])
        + " "
        + str(data.at[index, "Start"])
        + " "
        + str(data.at[index, "End"])
        + " "
        + str(data.at[index, "Symmetry operator"])
        + " "
        + str(data.at[index, "Dominant - Handshape - Baseform"])
        + " "
        + str(data.at[index, "Dominant - Handshape - Thumb position"])
        + " "
        + str(data.at[index, "Dominant - Handshape - Bending"])
        + " "
        + str(data.at[index, "Dominant - Handposition - "
                             "extended finger direction"])
        + " "
        + str(data.at[index, "Dominant - Handposition - Palm orientation"])
        + " "
        + str(data.at[index, "Dominant - Handposition - LR"])
        + " "
        + str(data.at[index, "Dominant - Handposition - TB"])
        + " "
        + str(data.at[index, "Dominant - Handposition - Distance"])
    )
    f.write("\n")
f.close()
