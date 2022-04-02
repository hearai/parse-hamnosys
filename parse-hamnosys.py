from argparse import ArgumentParser
from hamnosys_dicts import HandLocationFronalPlaneTB, HandshapeBaseformsDict, \
                           HandshapeBendingDict, \
                           HandpositionFingerDirectionDict, \
                           HandpositionPalmOrientationDict, \
                           HandshapeThumbPositionDict, \
                           HandLocationDistanceDict, MovementSigns, \
                           SymmetryOperatorsDict, UnknownSymbols1Dict, \
                           UnknownSymbols2Dict, UnknownSymbols3Dict

import pandas as pd
import numpy as np


def equal_to_nan(a):
    # TBD remove not needed logic
    return ((a == np.NaN) | (np.isnan(a) & np.isnan(np.NaN))).all()


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
        # metavar="log",
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
        default=["Name", "Start", "End",
                 "Symmetry operator",
                 "NonDom first",
                 "Dominant - Handshape - Baseform",
                 "Dominant - Handshape - Thumb position",
                 "Dominant - Handshape - Bending",
                 "Dominant - Handposition - Extended finger direction",
                 "Dominant - Handposition - Palm orientation",
                 "Dominant - Handshape - Baseform2",
                 "Dominant - Handshape - Thumb position2",
                 "Dominant - Handshape - Bending2",
                 "Dominant - Handposition - Extended finger direction2",
                 "Dominant - Handposition - Palm orientation2",
                 "NONDominant - Handshape - Baseform",
                 "NONDominant - Handshape - Thumb position",
                 "NONDominant - Handshape - Bending",
                 "NONDominant - Handposition - Extended finger direction",
                 "NONDominant - Handposition - Palm orientation",
                 "NONDominant - Handshape - Baseform2",
                 "NONDominant - Handshape - Thumb position2",
                 "NONDominant - Handshape - Bending2",
                 "NONDominant - Handposition - Extended finger direction2",
                 "NONDominant - Handposition - Palm orientation2",
                 "Handposition - LR",
                 "Handposition - TB",
                 "Handposition - Distance"],
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

    # Prepare a columns for results and fill them with NaNs (not set).
    data = data.reindex(columns=[
        *data.columns,
        "NonDom first",
        "Symmetry operator",
        "Dominant - Handshape - Baseform",
        "Dominant - Handshape - Thumb position",
        "Dominant - Handshape - Bending",
        "Dominant - Handposition - Extended finger direction",
        "Dominant - Handposition - Palm orientation",
        "Dominant - Handshape - Baseform2",
        "Dominant - Handshape - Thumb position2",
        "Dominant - Handshape - Bending2",
        "Dominant - Handposition - Extended finger direction2",
        "Dominant - Handposition - Palm orientation2",
        "NONDominant - Handshape - Baseform",
        "NONDominant - Handshape - Thumb position",
        "NONDominant - Handshape - Bending",
        "NONDominant - Handposition - Extended finger direction",
        "NONDominant - Handposition - Palm orientation",
        "NONDominant - Handshape - Baseform2",
        "NONDominant - Handshape - Thumb position2",
        "NONDominant - Handshape - Bending2",
        "NONDominant - Handposition - Extended finger direction2",
        "NONDominant - Handposition - Palm orientation2",
        "Handposition - LR",
        "Handposition - TB",
        "Handposition - Distance"],
        fill_value=np.NaN)

    # Change default values for columns where 0 means None
    data["NonDom first"] = 0
    data["Symmetry operator"] = 0
    data["Dominant - Handshape - Thumb position"] = 0
    data["Dominant - Handshape - Bending"] = 0
    data["Handposition - Distance"] = 0

    for index, _ in data.iterrows():
        print(index)
        # Search for symmetry operators that consists of from 3 to 1 symbol,
        # remove if found
        for i in range(1, 10):
            j = 3 if i < 3 else (2 if i < 7 else 1)
            char = Hamnosys_copy[index][0:j]
            if set(char) == set(SymmetryOperatorsDict[str(i)]):
                data.at[index, "Symmetry operator"] = i % 9
                if i % 9 == 0:
                    data.at[index, "NonDom first"] = 1
                Hamnosys_copy[index] = Hamnosys_copy[index][j:]
                continue

        # Remove bracket and vave shape (that describes the movement)
        for i in range(len(UnknownSymbols1Dict)):
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols1Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Dominant hand base form is expected here,
        # so we iter trough all possible options
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBaseformsDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Baseform"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue
        # If base form was not found here, the logic is broken
        # mark it by assigning -1 to the field
        if equal_to_nan(data.at[index, "Dominant - Handshape - Baseform"]):
            data.at[index, "Dominant - Handshape - Baseform"] = -1

        # Analyze thumb position - if not found
        # "None" is assigned by default
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index,
                        "Dominant - Handshape - Thumb position"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

        # Analyze bending - if not found
        # "None" is assigned by default
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                data.at[index, "Dominant - Handshape - Bending"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

        # This code removes duplicated bendings
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeBendingDict.items():
            if char == value:
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

        # For some entries thumb is placed after the bending sign,
        # so let's go back to thumb
        char = Hamnosys_copy[index][0]
        for key, value in HandshapeThumbPositionDict.items():
            if char == value:
                data.at[index,
                        "Dominant - Handshape - Thumb position"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                continue

        # Remove signs that may appear in this place
        # In most cases those are fingers with separate bending signs
        for i in range(len(UnknownSymbols1Dict)):
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols2Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Analyze second description of a dominant hand.
        # For example in notation 
        # Dominant hand is described as in beetween 
        # In this case  goes to the first description field,
        #  goes to the second one.
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index,
                            "Dominant - Handshape - Baseform2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # If handshape base form was not found after '\'
            # the logic is broken
            if equal_to_nan(data.at[index, "Dominant - Handshape - "
                                           "Baseform2"]):
                data.at[index, "Dominant - Handshape - Baseform2"] = -1
                continue
            # Set thumb and bending to 0 (None)
            data.at[index, "Dominant - Handshape - Thumb position2"] = 0
            data.at[index, "Dominant - Handshape - Bending2"] = 0
            char = Hamnosys_copy[index][0]
            # Search for the thumb, if not found remain unchanged value
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - "
                                   "Thumb position2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # Search for the bending, if not found remain unchanged value
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index,
                            "Dominant - Handshape - Bending2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # For some entries thumb is placed after the bending sign,
            # so let's go back to thumb
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "Dominant - Handshape - "
                                   "Thumb position2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # Remove closing bracket if there
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Analyze non dominat hand description if placed here
        # For example in notation  dominant hand
        # is described as , and the nondominant hand is described as 
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Baseform"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # If handshape base form was not found after ''
            # the logic is broken
            if equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                           "Baseform"]):
                data.at[index, "NONDominant - Handshape - Baseform"] = -1
                continue
            # Set thumb and bending to 0 (None)
            data.at[index, "NONDominant - Handshape - Thumb position"] = 0
            data.at[index, "NONDominant - Handshape - Bending"] = 0
            char = Hamnosys_copy[index][0]
            # Search for the thumb, if not found remain unchanged value
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # Search for the palm, if not found remain unchanged value
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Bending"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # For some entries thumb is placed after the bending sign,
            # so let's go back to thumb
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # Remove closing bracket if there
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Analyze second description of a NONDominant hand.
        # For example in notation 
        # Dominant hand is described as in beetween 
        # In this case  goes to the first description field,
        #  goes to the second one.
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Baseform2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # If handshape base form was not found after '\'
            # the logic is broken
            if equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                           "Baseform2"]):
                data.at[index, "NONDominant - Handshape - Baseform2"] = -1
                continue
            # Set thumb and bending to 0 (None)
            data.at[index, "NONDominant - Handshape - Thumb position2"] = 0
            data.at[index, "NONDominant - Handshape - Bending2"] = 0
            char = Hamnosys_copy[index][0]
            # Search for the thumb, if not found remain unchanged value
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # Search for the bending, if not found remain unchanged value
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Bending2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # For some entries thumb is placed after the bending sign,
            # so let's go back to thumb
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Remove signs that may appear in beetwen
        # In most cases those are fingers with separate bending signs
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

        # Extended finger direction
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                               "Extended finger direction"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        if equal_to_nan(data.at[index, "Dominant - Handposition - "
                                       "Extended finger direction"]):
            data.at[index, "Dominant - Handposition - "
                           "Extended finger direction"] = -1

        # Extended finger direction - If there are two in a row
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                               "Extended finger direction2"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Extended finger direction - Take care of two in a row with
        # "" sign (two for dominant)
        char = Hamnosys_copy[index][0]
        if char == "":
            if not(equal_to_nan(data.at[index, "Dominant - Handposition - "
                                               "Extended finger direction2"])):
                data.at[index, "Dominant - Handposition - "
                               "Extended finger direction2"] = -1
                continue
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionFingerDirectionDict.items():
                if char == value:
                    data.at[index, "Dominant - Handposition - "
                                   "Extended finger direction2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "Dominant - Handposition - "
                                           "Extended finger direction2"]):
                data.at[index, "Dominant - Handposition - "
                               "Extended finger direction2"] = -1

        # Extended finger direction - Take care of nondominant hand
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionFingerDirectionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                           "Extended finger direction"]):
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction"] = -1

        # Extended finger direction - If there are two in a row
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionFingerDirectionDict.items():
            if char == value:
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction2"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Extended finger direction - take care of two in a row with
        # "" sign (two for dominant)
        char = Hamnosys_copy[index][0]
        if char == "":
            if not(equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                               "Extended finger direction2"])):
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction2"] = -1
                continue
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionFingerDirectionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                           "Extended finger direction2"]):
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction2"] = -1

        # Remove unnecesairy bracket or a vave sign
        char = Hamnosys_copy[index][0]
        if char == "" or char == "" or char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Palm orientation
        char = Hamnosys_copy[index][0]
        for key, value in HandpositionPalmOrientationDict.items():
            if char == value:
                data.at[index, "Dominant - Handposition - "
                               "Palm orientation"] = int(key)
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        if equal_to_nan(data.at[index, "Dominant - Handposition - "
                                       "Palm orientation"]):
            data.at[index, "Dominant - Handposition - Palm orientation"] = -1

        # Palm orientation - Take care of two in a row with
        # "" sign (two for dominant)
        if len(Hamnosys_copy[index]) == 0:
            continue
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionPalmOrientationDict.items():
                if char == value:
                    data.at[index, "Dominant - Handposition - "
                                   "Palm orientation2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "Dominant - Handposition - "
                                           "Palm orientation2"]):
                data.at[index, "Dominant - Handposition - "
                               "Palm orientation2"] = -1

        # Remove unknown signs
        for i in range(5):
            if len(Hamnosys_copy[index]) == 0:
                continue
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols3Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Analyze NonDominant Hand if placed here
        char = Hamnosys_copy[index][0]
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # Check if this field was detected before and assign -1 if true
            if not(equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                               "Baseform"])):
                data.at[index, "NONDominant - Handshape - Baseform"] = -1
                continue
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBaseformsDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Baseform"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            #Hashape base for doesn have to be found, see:
            # 
            if not(equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                               "Thumb position"])):
                data.at[index, "NONDominant - Handshape - Thumb position"] = -1
                continue
            data.at[index, "NONDominant - Handshape - Thumb position"] = 0
            data.at[index, "NONDominant - Handshape - Bending"] = 0
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    data.at[index,
                            "NONDominant - Handshape - Bending"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in HandshapeThumbPositionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handshape - "
                                   "Thumb position"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            # Analyze second option
            if char == "":
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                if not(equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                                   "Baseform2"])):
                    data.at[index, "NONDominant - Handshape - Baseform2"] = -1
                    continue
                char = Hamnosys_copy[index][0]
                for key, value in HandshapeBaseformsDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handshape - "
                                       "Baseform2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                if equal_to_nan(data.at[index, "NONDominant - Handshape - "
                                               "Baseform2"]):
                    data.at[index, "NONDominant - Handshape - Baseform2"] = -1
                    continue
                data.at[index, "NONDominant - Handshape - Thumb position2"] = 0
                data.at[index, "NONDominant - Handshape - Bending2"] = 0
                char = Hamnosys_copy[index][0]
                for key, value in HandshapeThumbPositionDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handshape - "
                                       "Thumb position2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                char = Hamnosys_copy[index][0]
                for key, value in HandshapeBendingDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handshape - "
                                       "Bending2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                # for some entries thumb is placed after the bending sign,
                # so let's go back to thumb
                char = Hamnosys_copy[index][0]
                for key, value in HandshapeThumbPositionDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handshape - "
                                       "Thumb position2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                # Remove closing bracket if there
                if char == "":
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols2Dict.items():
                if char==value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                    char = Hamnosys_copy[index][0]
                if int(key) > 5:
                    break
            # Extended finger direction
            if not(equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                               "Extended finger direction"])):
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction"] = -1
                continue
            for key, value in HandpositionFingerDirectionDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                           "Extended finger direction"]):
                data.at[index, "NONDominant - Handposition - "
                               "Extended finger direction"] = -1
                continue

            # Extended finger direction - If there are two in a row
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionFingerDirectionDict.items():
                if char == value:
                    if not(equal_to_nan(data.at[index, "NONDominant - "
                                                       "Handposition - "
                                                       "Extended finger "
                                                       "direction2"])):
                        data.at[index, "NONDominant - Handposition - "
                                       "Extended finger direction2"] = -1
                        break
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # Extended finger direction -
            # take care of two in a row with "" sign
            char = Hamnosys_copy[index][0]
            if char == "":
                # Check if this field was detected before
                # and assign -1 if true
                if not(equal_to_nan(data.at[index, "NONDominant - "
                                                   "Handposition - "
                                                   "Extended finger "
                                                   "direction2"])):
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction2"] = -1
                    continue
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                char = Hamnosys_copy[index][0]
                for key, value in HandpositionFingerDirectionDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handposition - "
                                       "Extended finger direction2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                               "Extended finger direction2"]):
                    data.at[index, "NONDominant - Handposition - "
                                   "Extended finger direction2"] = -1
            # Palm orientation
            # Check if this field was detected before and assign -1 if true
            if not(equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                               "Palm orientation"])):
                data.at[index, "NONDominant - Handposition - "
                               "Palm orientation"] = -1
                continue
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionPalmOrientationDict.items():
                if char == value:
                    data.at[index, "NONDominant - Handposition - "
                                   "Palm orientation"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                           "Palm orientation"]):
                data.at[index, "NONDominant - Handposition - "
                               "Palm orientation"] = -1
                continue
            # Palm orientation - If there are two in a row
            char = Hamnosys_copy[index][0]
            for key, value in HandpositionPalmOrientationDict.items():
                if char == value:
                    # Check if this field was detected before
                    # and assign -1 if true
                    if not(equal_to_nan(data.at[index, "NONDominant - "
                                                       "Handposition - "
                                                       "Palm orientation2"])):
                        data.at[index, "NONDominant - Handposition - "
                                       "Palm orientation2"] = -1
                        break
                    data.at[index, "NONDominant - Handposition - "
                                   "Palm orientation2"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            # Palm orientation - take care of two in a row with "" sign
            char = Hamnosys_copy[index][0]
            if char == "":
                # Check if this field was detected before
                # and assign -1 if true
                if not(equal_to_nan(data.at[index, "NONDominant - "
                                                   "Handposition - "
                                                   "Palm orientation2"])):
                    data.at[index, "NONDominant - Handposition - "
                                   "Palm orientation2"] = -1
                    continue
                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                char = Hamnosys_copy[index][0]
                for key, value in HandpositionPalmOrientationDict.items():
                    if char == value:
                        data.at[index, "NONDominant - Handposition - "
                                       "Palm orientation2"] = int(key)
                        Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                if equal_to_nan(data.at[index, "NONDominant - Handposition - "
                                               "Palm orientation2"]):
                    data.at[index, "NONDominant - Handposition - "
                                   "Palm orientation2"] = -1

        # Remove closing bracket if there
        if char == "":
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        # Removing some signs.."
        for i in range(10):
            if len(Hamnosys_copy[index]) == 0:
                continue
            char = Hamnosys_copy[index][0]
            for key, value in UnknownSymbols3Dict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
            for key, value in HandshapeBendingDict.items():
                if char == value:
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Check if handposition left symbol is placed here
        if len(Hamnosys_copy[index]) == 0:
            continue
        char = Hamnosys_copy[index][0]
        if char == "":
            data.at[index, "Handposition - LR"] = 1
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
        elif char == "":
            data.at[index, "Handposition - LR"] = 2
            Hamnosys_copy[index] = Hamnosys_copy[index][1:]

        # Check 4 next signs searching
        # for Handlocation Frontal Plane Top/bottom
        if len(Hamnosys_copy[index]) == 0:
            continue
        loops = 4
        if len(Hamnosys_copy[index]) < loops:
            loops = len(Hamnosys_copy[index])
        for i in range(loops):
            char = Hamnosys_copy[index][i]
            for key, value in HandLocationFronalPlaneTB.items():
                if char == value:
                    data.at[index, "Handposition - TB"] = int(key)
                    if equal_to_nan(data.at[index, "Handposition - LR"]):
                        char = Hamnosys_copy[index][i-1]
                        if char == "":
                            data.at[index, "Handposition - LR"] = 1
                            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                        elif char == "":
                            data.at[index, "Handposition - LR"] = 2
                            Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                        if len(Hamnosys_copy[index]) > i+1:
                            char = Hamnosys_copy[index][i+1]
                            if char == "":
                                data.at[index, "Handposition - LR"] = 3
                                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                            elif char == "":
                                data.at[index, "Handposition - LR"] = 4
                                Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                    break

            if not(equal_to_nan(pd.to_numeric(
                            data.at[index, "Handposition - TB"]))):
                break
            for key, value in MovementSigns.items():
                if char == value:
                    data.at[index, "Handposition - TB"] = 14
                    break
            if char == "":
                data.at[index, "Handposition - TB"] = 14
                break
            if not(equal_to_nan(pd.to_numeric(
                            data.at[index, "Handposition - TB"]))):
                break
        if equal_to_nan(pd.to_numeric(
                            data.at[index, "Handposition - TB"])):
            data.at[index, "Handposition - TB"] == 14

        if len(Hamnosys_copy[index]) == 0:
            continue
        char = Hamnosys_copy[index][0]
        if equal_to_nan(pd.to_numeric(
                            data.at[index, "Handposition - LR"])):
            data.at[index, "Handposition - LR"] = 0

        # check 4 next signs searching for distance
        loops = 4
        if loops > len(Hamnosys_copy[index]):
            loops = len(Hamnosys_copy[index])
        for i in range(loops):
            char = Hamnosys_copy[index][i]
            val_assigned = 0
            for key, value in HandLocationDistanceDict.items():
                if char == value:
                    data.at[index,
                            "Handposition - Distance"] = int(key)
                    Hamnosys_copy[index] = Hamnosys_copy[index][1:]
                    val_assigned = 1
                    break
            for key, value in MovementSigns.items():
                if char == value:
                    data.at[index, "Handposition - Distance"] = 0
                    val_assigned = 1
                    break
            if char == "":
                data.at[index, "Handposition - Distance"] = 0
                val_assigned = 1
                break
            if val_assigned == 1:
                break

    # Save resultant file
    df = data[args.columnnamesout]
    df.to_csv(args.dstfilename,
              sep=" ",
              header=True,
              index=False,
              na_rep='NaN')


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)
