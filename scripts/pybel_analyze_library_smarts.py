import pybel
import argparse
import os
import csv

class StandardArgumentParser:
    def __init__(self, parserDescription):
        self.parser = argparse.ArgumentParser(description=parserDescription)
        self.requiredArguments = self.parser.add_argument_group('required arguments')
    def add_required_arg(self,key,paramMetavar,helpMessage):
        self.requiredArguments.add_argument(key, metavar=paramMetavar,required=True,help=helpMessage)
    def add_optional_arg(self,key,paramMetavar,helpMessage):
        self.parser.add_argument(key, metavar=paramMetavar, required=False,help=helpMessage)
    def parse_args(self):
        return self.parser.parse_args()
class LibraryReader:
    """Reads various library file types"""
    def __init__(self):
        None  
    def load_data(self,fileName,fileFormat=None): 
        """
        Reads a file and returns a list of pybel.Molecule. Use pybel.informats for all possible readable files
        
        Example:
        #Reads a .smiles file using pybel.readfile
        >>> myLibraryMoleculesList = LibraryReader.load_data(myLibrary.smiles)
        #Reads a .txt file of smiles format lines 
        >>>myLibraryMoleculesList = LibraryReader.load_data(myLibrary.txt,fileFormat='smiles')
        
        Using pybel.readfile it can read all chemical file types that pybel can handle. 
        Additionally, it automatically determines the file type based on extension unless a fileFormat is specified.
        For .txt, the fileFormat of the txt molecules must be specified. 
    
        Parameters
        ----------
        arg1 : fileName (str) 
            The library being searched as a file path
            
        arg2: (opt) fileFormat (str)
            Default = None
            The file format can be specified rather than extrapolating from the file name
    
        Returns
        -------
        list[pybel.Molecule]
            A list of molecules in the read file 
        """
        fileExtension = self._get_extension(fileName,fileFormat)
        return self.__default_load(fileName,fileExtension) 
    def _get_extension(self,fileName,fileFormat=None):  
        """ Determines the extension of a file based on the fileName path unless a fileFormat is specified"""
        if (fileFormat!=None):
            return fileFormat
        splitFileName = fileName.split(".")
        return splitFileName[-1]
    def __default_load(self,fileName,fileExtension):
        """ Uses pybel.readfile to read a file and returns a list of pybel.molecules"""
        return list(pybel.readfile(fileExtension,fileName))
    
class LibraryWriter:
    """ For writing data into csv"""
    def __init__(self):
        None
    def write_csv_file(self, fileName, dataList, titleList):
        """ An improved CSV writer for pybel data-based analysis
        
        For standard tables, all values inside the lists should be numbers or strings,
        the titleList sublists should have one element less than the dataList sublists.
        titleList is typically a list of one element which is another list of the titles. 
        
        Parameters
        ----------
        arg1 : dataList(list[list[object]]) 
            The data to be written where each sublist is a row. All objects are converted to strings
        arg2 : titleList (list[list[object]]) 
            The list of titles of columns. All objects are converted to strings. Note: This is a list of list
            so that multiple rows of titles can exist     
        """
        with open(fileName, "w") as output:
            for titleRow in titleList:
                self.__write_title_line(output,titleRow)
            for dataRow in dataList:
                self.__write_data_line(output,dataRow)
        output.close()
    def __write_data_line(self, output, listOfData):
        """ Writes a list of information into a row on a csv"""
        self.__write_row(output,listOfData)
    def __write_title_line(self,output, listOfData):
        """ Writes a list of information into a row of the output, skipping the first cell"""
        output.write(",")
        self.__write_row(output,listOfData)
    def __write_row(self,output,listOfData):
        """ Writes a list of information into the output, ending the line after the list"""
        for datapoint in listOfData:
            self.__write_cell(output,datapoint)
        self.__write_new_line_character(output)
    def __write_cell(self,output,datapoint):
        """ Writes a single object into a cell of a csv"""
        output.write('"'+str(datapoint)+'"'+',')
    def __write_new_line_character(self,output):
        """ Writes a new line character to the output"""
        output.write('\n')
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
        myNewSmarts = []
        for smarts in smartsList:
            myNewSmarts.append(SmartsCode(smarts))
        return myNewSmarts
    def dictLoad(self, smartsDictionary):
        """ Makes a list of SmartCode from a dictionary of title to code"""
        myNewSmarts = []
        for key in smartsDictionary:
            myNewSmarts.append(SmartsCode(smartsDictionary[key],key))
        return myNewSmarts
    def csvLoad(self,myCSVFile):
        """ Returns a list[SmartCode] from a csv file
        
         Format of csv must be first row titles, second row codes, codes are inside "" marks
        """
        smartsCodes = []
        with open(myCSVFile) as csvfile:
            smartsCSV = csv.DictReader(csvfile, delimiter=',', quotechar = '"')
            for row in smartsCSV:
                title = row["Title"]
                code = self.__removeQuotes(row["SMARTS"])
                SMARTS = SmartsCode(code,title)
                smartsCodes.append(SMARTS)
        return smartsCodes
    def __removeQuotes(self,stringWord):
        """ Returns a string without quotes around it"""
        if (stringWord.startswith('"') and stringWord.endswith('"')):
            return stringWord[1:-1]
        else:
            return stringWord
    
