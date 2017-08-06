'''
Created on Jul 19, 2017
@author: Bilva Sanaba
SMARTSTool allows for easy use of pybel with the purpose of SMARTS matching on libraries
'''
import pybel
import csv
from src import library_tool

class SmartsCode: 
    """
    Encapsulates a pybel.Smarts object

    Contains a pybel.Smarts object as well as its string representation and a title.
    Follows the pybel.Smarts interface with the following methods: findall(pybel.Molecule)
    """
    def __init__(self,smartsCode="*",smartsTitle=None):
        """
        Stores a smartsCode and smartsTitle representing the SmartsCode object. Also creates
        a pybel.Smarts object from the smartsCode
    
        Parameters
        ----------
        arg1 : smartsCode str
            Default = "*"  (the blank code string)
            The smartsCode representing the object
        arg2 : smartsTitle str
            A title for the SmartsCode
        """
        self.smartsString=smartsCode
        self.SMARTS=pybel.Smarts(smartsCode)
        self.codeTitle=smartsTitle 
    @property
    def smartsString(self):
        """ Returns the stored SMARTS string"""
        return self.smartsString
    @smartsString.setter
    def setSmarts(self,smartsCode):
        """ Sets the smartsString and updates the SMARTS object"""
        self.__init__(smartsCode,self.codeTitle)
    def setTitle(self,title):
        """ Sets the value of the code title"""
        self.codeTitle = title
    def findall(self,molecule):
        """Find all matches of the SMARTS pattern to a particular molecule.Uses pybel.Smarts.findall(molecule)
        
        Parameters
        ----------
        arg1 : pybel.Molecule molecule
            The particular molecule being searched
        Return 
        ----------
        List(list(int)) 
        Each sublist contains ints representing the atoms matching the SMARTS pattern, 
        the entire list contains each occurence of the SMARTS pattern for the particular molecule
        """
        return self.SMARTS.findall(molecule)    
    def __str__(self):
        return "SMARTS Code : " + str(self.smartsString) + '    ' + "Title : " + str(self.codeTitle)
    
class SmartsReader: 
    """
    Reads various representations of multiple SMARTS strings.

    This class reads various representations of multiple SMARTS strings and 
    stores them as a SMARTSTool.SmartsCode object.
    """
    def __init__(self):
        """Stores a dictionary of object type to load type"""
        self.FileDictionary = {"csv": self.csvLoad, 
                               "list": self.listLoad, 
                               "dict": self.dictLoad} 
    def generalLoad(self,myFile,dataType ="csv"):
        """ Given various data types, generates a list of SmartsCode using methods from self.FileDictionary"""
        self.FileDictionary[dataType](myFile)
    def listLoad(self, smartsList):
        """ Makes a list of SmartCode from a list of strings"""
        mySmarts = []
        for smarts in smartsList:
            mySmarts.append(SmartsCode(smarts))
        return mySmarts
    def dictLoad(self, smartsDictionary):
        """ Makes a list of SmartCode from a dictionary of title to code"""
        mySmarts = []
        for key in smartsDictionary:
            mySmarts.append(SmartsCode(smartsDictionary[key],key))
        return mySmarts
    def csvLoad(self,myCSVFile):
        """ Returns a list[SmartCode] from a csv file
        
         Format of csv must be first column titles, second column codes, codes are inside "" marks
         First row must be Title | SMARTS
         There can be no cells outside these two columns
        """
        smartsCodes = []
        with open(myCSVFile) as csvfile:
            smartsCSV = csv.DictReader(csvfile, delimiter=',', quotechar = '"')
            for row in smartsCSV:
                title = row["Title"]
                code = self._removeQuotes(row["SMARTS"])
                SMARTS = SmartsCode(code,title)
                smartsCodes.append(SMARTS)
        return smartsCodes
    def _removeQuotes(self,stringWord):
        """ Returns a string without quotes around it"""
        if (stringWord.startswith('"') and stringWord.endswith('"')):
            return stringWord[1:-1]
        else:
            return stringWord
    
