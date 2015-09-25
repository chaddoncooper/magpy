#!/usr/bin/env python2.7

import sys
from DateFinder import DateFinder
from CountryFinder import CountryFinder
from Util import Util
from Organiser import Organiser

dateFinder = DateFinder()
countryFinder = CountryFinder()

print '\nTest Name - (Formatted Date, Raw Date):\n'
testNames = (
	'Amiga Force jan 2 2004',
	'TechLif55dd3433e4News_1_August2014',
	'TechLif55dd3433e4News1August2014',
	'Digital Camera World 2013-07',
	'DigitalCameraWorld2013 07',
	'DigitalCameraWorld07-2013',
	'Digital Camera World 07.2013',
	'DigitalCameraWorld201307',
	'DigitalCameraWorld307999',
	'DigitalCameraWorld012000',
	'DigitalCameraWorld22000'
	)

for name in testNames:
	print name + ' - ' + str(dateFinder.Find(name)) + '\n'

print '\nEnd of date tests\n\n'

files = Util.FindFiles("/home/chad/Magazines","pdf",0)

for filepath in files:
	name = Util.NameFromFilepath(filepath)
	output = name + ' - ' + str(dateFinder.Find(name)) + ' - ' + str(countryFinder.Find(name)) + '\n'
	print output    
	with open("/home/chad/Mags.txt", "a") as logfile:
		logfile.write(name + ' - ' + str(dateFinder.Find(name)) + '\n')
