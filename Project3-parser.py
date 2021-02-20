"""
Authors: Team 7
Description:This program is written to save information about individuals and families in lists (or collections) and display them in pretty table.
"""
import gedcom
import datetime
from prettytable import PrettyTable

parsed = gedcom.parse('team7.ged')

## Parse the gedcom file and store data in the list
individual = list(parsed.individuals)
today = datetime.datetime.now()
individualTable = PrettyTable()

## Set the table headers/columns for individuals and families
individualTable.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
familyTable = PrettyTable()
familyTable.field_names = ['ID','Married','Divorced','Husband_ID','Husband Name', 'Wife Id', 'Wife Name', 'Children']
md = []

print('\n ----------------------------------------------------------------------\n  Person list   \n ----------------------------------------------------------------------')
for i in range(len(individual)):
    lstdata = individual[i]
    person = {}
    fname, lname = lstdata.name
    person['id'] = lstdata.id
    person['name'] = fname +' '+ lname
    person['gender'] = lstdata.gender
    person['birthdate'] = lstdata.birth.date
    birthDate = datetime.datetime.strptime(lstdata.birth.date,'%d %b %Y')

    if lstdata.__contains__('DEAT'):
        person['alive'] = 'NA'
        deathDate = lstdata.__getitem__('DEAT')
        person['deathdate'] = deathDate.value
    else:
        person['deathdate'] = 'NA'
        person['alive'] = 'Y'

    if lstdata.__contains__('DEAT'):
        person['age'] = (datetime.datetime.strptime(lstdata.death.date,'%d %b %Y') - datetime.datetime.strptime(lstdata.birth.date,'%d %b %Y')).days/365
    else:
        person['age'] = round(((today - birthDate).days/365),1)

    if lstdata.__contains__('FAMS'):
        spouses = lstdata.__getitem__('FAMS')
        if isinstance(spouses, gedcom.Element):
            person['spouses'] = spouses.value
        else:
            spouses_id = []
            for i in range(len(spouses)):
                spouses_id.insert(i,spouses[i].value)
            person['spouses'] = spouses_id
    else:
        person['spouses'] = 'NA'

    if lstdata.__contains__('FAMC'):
        child = lstdata.__getitem__('FAMC')
        if isinstance(child, gedcom.Element):
            person['child'] = child.value
        else:
            child_id = []
            for i in range(len(child)):
                child_id.append(child[i].value)
            person['child'] = child_id
    else:
        person['child'] = 'NA'

    dictlist = [person['id'],person['name'],person['gender'],person['birthdate'],round(person['age'],2),person['alive'],person['deathdate'],person['child'],person['spouses']]
    individualTable.add_row(dictlist)
    print(person)

fa = list(parsed.families)
print('\n ----------------------------------------------------------------------\n  Family list   \n ----------------------------------------------------------------------')
for i in range(len(fa)):
    f = fa[i]
    family = {}
    family['Family_id'] = f.id
    if f.__contains__('DIV'):
        divorce = f.__getitem__('DIV').__getitem__('DATE').value
        family['divorce'] = divorce
    else:
        family['divorce'] = 'NA'

    if f.__contains__('CHIL'):
        child = f.__getitem__('CHIL')
        if isinstance(child, gedcom.Element):
            family['child'] = child.value
        else:
            child_id = []
            for i in range(len(child)):
                child_id.append(child[i].value)
            family['child'] = child_id
    else:
        family['child'] = 'NA'
    
    if f.__contains__('MARR'):
        md = (f.__getitem__('MARR')).date
    else:
        family['marriage'] = 'NA'

    family['husband_id'] = f.partners[0].value
    family['husband_name'] = ' '.join(f.get_by_id(f.partners[0].value).name)
    family['wife_id'] = f.partners[1].value
    family['wife_name'] = ' '.join(f.get_by_id(f.partners[1].value).name)
    family['marriage'] = md

    dictlist2 = [family['Family_id'],family['marriage'],family['divorce'],family['husband_id'],family['husband_name'],family['wife_id'],family['wife_name'],family['child']]
    familyTable.add_row(dictlist2)
    print(family)

print('\n ----------------------------------------------------------------------\n  Individuals   \n ----------------------------------------------------------------------')
print(individualTable)

print('\n ----------------------------------------------------------------------\n    Families     \n ----------------------------------------------------------------------')
print(familyTable)
