#!/usr/bin/python

import os, sys, ntpath, shutil, calendar, datetime, re

class Magazine:
    'Common base class for magazine'

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(filepath)
        self.name = self.filename('/')[-1].split('.')[0]
        
class Organiser:

    ''' Recursive scanning of a directory for files of a given type
        SourceDir string Root directory to scan
        FileType string Type of file to scan for e.g. 'pdf'
        Recursive bool Will scan subdirs if == 1
        Returns array List of files
    '''
    @staticmethod
    def ScanDirectory(SourceDir, FileType, Recursive=0):
        dirs = os.listdir(SourceDir)
        files = []
        for file in dirs:
            if os.path.isdir(SourceDir + "\\" + file) and Recursive == 1:
                moreFiles = Organiser.ScanDirectory(SourceDir + "\\" + file,FileType,Recursive)
                if moreFiles:
                    for fileFromSubDir in moreFiles:
                        files.append(fileFromSubDir)
            if file.endswith(FileType):
                #os.system('cls')
                #print "Found..." + SourceDir + "\\" + file
                files.append(SourceDir + "\\" + file)
        return files    

    def CurrentNames(magazineDir):
        magazineNames = []
        for file in os.listdir(magazinesDir):
            if os.path.isdir(file): pass
            else: magazineNames.append(file)
        return magazineNames

    #def MoveRecognisedMagazines(filePaths, magazineDir):

    @staticmethod
    def NameFromFilepath(filepath):
        name = os.path.basename(filepath)
        name = os.path.splitext(name)[0]
        name = name.replace("_", " ")
        return name

    @staticmethod
    def FormatDate(YYYY='', MM='', DD=''):
        if MM:
            MM = '-' + format(int(MM), '02d')
        if DD:
            DD = '-' + format(int(DD), '02d')
        return str(YYYY) + str(MM) + str(DD)

    @staticmethod
    def IsValidYear(YYYY):
        YYYY = int(YYYY)
        now = datetime.datetime.now()
        thisYear =  now.year
        nextYear = thisYear + 1
        if YYYY > 1900 and YYYY <= nextYear:
            return 1
        else:
            return 0

    @staticmethod
    def IsValidDay(DD):
        return 1

    @staticmethod
    def IsValidMonth(MM):
        MM = int(MM)
        if MM >= 1 and MM <= 12:
            return 1
        else:
            return 0
    
    @staticmethod
    def GetDateFromName(name):
        # Try and get something from (YYYYMM)
        # DigitalCameraWorld201307 || Digital Camera World 2013 07 || Digital Camera World 2013_07
        # Digital Camera World 2013-07 || Digital Camera World 2013.07
        # DigitalCameraWorld072013 || Digital Camera World 07 2013 || Digital Camera World 07_2013
        # DigitalCameraWorld07-2013 || Digital Camera World 07.2013 
        match = re.match('(\S\D*)(\d{6}|\d{4}\D{1}\d{2}|\d{2}\D{1}\d{4})', name)
        if match:
            date = Organiser.RemoveJoins(match.group(2), (' ','.','_','-'))
            YYYY = date[:4]
            MM = date[-2:]
            if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                return (Organiser.FormatDate(YYYY,MM), match.group(2))
            MM = date[:2]
            YYYY = date[-4:]
            if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                return (Organiser.FormatDate(YYYY,MM), match.group(2))
        for month in calendar.month_name[1:]:
            # TechLif55dd3433e4News_1_August2014 || TechLif55dd3433e4News1August2014
            p = re.compile(ur'(\d{1}|\d{2})\D?(' + month + ')(\d{4})', re.IGNORECASE)
            match = re.search(p, name)
            if match:
                DD = match.group(1)
                MM = Organiser.GetMonthNumberFromName(match.group(2))
                YYYY = match.group(3)
                if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                    return (Organiser.FormatDate(YYYY,MM,DD), match.group(0))
            # TechLif55dd3433e4News_August2014 || TechLif55dd3433e4NewsAugust2014
            p = re.compile(ur'(' + month + ')(\D?)(\d{4})', re.IGNORECASE)
            match = re.search(p, name)
            if match:
                MM = Organiser.GetMonthNumberFromName(match.group(1))
                YYYY = match.group(3)
                if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                    return (Organiser.FormatDate(YYYY,MM), match.group(0))
            # TechLif55dd3433e4News_August_23_2014 || TechLif55dd3433e4NewsAugust232014          
            p = re.compile(ur'(' + month + ')[\S|\s]?(\d{1}\d?)[\S|\s]?(\d{4})', re.IGNORECASE)
            match = re.search(p, name)
            if match:
                MM = Organiser.GetMonthNumberFromName(match.group(1))
                DD = match.group(2)
                YYYY = match.group(3)
                if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                    return (Organiser.FormatDate(YYYY,MM,DD), match.group(0))

    @staticmethod
    def GetCountryFromName(name):
        countryNames = ('UK', 'USA', 'IN', 'AU',)
        for countryName in countryNames:
            p = re.compile(ur'(' + countryName + ')', re.IGNORECASE)
            match = re.match('(\S\D*)(\d{6}|\d{4}\D{1}\d{2}|\d{2}\D{1}\d{4})', name)
                if match:
                    date = Organiser.RemoveJoins(match.group(2), (' ','.','_','-'))
                    YYYY = date[:4]
                    MM = date[-2:]
                    if Organiser.IsValidYear(YYYY) == 1 and Organiser.IsValidMonth(MM) == 1:
                        return (Organiser.FormatDate(YYYY,MM), match.group(2))


            

    @staticmethod
    def RemoveJoins(string, joins = ('.','_','-')):
        i = 0
        for join in joins:
            string = string.replace(joins[i],"")
            i += 1
        return string
    
    @staticmethod
    def GetMonthNumberFromName(name):
        name = name.lower()
        # Try with full month name
        i = 1;
        for month in calendar.month_name[1:]:
            if month.lower() in name:
                return i
            i += 1
        # Try with full month abbreviation
        i = 1;
        for month in calendar.month_abbr[1:]:
            if month.lower() in name:
                return i
            i += 1
        return 0

    @staticmethod
    def SplitCamelCase(name):
        print name
        p = re.compile(ur'([A-Z\d]*[a-z\d]+)([A-Z\d]*[a-z\d]+)+')
        match = re.match(p, name)
        # need to stop this from matching on cases which have whitespace using better regex
        if match and " " not in name:
            print "lol"
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
            name = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
        return name

    #@staticmethod
    #def GetParts(name):

     
