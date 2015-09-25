import re

class CountryFinder:

    def __init__(self):
        self.countries = ('UK', 'USA', 'IN', 'AU')

    def Find(self, string):
        """ Try to find country initals within a string """
        names = '|'.join(self.countries)
        pattern = re.compile('(' + names + ')', re.IGNORECASE)
        match = pattern.search(string)
        if match:
            return match.group(1)

    def AddCountry(self, initals):
        """ Adds a country's initals to the finder

        :param initials: e.g. UK, USA etc
        :type initials: str
        """
        self.countries.append(initals)