class SMARTSDataWriter:
    """ Class for writing results into files"""
    def __init__(self):
        self._LibTool = library_tool.LibraryWriter()
    def write_library_file(self,fileName,molecules,writeFormat,overwrite=False,txtFormat=False):
        """ Uses library_tool.LibraryWriter.write_library_file(params) to write a file"""
        self._LibTool.write_library_file(molecules,writeFormat,fileName,overwrite)
    def write_library_csv(self, fileName,molecules, smartsCodes, writeFormat = 'smiles'):
        """ Writes a CSV table with rows being molecules and columns of occurences of SMARTS hits
           
        Parameters
        ----------
        arg1 : fileName (str)
            Location of where file will be written
        arg2 : molecules (list[pybel.Molecule]) 
            All molecules to be written into CSV
        arg3 : smartsCodes (list[str])
            All smarts codes to be included in CSV 
        arg4 : writeFormat (str)
            Default: 'smiles'
            Format molecules will be written in
        """
             
        smartsTitles=self._format_titles_and_codes(smartsCodes)
        moleculeLines=self._format_molecule_lines(molecules, smartsCodes, writeFormat)
        self._LibTool.write_csv_file(fileName,moleculeLines,smartsTitles)   
    def write_data_summary_csv(self,fileName,molecules, smartsCodes):
        """ Creates CSV of total occurrences and molecules with each SMARTS smartsString
        Parameters
        ----------
        arg1 : fileName (str)
            Location of where file will be written
        arg2 : molecules (list[pybel.Molecule]) 
            All molecules to be written into CSV
        arg3 : smartsCodes (list[str])
            All smarts codes to be included in CSV          
        """
        smartsTitles= self._format_titles_and_codes(smartsCodes)
        molRow = self._format_number_of_molecules(molecules,smartsCodes)
        occurRow=self._format_number_of_occurences(molecules, smartsCodes)
        data = [molRow,occurRow]
        self._LibTool.write_csv_file(fileName,data,smartsTitles)
    def _format_titles_and_codes(self, smartsCodes):
        """ Formats a list of titles rows"""
        smartsNameTitles = []
        smartCodes = []
        for smartsCode in smartsCodes: 
            smartsNameTitles.append(smartsCode.codeTitle)
            smartCodes.append(smartsCode.smartsString)
        if smartsNameTitles.count(None)==len(smartsNameTitles):
            titleRows=[smartCodes]
        else: 
            titleRows = [smartsNameTitles,smartCodes]
        return titleRows
    def _format_number_of_molecules(self,molecules, smartsCodes):
        """Formats a list for Number of Molecules"""
        global countMolecules
        return self._format_general_list(molecules,smartsCodes,"Number of Molecules", countMolecules)
    def _format_number_of_occurences(self,molecules, smartsCodes):
        """Formats a list for Number of Occurences"""
        global countOccurrences
        return self._format_general_list(molecules,smartsCodes,"Number of Occurrences", countOccurrences)
    def _format_general_list(self,molecules,smartsCodes,firstCell,methodOperator):
        """ Formats a list with a first cell followed by the value returned by the methodOperator for each smartsCode"""
        moleculeLine =[firstCell]
        for smartsCode in smartsCodes:
            moleculeLine.append(str(methodOperator(molecules,smartsCode.SMARTS)))
        return moleculeLine
    def _format_molecule_lines(self,molecules,smartsCodes,writeType='smiles'):
        """ Creates a list of lists with each sublist having a molecule first, followed"""
        moleculesLines = []
        for molecule in molecules:
            moleculeLine = []
            moleculeLine.append(molecule.write(writeType).rstrip())
            for smartsCode in smartsCodes:
                moleculeLine.append(str(countOccurrences([molecule],smartsCode.SMARTS)))
            moleculesLines.append(moleculeLine)
        return moleculesLines
  
def countOccurrences(molecules,smartsCode): 
    """
    Counts the number of occurrences of a substructure indicated by a SMARTS smartsString in a library

    Parameters
    ----------
    arg1 : list (pybel.Molecule) 
        The library being searched, represented as a list of pybel.Molecule objects
    arg2 : pybel.Smarts or SMARTSTool.SmartsCode
        Object representing the substructure SMARTS smartsString that will be searched

    Returns
    -------
    int
        Count of number of occurrences of substructure throughout library
    """
    occurrences = 0
    for molecule in molecules:
        occurrences+=len(smartsCode.findall(molecule))
    return occurrences

def countMolecules(molecules,smartsCode):
    """
    Counts the number of molecules that contain the substructure indicated by the SMARTS smartsString

    Parameters
    ----------
    arg1 : list (pybel.Molecule) 
        The library being searched, represented as a list of pybel.Molecule objects
    arg2 : pybel.Smarts or SMARTSTool.SmartsCode
        Object representing the substructure SMARTS smartsString that will be searched

    Returns
    -------
    int
        Count of number of molecules containing desired substructure 
    """
    moleculeCount = 0
    for molecule in molecules:
        if (len(smartsCode.findall(molecule))>0):
            moleculeCount+=1
    return moleculeCount    