class SMARTSDataWriter:
    """ Class for writing results into files"""
    def __init__(self):
        self.__LibTool = LibraryWriter()
    def write_library_file(self,fileName,molecules,writeFormat,overwrite=False,txtFormat=False):
        """ Uses LibraryTool.LibraryWriter.write_library_file(params) to write a file"""
        self.__LibTool.write_library_file(molecules,writeFormat,fileName,overwrite)
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
             
        smartsTitles=self.__formatTitlesAndCodes(smartsCodes)
        moleculeLines=self.__formatMoleculeLines(molecules, smartsCodes, writeFormat)
        self.__LibTool.write_csv_file(fileName,moleculeLines,smartsTitles)   
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
        smartsTitles= self.__formatTitlesAndCodes(smartsCodes)
        molRow = self.__formatNumberOfMolecules(molecules,smartsCodes)
        occurRow=self.__formatNumberOfOccurences(molecules, smartsCodes)
        data = [molRow,occurRow]
        self.__LibTool.write_csv_file(fileName,data,smartsTitles)
    def __formatTitlesAndCodes(self, smartsCodes):
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
    def __formatNumberOfMolecules(self,molecules, smartsCodes):
        """Formats a list for Number of Molecules"""
        global countMolecules
        return self.__formatGeneralList(molecules,smartsCodes,"Number of Molecules", countMolecules)
    def __formatNumberOfOccurences(self,molecules, smartsCodes):
        """Formats a list for Number of Occurences"""
        global countOccurrences
        return self.__formatGeneralList(molecules,smartsCodes,"Number of Occurrences", countOccurrences)
    def __formatGeneralList(self,molecules,smartsCodes,firstCell,methodOperator):
        """ Formats a list with a first cell followed by the value returned by the methodOperator for each smartsCode"""
        moleculeLine =[firstCell]
        for smartsCode in smartsCodes:
            moleculeLine.append(str(methodOperator(molecules,smartsCode.SMARTS)))
        return moleculeLine
    def __formatMoleculeLines(self,molecules,smartsCodes,writeType='smiles'):
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
if __name__ == '__main__':
    #Handle arguments in command line
    parser = StandardArgumentParser('Analyze functional groups of a library \n Adds new files data files to same directory as library file')
    parser.add_required_arg('-l', 'PATHNAME', 'the path to the library')
    parser.add_required_arg('-s', 'PATHNAME', 'path to csv file containing SMARTS codes')
    parser.add_optional_arg('-f','FORMAT','file format for text files')
    arguments = parser.parse_args()
    libraryFileName = arguments.l
    smilesFileName=arguments.s
    fileFormat=arguments.f
    #Find Directory to write new files (same as chemical library directory)
    mypath = os.path.normpath(libraryFileName)
    directory= os.path.dirname(mypath)
    #Creates titles for new files
    basename = os.path.basename(mypath)
    title = basename.split(".")[0]
    fullLibTitle = title+" Functional Group Data.csv"
    summaryLibTitle = title + " Functional Group Data Summary.csv"
    #Reads input files to creates smarts codes and molecules
    myLibTool = LibraryReader()
    moleculeList=myLibTool.load_data(libraryFileName,fileFormat) 
    myDataReader = SmartsReader()
    smartsCodes = myDataReader.csvLoad(smilesFileName)
    myDataWriter = SMARTSDataWriter()
    #Writes new files
    myDataWriter.write_library_csv(os.path.join(directory,fullLibTitle),moleculeList, smartsCodes)
    myDataWriter.write_data_summary_csv(os.path.join(directory,summaryLibTitle),moleculeList, smartsCodes)
