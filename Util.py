import os

class Util:

	@staticmethod
	def ClearScreen():
		""" Clears the screen """
		os.system('cls' if os.name == 'nt' else 'clear')

	@staticmethod
	def FindFiles(sourceDir, fileType='', recursive=0):
		""" Recursive scanning of a directory for files of a given type

		:param sourceDir: Root directory to scan.
		:type sourceDir: str
		:param fileType: Type of file to scan for e.g. 'pdf'.
		:type fileType: str
		:param recursive: Will scan subdirs if == 1 (default 0).
		:type recursive: int (1|0) 
		:returns: List of files
		:rtype: array
		"""
		dirs = os.listdir(sourceDir)
		files = []
		for file in dirs:
		    if os.path.isdir(sourceDir + os.path.sep + file) and recursive == 1:
			moreFiles = Util.FindFiles(sourceDir + os.path.sep + file,fileType,recursive)
			if moreFiles:
			    for fileFromSubDir in moreFiles:
				files.append(fileFromSubDir)
		    if fileType == '' or file.lower().endswith(fileType.lower()):
				files.append(sourceDir + os.path.sep + file)
		return files

	@staticmethod
	def RemoveJoins(string, joins = ('.','_','-')):
		i = 0
		for join in joins:
		    string = string.replace(joins[i],"")
		    i += 1
		return string

	@staticmethod
	def SplitCamelCase(name):
		print name
		p = re.compile(ur'([A-Z\d]*[a-z\d]+)([A-Z\d]*[a-z\d]+)+')
		match = re.match(p, name)
		# need to stop this from matching on cases which have whitespace using better regex
		if match and " " not in name:
		    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
		    name = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
		return name

	@staticmethod
	def NameFromFilepath(filepath):
		name = os.path.basename(filepath)
		name = os.path.splitext(name)[0]
		name = name.replace("_", " ")
		return name

