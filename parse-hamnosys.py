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


def get_args_parser():
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
        #metavar="log",
        action="store_true",
        default=False,
        help="Enable logging"
    )
    parser.add_argument(
        "-c",
        "--column",
        dest="columnnames",
        metavar="col",
        nargs='+',
        type=str,
        default=["Name", "Start", "End", "Dict", "Word", "Hamnosys"],
        help="Input column names"
    )
    parser.add_argument(
        "-co",
        "--column-out",
        dest="columnnamesout",
        metavar="colout",
        nargs='+',
        type=str,
        default=["Name", "Start", "End", "Symmetry operator",
                 "Dominant - Handshape - Baseform",
                 "Dominant - Handshape - Thumb position",
                 "Dominant - Handshape - Bending",
                 "Dominant - Handposition - Extended finger direction",
                 "Dominant - Handposition - Palm orientation",
                 "Dominant - Handposition - LR",
                 "Dominant - Handposition - TB",
                 "Dominant - Handposition - Distance"],
        help="Output column names"
    )
    return parser


def main(args):
    # Read file and create a structure to store results,
    # load data from source file and name columns
    data = pd.read_csv(args.srcfilename, sep=" ", header=None)
    data.columns = args.columnnames

    # Work on Hamnosys_copy array
    Hamnosys_copy = data["Hamnosys"].values
    # Prepare a column for Flag that will be set if non dominant hand is
    # analyzed as only. Fill it with 0s (not set).
    # Prepare a column for symmetry operator and all analyzed features
    data = data.reindex(columns=[
        *data.columns,
        "NonDom first",
        "Symmetry operator",
        "Dominant - Handshape - Baseform",
        "Dominant - Handshape - Thumb position",
        "Dominant - Handshape - Bending",
        "Dominant - Handposition - Extended finger direction",
        "Dominant - Handposition - Palm orientation",
        "Dominant - Handposition - LR",
        "Dominant - Handposition - TB",
        "Dominant - Handposition - Distance",
        "Dominant - Handshape - Baseform2",
        "Dominant - Handshape - Thumb position2",
        "Dominant - Handshape - Bending2",
        "Dominant - Handposition - Extended finger direction2",
        "Dominant - Handposition - Palm orientation2",
        "Dominant - Handposition - LR2",
        "Dominant - Handposition - TB2",
        "Dominant - Handposition - Distance2",
        "NONDominant - Handshape - Baseform",
        "NONDominant - Handshape - Thumb position",
        "NONDominant - Handshape - Bending",
        "NONDominant - Handposition - Extended finger direction",
        "NONDominant - Handposition - Palm orientation",
        "NONDominant - Handposition - LR",
        "NONDominant - Handposition - TB",
        "NONDominant - Handposition - Distance",
        "NONDominant - Handshape - Baseform2",
        "NONDominant - Handshape - Thumb position2",
        "NONDominant - Handshape - Bending2",
        "NONDominant - Handposition - Extended finger direction2",
        "NONDominant - Handposition - Palm orientation2",
        "NONDominant - Handposition - LR2",
        "NONDominant - Handposition - TB2",
        "NONDominant - Handposition - Distance2",
        "ERROR"],
        fill_value=0)
    # change some default values for chosen columns
    data["Dominant - Handshape - Baseform"] = 99
    data["Dominant - Handposition - Extended finger direction"] = 99
    data["Dominant - Handposition - Palm orientation"] = 99
    #data["Dominant - Handposition - LR"] = 2
    data["Dominant - Handposition - TB"] = 14
    #data["Dominant - Handposition - Distance"] = 3

    if args.logging:
        print("Symetry operator:")

    for index, row in data.iterrows():
        # Search for symmetry operators that consists of 3 symbols, remove if found
        char = Hamnosys_copy[index][0:3]
        if ((char == SymmetryOperatorsDict["1"]) or
                (char == SymmetryOperatorsDict["9"])):
            data.at[index, "Symmetry operator"] = 1
            Hamnosys_copy[index] = Hamnosys_copy[index][3:]
            continue
        elif ((char == SymmetryOperatorsDict["2"]) or
            (char == SymmetryOperatorsDict["10"])):
            data.at[index, "Symmetry operator"] = 2
            Hamnosys_copy[index] = Hamnosys_copy[index][3:]
            continue

        # Search for symmetry operators that consists of 2 symbols, remove if found
        char = Hamnosys_copy[index][0:2]
        if char == SymmetryOperatorsDict["3"]:
            data.at[index, "Symmetry operator"] = 3
            Hamnosys_copy[index] = Hamnosys_copy[index][2:]
            continue
        elif char == SymmetryOperatorsDict["4"]:
            data.at[index, "Symmetry operator"] = 4
            Hamnosys_copy[index] = Hamnosys_copy[index][2:]
            continue
        elif char == SymmetryOperatorsDict["5"]:
            data.at[index, "Symmetry operator"] = 5
            Hamnosys_copy[index] = Hamnosys_copy[index][2:]
            continue
        elif char == SymmetryOperatorsDict["6"]:
            data.at[index, "Symmetry operator"] = 6
            Hamnosys_copy[index] = Hamnosys_copy[index][2:]
            continue

        # Search for symmetry operators that consists of 1 symbol, remove if found
        char = Hamnosys_copy[index][0]
        if char == SymmetryOperatorsDict["7"]:
            data.at[index, "Symmetry operator"] = 7
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            continue
        elif char == SymmetryOperatorsDict["8"]:
            data.at[index, "Symmetry operator"] = 8
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            continue
        # Check if non dominan hand is analyzed as only and set flag to 1 if true
        elif char == "":
            data.at[index, "Symmetry operator"] = 0
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            data.at[index, "NonDom first"] = 1
            continue

    # Log analysis result if logging is enabled
    if args.logging:
        for index, row in data.iterrows():
            print(
                str(index)
                + ": "
                + data.at[index, "Hamnosys"]
                + " -> "
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Symmetry operator"])
            )

    # Remove unknown signs - do it many times as you never know the order;
    for i in range(len(UnknownSymbols1Dict)):
        for index, row in data.iterrows():
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols1Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Handshape base form occurs always after the symmetry operator
    if args.logging:
        print("Dominant - Handshape - Baseform:")

    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBaseformsDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Baseform"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
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
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handshape - Baseform"])
            )

    if args.logging:
        print("Dominant - Handshape - Thumb position:")

    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Thumb position"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

    if args.logging:
        for index, row in data.iterrows():
            print(
                str(index)
                + ": "
                + data.at[index, "Hamnosys"]
                + " -> "
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handshape - Thumb position"])
            )

    if args.logging:
        print("Dominant - Handshape - Bending")

    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Bending"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

    # This code removes duplicated bendings
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

    if args.logging:
        for index, row in data.iterrows():
            print(
                str(index)
                + ": "
                + data.at[index, "Hamnosys"]
                + " -> "
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handshape - Bending"])
            )

    if args.logging:
        print("Dominant - Handshape - Thumb position - second try:")

    # For some entries thumb is placed after the bending sign,
    # so let's go back to thumb
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Thumb position"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

    if args.logging:
        for index, row in data.iterrows():
            print(
                str(index)
                + ": "
                + data.at[index, "Hamnosys"]
                + " -> "
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handshape - Thumb position"])
            )

    # Remove signs that may appear in this place
    # In most cases those are fingers with separate bending signs
    for index, row in data.iterrows():
        for i in range(len(UnknownSymbols1Dict)):
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols2Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Analyze second description of a dominant hand.
    # For example in notation 
    # Dominant hand is described as in beetween 
    # In this case  goes to the first description field,
    #  goes to the second one.
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "Dominant - Handshape - Baseform2"] = 99
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - Baseform2"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - Thumb position2"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - Bending2"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # for some entries thumb is placed after the bending sign,
            # so let's go back to thumb
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - Thumb position2"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # if base form was not found after "" announce an error
            if data.at[index, "Dominant - Handshape - Baseform2"] == 99:
                data.at[index, "ERROR"] = 2
            char = Hamnosys_copy[index][0]
            # Remove closing bracket if there
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Analyze non dominat hand description if placed here
    # For example in notation  dominant hand
    # is described as , and the nondominant hand is described as 
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "NONDominant - Handshape - Baseform"] = 99
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - Baseform"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - Thumb position"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - Bending"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # for some entries thumb is placed after the bending sign,
            # so let's go back to thumb
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - Thumb position"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # if base form was not found after "" announce an error
            if data.at[index, "NONDominant - Handshape - Baseform"] == 99:
                data.at[index, "ERROR"] = 3
            # Remove closing bracket if there
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Removing "" to be able to analyze examples like the one below
    # 
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Remove signs that may appear in beetwen
    # In most cases those are fingers with separate bending signs
    for index, row in data.iterrows():
        for i in range(len(UnknownSymbols1Dict)):
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols1Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in UnknownSymbols2Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    if args.logging:
        print("Dominant - Handposition - Extended finger direction:")

    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                            "Extended finger direction"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        if data.at[index, "Dominant - Handposition - "
                        "Extended finger direction"] == 99:
            data.at[index, "ERROR"] = 4

    # If there are two in a row
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                            "Extended finger direction2"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # take care of two in a row with "" sign (two for dominant)
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "":
            if data.at[index, "Dominant - Handposition - "
                            "Extended finger direction2"] != 0:
                data.at[index, "ERROR"] = 5
            data.at[index, "Dominant - Handposition - "
                        "Extended finger direction2"] = 99
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                            "Extended finger direction2"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        if data.at[index, "Dominant - Handposition - "
                        "Extended finger direction2"] == 99:
            data.at[index, "ERROR"] = 6

    # take care of nondominant hand
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "NONDominant - Handposition - "
                        "Extended finger direction"] = 99
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "NONDominant - Handposition - "
                            "Extended finger direction"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
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
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handposition - "
                                    "Extended finger direction"])
            )

    # Remove unnecesairy bracket or some strange dots
    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        if char == "" or char == "" or char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    if args.logging:
        print("Dominant - Handposition - Palm orientation:")

    for index, row in data.iterrows():
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionPalmOrientationDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                            "Palm orientation"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # take care of two in a row with "" sign (two for dominant)
    for index, row in data.iterrows():
        if len(Hamnosys_copy[index]) == 0:
            break
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "NONDominant - Handposition - palm orientation"] = 99
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
        for key, value in HandpositionPalmOrientationDict.items():
            if char == value:
                data.at[index, "NONDominant - Handposition - "
                            "palm orientation"] = key
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        if data.at[index, "NONDominant - Handposition - Palm orientation"] == 99:
            data.at[index, "ERROR"] = 7

    if args.logging:
        for index, row in data.iterrows():
            print(
                str(index)
                + ": "
                + data.at[index, "Hamnosys"]
                + " -> "
                + Hamnosys_copy[index]
                + " = "
                + str(data.at[index, "Dominant - Handposition - "
                                    "Extended finger direction"])
            )

    # Remove unknown signs
    for i in range(5):
        for index, row in data.iterrows():
            if len(Hamnosys_copy[index]) == 0:
                break
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols3Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in UnknownSymbols4Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Check if handposition left symbol is placed here
    for index, row in data.iterrows():
        if len(Hamnosys_copy[index]) == 0:
            break
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "Dominant - Handposition - LR"] = 1
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        elif char == "":
            data.at[index, "Dominant - Handposition - LR"] = 2
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # Removing some signs.."
    for i in range(10):
        for index, row in data.iterrows():
            if len(Hamnosys_copy[index]) == 0:
                break
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols3Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    if args.logging:
        print("Hand location - fronal plane t/b")

    # check 4 next signs searching for Handlocation Frontal Plane Top/bottom
    for index, row in data.iterrows():
        if len(Hamnosys_copy[index]) == 0:
            break
        for i in range(4):
            char = Hamnosys_copy[index][i]
            for key, value in HandLocationFronalPlaneTB.items():
                if char == value:
                    data.at[index, "Dominant - Handposition - TB"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
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
        if len(Hamnosys_copy[index]) == 0:
            break
        char = Hamnosys_copy[index][0]
        if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 99:
            if char == "":
                data.at[index, "Dominant - Handposition - LR"] = "3"
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if char == "":
                data.at[index, "Dominant - Handposition - LR"] = "4"
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

    # check 4 next signs searching for distance
    for index, row in data.iterrows():
        if len(Hamnosys_copy[index]) == 0:
            break
        for i in range(4):
            char = Hamnosys_copy[index][i]
            for key, value in HandLocationDistanceDict.items():
                if char == value:
                    data.at[index, "Dominant - Handposition - Distance"] = key
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                    break
            if pd.to_numeric(data.at[index, "Dominant - Handposition - "
                                            "Distance"]) != 3:
                break
            for key, value in MovementSigns.items():
                if char == value:
                    data.at[index, "Dominant - Handposition - Distance"] = 0
                    break
            if char == "":
                data.at[index, "Dominant - Handposition - Distance"] = 0
                break
            if pd.to_numeric(data.at[index, "Dominant - Handposition - TB"]) != 3:
                break

    # Save resultant file
    df = data[args.columnnamesout]
    df.to_csv(args.dstfilename, sep=" ", header=True)


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)
