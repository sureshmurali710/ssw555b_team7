"""
#===========================================================================================#
Subject         : SSW -555(Agile Methods for Software Development) 
Assignment      : P02: Practice programming with GEDCOM data 
Script Author   : Team#7
Date            : 02/14/2021
Script Name     : SSW555-Porject.py
#===========================================================================================#

Purpose:
--------
Create a small GEDCOM file to use in testing your program.
You may reuse the file you submitted for assignment Project 01 or create a new one.
Make sure that it includes a NOTE record at the beginning with your name.

Write a short program that:

Reads each line of a GEDCOM file

Prints "--> <input line>"

Prints "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
<level> is the level of the input line, e.g. 0, 1, 2
<tag> is the tag associated with the line, e.g. 'INDI', 'FAM', 'DATE', ...
<valid?> has the value 'Y' if the tag is one of the supported tags or 'N' otherwise.
  The set of all valid tags for our project is specified in the Project Overview document.
<arguments> is the rest of the line beyond the level and tag.
---------------------------------------------------------------------------------------------


"""

"""Sample input:

0 NOTE dates after now
1 SOUR Family Echo
2 WWW http://www.familyecho.com  (Links to an external site.)
0 bi00 INDI
1 NAME Jimmy /Conners/
Sample output:

--> 0 NOTE dates after now
<-- 0|NOTE|Y|dates after now
--> 1 SOUR Family Echo
<-- 1|SOUR|N|Family Echo
--> 2 WWW http://www.familyecho.com (Links to an external site.) (Links to an external site.)
<-- 2|WWW|N|http://www.familyecho.com (Links to an external site.)
--> 0 bi00 INDI
<-- 0|INDI|Y|bi00
--> 1 NAME Jimmy /Conners/
<-- 1|NAME|Y|Jimmy /Conners/
"""

import sys

# welcome Message
print('welcome to P02 Python Assignment\n')

# purpose
print('Practice programming with GEDCOM data\n')

print('Enter file name with extension when prompted  e.g : test.ged \n')

# Dictionary  from Project file
Tag_Level = {
    'INDI': 0,
    'NAME': 1,
    'SEX': 1,
    'BIRT': 1,
    'DEAT': 1,
    'FAMC': 1,
    'FAMS': 1,
    'FAM': 0,
    'MARR': 1,
    'HUSB': 1,
    'WIFE': 1,
    'CHIL': 1,
    'DIV': 1,
    'DATE': 2,
    'HEAD': 0,
    'TRLR': 0,
    'NOTE': 0}
from prettytable import PrettyTable

ID = []
Name = []
Fam = []
Hus = []
Wif = []
Ind = PrettyTable(["ID", "NAME"])
Family = PrettyTable(["ID", "Husband Name", "Wife Name"])

def data_match(splitline):
    data_found = False
    index = 1  # default value
    for key, val in Tag_Level.items():
        if key in splitline:
            index = splitline.index(key)
        if key == splitline[index] and val == int(splitline[0]):
            data_found = True
            break
    return data_found, index


def find_str(fhand):
    """
    To extract the valve and update the variable value only if more than 2 parameters are there to check with the provided dict
    """
    global ID, Name, Ind, Fam, Hus, Wif
    ind_list = []
    temp=[]
    for line in fhand:
        # arguments = '' #default
        line = line.strip()  # Return a copy of the sequence with specified leading and trailing bytes removed (spaces)
        if len(line) > 1:  # ignored any data without 2 parameters.
            splitline = line.split(' ', 2)
            found, index = data_match(splitline)
            if index != 1:  # swapping 2 and 3 index if the tag is present in 3 element
                splitline[1], splitline[2] = splitline[2], splitline[1]

            if splitline[0] == '0' and splitline[1] == 'INDI':
                if splitline[2] not in ID:
                    splitline[2] = splitline[2].replace("@", "")
                    ID.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'NAME':
                if splitline[2] not in Name:
                    Name.append(splitline[2])

            if splitline[0] == '0' and splitline[1] == 'FAM':
                if splitline[2] not in Fam:
                    Fam.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'HUSB':
                if splitline[2] not in Hus:
                    Hus.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'WIFE':
                if splitline[2] not in Wif:
                    Wif.append(splitline[2])

    for i, n in zip(ID, Name):
        Ind.add_row([i, n])
        ind_list.append((i, n))
    Ind.sortby = 'ID'
    print(Ind)

    for f, h, w in zip(Fam, Hus, Wif):

        hus_name = f.ind_list[Hus]
        print("hus_name = ", hus_name)
        #Ind.add_row([i, n])
        #fam_list.append((i, n))


fname = input('Enter the file name: ')
try:
    fhand = open(fname)  # open File
    sys.stdout = open('OutputFile.txt', 'w')

    find_str(fhand)
    fhand.close()  # Close the file
except:
    print('File cannot be opened:', fname)
    sys.exit()