#if it contains a six digit number:
#last four digits above 1900 and first two digits 01 <> 12

#first four digits above 1900 first two digits 01 <> 12
os.system('cls')
print '\nTest Name - (Formatted Date, Raw Date):\n'
testNames = (
    'TechLif55dd3433e4News_1_August2014',
    'TechLif55dd3433e4News1August2014',
    'Digital Camera World 2013-07',
    'DigitalCameraWorld2013 07',
    'DigitalCameraWorld07-2013',
    'Digital Camera World 07.2013'
    )
for name in testNames:
    print name + ' - ' + str(Organiser.GetDateFromName(name)) + '\n'

print '\nEnd of basic name tests\n\n'

files = Organiser.ScanDirectory("D:\Downloads\Processed Downloads\Magazines","pdf",0)

for filepath in files:
    name = Organiser.NameFromFilepath(filepath)
    #print name + ' - ' + str(Organiser.GetDateFromName(name)) + '\n'
    with open("d:\Mags.txt", "a") as logfile:
                logfile.write(name + ' - ' + str(Organiser.GetDateFromName(name)) + '\n')




sys.exit();
name = 'House Beautiful - September 2014  UK'
date = Organiser.GetDateFromName(name)

print date

name = name.replace(date[1],"")
name = Organiser.RemoveJoins(name)
name = Organiser.SplitCamelCase(name)
print re.sub('\s{2,}', ' ', name)


sys.exit()

path = "d:\Downloads\Completed Downloads"
magazinesDir = "G:\Magazines"
processedDir = "D:\Downloads\Processed Downloads\Magazines"
fileType = "pdf"
os.system('cls')

print "Scanning for " + fileType + " files..."
#files = Organiser.ScanDirectory(path,fileType,1)

print Organiser.GetMonthNumberFromName("Dot Net - Issue 243, Feb 2013")


#for file in files:
    #os.system('cls')
#    print file + "\n"
    #print Organiser.NameFromFilepath(file)
    

    #try:
    #    print 'Copying...' + file
    #    shutil.copy(file,processedDir)
    #except IOError, e:   
    #    print e


#print len(files)

raw_input()

sys.exit()



