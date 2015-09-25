#!/usr/bin/python

class Organiser:

    def CurrentNames(magazineDir):
    	""" Returns a list of magazine names based upon names of directories

    	:param magazineDir: Root directory of magazines
    	:type magazineDir: str
    	:returns: List of magazines
    	:rtype: arr
    	"""
        magazineNames = []
        for file in os.listdir(magazinesDir):
            if os.path.isdir(file): pass
            else: magazineNames.append(file)
        return magazineNames

