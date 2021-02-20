# Jonathan Sebast, SSW555, February 13, 2021

import sys


def process_level(level_value):
    success = False
    if level_value == "0" or level_value == "1" or level_value == "2":
        success = True
    return success

def check_tag(input_level, input_tag):
    success = False
    valid_tags = {
        "INDI": "0",
        "FAM": "0",
        "HEAD": "0",
        "TRLR": "0",
        "NOTE": "0",
        "NAME": "1",
        "SEX": "1",
        "BIRT": "1",
        "DEAT": "1",
        "FAMC": "1",
        "FAMS": "1",
        "MARR": "1",
        "HUSB": "1",
        "WIFE": "1",
        "CHIL": "1",
        "DIV": "1",
        "DATE": "2"
    }
    if input_tag in valid_tags and valid_tags[input_tag] == input_level:
        success = True
    return success


arguments = len(sys.argv)
if arguments == 1:
    print("Please provide the filename")
elif arguments > 2:
    print("Provide just the filename, with quotes if it includes spaces")
else:
    inputFile = open(sys.argv[1], "r")
    try:
        for line in inputFile:
            validTag = True
            level = 0
            tag = ""
            arguments = ""

            # Reading a text file, just get rid of the end of line characters
            line = line.replace("\r", "")
            line = line.replace("\n", "")

            # Output the original text
            print(f"--> {line}")

            lineElements = line.split(" ")
            if process_level(lineElements[0]):
                level = lineElements[0]
                numElements = len(lineElements)
                if (numElements > 2 and lineElements[0] == "0" and
                        (lineElements[2] == "INDI" or lineElements[2] == "FAM")):
                    tag = lineElements[2]
                    arguments = lineElements[1]
                    # Tag is known to be valid, since we checked it in the IF statement -
                    # no validTag = false case needed here.
                else:
                    tag = lineElements[1]
                    validTag = check_tag(level, tag)
                    for i in range(2, numElements):
                        # This prints a trailing space if there are arguments.  I'm not
                        # aware of anything that would detect and have issues with this.
                        arguments = arguments + lineElements[i] + " "
            else:
                validTag = False

            # Create the output text
            if validTag:
                validChar = "Y"
            else:
                validChar = "N"
            processedText = "<-- " + level + "|" + tag + "|" + validChar + "|" + arguments
            print(processedText)
    finally:
        inputFile.close()
