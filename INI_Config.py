import ConfigParser
import json

FileName = 'noname'
INI = ConfigParser.RawConfigParser()

def OpenFile(filename):
    global FileName ,INI
    FileName = filename
    INI.read(filename)

def FlashFile():
    global FileName, INI
    with open(FileName, 'wb') as Inifile:
        INI.write(Inifile)
    INI.read(FileName)



def IsSection(SectionName):
    global INI
    return INI.has_section(SectionName)

def AddSection(SectionName):
    global INI
    if (INI.has_section(SectionName)):
        return 0
    else :
        return INI.add_section(SectionName)

def DelSection(SectionName):
    global INI
    if (INI.has_section(SectionName)):
        return INI.remove_section(SectionName)



def IsOption(SectionName,Option):
    global INI
    return INI.has_option(SectionName,Option)


def SetData(SectionName,Option,val):
    global INI
    if (INI.has_section(SectionName)):
        INI.set(SectionName, Option, val)
    else:
        INI.add_section(SectionName)
        INI.set(SectionName, Option, val)

def GetData(SectionName,Option):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName,Option)):
            return INI.get(SectionName, Option)

def DelData(SectionName,Option):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName, Option)):
            INI.remove_option(SectionName, Option)


def GetList(SectionName,ListName):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName, ListName)):
            return json.loads( INI.get(SectionName, ListName))


def GetSectionS():
    global INI
    return INI.sections()

def GetOptionS(SectionName):
    global INI
    return INI.options(SectionName)

def GetItemS(SectionName):
    global INI
    return INI.items(SectionName)

def GetDataInt(SectionName,Option):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName, Option)):
            return INI.getint(SectionName, Option)

def GetDatafloat(SectionName,Option):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName, Option)):
            return INI.getfloat(SectionName, Option)

def GetDataBool(SectionName,Option):
    global INI
    if (INI.has_section(SectionName)):
        if (INI.has_option(SectionName, Option)):
            return INI.getboolean(SectionName, Option)

"""
OpenFile('example.cfg')
SEC = 'Section1'
print GetItemS(SEC)
"""