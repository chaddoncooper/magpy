import calendar, re, datetime

class DateFinder:

	compiledPatterns = []
	groupings = []

	def __init__(self):

		months = '|'.join(calendar.month_name[1:] + calendar.month_abbr[1:])
		
		patterns = [ 
		'(19\d{2}|2\d{3})\D*(0[1-9]|1[0-2])\D*(0[1-9]|1\d{1}|2d{1}|30|31)', # YYYY-MM-DD || YYYYMMDD
		'(0[1-9]|1\d{1}|2d{1}|30|31)\D*(0[1-9]|1[0-2])\D*(19\d{2}|2\d{3})', # DD-MM-YYYY || DDMMYYYY
		'(0[1-9]|1\d{1}|\d{1}|2\d{1}|30|31)?\D?(' + months + ')\D?(19\d{2}|2\d{3})', # 1_August2014 || 1August2014 || 1 aug 2014 || aug 2014
		'(' + months + ')\D?(0[1-9]|1\d{1}|\d{1}|2\d{1}|30|31)?\D?(19\d{2}|2\d{3})', # August_23_2014 || August232014 || Aug232014 || aug 2014
		'(\d{1,2})\D?(\d{4})', # 01_2013 || 012013 || 1 2013 || 12013
		'(\d{4})\D?(\d{1,2})', # 2013_01 || 201301 || 2013_1 || 12013
		]
		groupings = [
		[1,2,3],
		[3,2,1],
		[3,2,1],
		[3,1,2],
		[2,1],
		[1,2]
		]
		i = 0
		for pattern in patterns:
			self.AddPattern(pattern,groupings[i])
			i += 1
			
	def AddPattern(self, pattern, grouping=[1,2,3]):
		""" Adds a regex pattern to the date DateFinder

		:param pattern: Regex pattern string to match dates against
		:type pattern: str
		:param grouping: The grouping pattern where 1=year, 2=month, 3=Day (default=[1,2,3])
		:type grouping: arr
		"""
		self.compiledPatterns.append(re.compile(pattern, re.IGNORECASE))
		self.groupings.append(grouping)

	def Find(self, str):
		""" Attempt to extract a date from a given string 
		Returns formatted date and match if found

		:param str: String to attempt to get date from
		:type str: str
		:returns: Formatted date string
		:rtype: Arr [formatted date, original match]
		"""
		i = 0
		for compiledPattern in self.compiledPatterns:
			match = compiledPattern.search(str)
			if match:
				YYYY = match.group(self.groupings[i][0])
				MM = DateFinder.GetMonthNumberFromName(match.group(self.groupings[i][1]))
				DD = ''				
				if 3 in self.groupings[i]:
					if match.group(self.groupings[i][2]) is not None:
						DD = match.group(self.groupings[i][2])
				if DateFinder.IsValidYear(YYYY) == 1 and DateFinder.IsValidMonth(MM):
					return (DateFinder.FormatDate(YYYY,MM,DD), match.group(0))
			i += 1

	@staticmethod
	def FormatDate(YYYY='', MM='', DD=''):
		""" Formats dates """
		if MM:
		    MM = '-' + format(int(MM), '02d')
		if DD:
		    DD = '-' + format(int(DD), '02d')
		return str(YYYY) + str(MM) + str(DD)

	@staticmethod
	def IsValidYear(YYYY):
		""" Checks if a year is valid """
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
		""" Checks if a day is valid """
		if DD >= 1 and DD <= 31:
			return 1
		else:
			return 0

	@staticmethod
	def IsValidMonth(MM):
		""" Checks if a month is valid """
		MM = int(MM)
		if MM >= 1 and MM <= 12:
		    return 1
		else:
			return 0

	@staticmethod
	def GetMonthNumberFromName(name):
		""" Gets the month number from a name if it's a str
		Returns if it's already a number
		"""
		if str.isdigit(name):
			return name
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
