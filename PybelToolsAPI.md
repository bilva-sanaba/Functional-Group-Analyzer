# PybelTools API

## Package: pybelTools
"Stores modules designed for using pybel for specific purposes with ease"
Contains the following Modules: LibraryTool, SMARTSTool

### Module: library_tool.py
#### Class: LibraryReader
"Reads various library file types"
Methods: loadData

##### Method: def loadData(fileName,fileFormat=None):
 Reads a file and returns a list of pybel.Molecule. Use pybel.informats for all possible readable files
        
        Example:
        #Reads a .smiles file using pybel.readfile
        >>> myLibraryMoleculesList = LibraryReader.loadData(myLibrary.smiles)
        #Reads a .txt file of smiles format lines 
        >>>myLibraryMoleculesList = LibraryReader.loadData(myLibrary.txt,fileFormat='smiles')
        
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

#### Class: LibraryWriter
"For writing list[pybel.Molecule] into chemical files, txt files. 
Also provides csv writer"
##### Method: write_library_file(molecules,writeFormat,fileName, overwrite=False)
Writes a list of pybel.molecules to a chemical file
        
    Uses pybel.OutputFile to write the file. Adds every molecule in molecules to the file
    
        Parameters
        ----------
        arg1 : molecules (list[pybel.Molecule]) 
            The molecules being written as the library            
        arg2 : (opt) writeFormat (str) 
            The type of chemical file being written
        arg3 : fileName (str) 
            The library being written to as a file path
        arg4: (opt) overWrite (bool)
            Default = False
            If the file already exists should it be overwritten
            Note: txt files are always overwritten

##### Method:def write_csv_file(fileName, dataList, titleList)
" An improved CSV writer for pybel data-based analysis "
        
For standard tables, all values inside the lists should be numbers or strings,
the titleList sublists should have one element less than the dataList sublists.TitleList is typically a list of one element which is another list of the column titles. 
        
        Parameters
        ----------
        arg1 : dataList(list[list[object]]) 
            The data to be written where each sublist is a row. All objects are converted to strings
        arg2 : titleList (list[list[object]]) 
            The list of titles of columns. All objects are converted to strings. 
            Note: This is a list of list so that multiple rows of titles can exist     

### Module: smarts_tool.py
'SMARTSTool allows for easy use of pybel with the purpose of SMARTS matching on libraries'

Contains the following classes: SmartsCode, SmartsReader, SMARTSDataWriter
Contains the following methods: countOccurences, countMolecules

#### Class: SmartsCode
Encapsulates a pybel.Smarts object
Contains a pybel.Smarts object as well as its string representation and a title.Follows the pybel.Smarts interface with the following methods: findall(pybel.Molecule)

    
#### Method: def \__init__(smartsCode="*",smartsTitle=None):
Stores a smartsCode and smartsTitle representing the SmartsCode object. Also creates a pybel.Smarts object from the smartsCode
    
        Parameters
        ----------
        arg1 : smartsCode str
            Default = "*"  (the blank code string)
            The smartsCode representing the object
        arg2 : smartsTitle str
            A title for the SmartsCode
#### Method: def findall(molecule):
Find all matches of the SMARTS pattern to a particular molecule.Uses pybel.Smarts.findall(molecule)
        
        Parameters
        ----------
        arg1 : pybel.Molecule molecule
            The particular molecule being searched
        Return 
        ----------
        List(list(int)) 
        Each sublist contains ints representing the atoms matching the SMARTS pattern, the entire 
        list contains each occurence of the SMARTS pattern    for the particular molecule

### Class: SmartsReader
Reads various representations of multiple SMARTS strings.

This class reads various representations of multiple SMARTS strings and stores them as a SMARTSTool.SmartsCode object.

#### Method: def generalLoad(myFile,dataType ="csv"):
Given various data types, generates a list of SmartsCode using methods from self.FileDictionary
myFile = object with SMARTS data
dataType = type of the object (all possible types included in SmartsReader.SmartsDictionary)
#### Method: def listLoad(smartsList):
Makes a list of SmartCode from a list of strings
#### Method: def dictLoad(smartsDictionary):
Makes a list of SmartCode from a dictionary of title to code
smartsDictionary = Dictionary -> {title : code}
#### Method: def csvLoad(myCSVFile):
Returns a list[SmartCode] from a csv file

Format of csv must be first column 'Titles', second column 'SMARTS', codes are inside "" marks. Example: (Read by column)
<table><tr>
  <tr>
    <th>Title</th>
    <th>SMARTS</th> 
  </tr>
  <tr>
    <td>Description</td>
    <td>SMARTS Code</td> 
  </tr>
  <tr>
    <td>of</td>
    <td>Inside Quotation</td> 
  </tr>
   <tr>
    <td>SMARTS</td>
    <td>("") Marks</td> 
  </tr>
</table>

### Class: SMARTSDataWriter
Class for writing results into files 
#### Method:  def write\_library_csv(fileName,molecules, smartsCodes, writeFormat = 'smiles'):
 Writes a CSV table with rows being molecules and columns of occurences of SMARTS hits
            
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
  
#### Method: def write\_data\_summary_csv(fileName,molecules, smartsCodes):
Creates CSV of total occurrences and molecules with each SMARTS smartsString
        
        Parameters
        ----------
        arg1 : fileName (str)
            Location of where file will be written
        arg2 : molecules (list[pybel.Molecule]) 
            All molecules to be written into CSV
        arg3 : smartsCodes (list[str])
            All smarts codes to be included in CSV          
            
### __Method__ : def countOccurrences(molecules,smartsCode):
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

### __Method__: def countMolecules(molecules,smartsCode):
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
# Package: scripts
Collection of scripts files using PybelTools for terminal
## Module: script_tools.py
### Method: def build_path():
Adds the working directory to the python path temporarily. This is useful for scripts using PybelTools
This python module must be in the scripts folder which is in the top level of the directory for this methods'
intended function

### Class: StandardArgumentParser:
""" An encapsulation of argparse.ArgumentParser with a preset group called required arguments"""
#### Method: \__init__(parserDescription):
Creates an argparse.ArgumentParser with an argument group called 'required arguments'
	 Parameters
     ----------
		arg1 : parserDescription str
            The description of the parser in command prompt
#### Method: add\_required_arg(key,paramMetavar,helpMessage):
Adds a required argument to the argument parser
        
        Parameters
        ----------
        arg1 : str
            The typed in key for command prompt that defines this argument
        paramMetavar : str
            The string to appear in the help of command prompt giving a title of what the variable is
            for the argument
        helpMessage : str
            The message to appear in command prompt for the argument when help is run

#### Method: def add\_optional_arg(key,paramMetavar,helpMessage):
Adds an optional argument to the argument parser 
        
        Parameter 
        ---------
        See add_required_arg

#### Method: def parse_args():
Returns an ArgumentParser.parse_args() 
    
### Script: analyze\_library_smarts.py
__Usage__ (in terminal): 
<br>

analyzeLibraryFunctionalGroups.py [-h] -l PATHNAME -s PATHNAME [-f FORMAT]

Analyzes functional groups of a library. 
Adds new data files to same directory as library file.

__Required Arguments__:
  -l PATHNAME  the path to the library
  -s PATHNAME  path to csv file containing smiles

__Optional Arguments__:
  -f FORMAT    file format for text files
  -h, --help   show this help message and exit
### Script: test\_smarts_code.py
Test a SMARTS code
#### Method: def testCode(code,positiveFile,negativeFile,fileFormat='smiles'):
    """ 
    Runs a SMARTS code against a positive and negative file and determines if there are any incorrect results
    
    Parameters
        ----------
        arg1 : code (str) 
            The smarts code to be tested  
        arg2: positiveFile (str)
            The file which should return all positive hits for the code
        arg3: negativeFile (str)
            The file which should return all negative hits for the code
        arg4: 
    Returns
    -------
        (list[str],list[str])
        Tuple containing the list of False negatives in smiles and the list of False positives in smiles
    """
####__Usage__ (in terminal):
<br>
 
python.exe testSMARTSCode.py -s SMARTSCODE -p LibraryPositive -n LibraryNegative [-f format]

__Required Arguments__:
  -s SMARTS    the path to the library
  
  -p POSITIVE  path to csv file containing smiles
  
  -n NEGATIVE  path to csv file containing smiles

__Optional Arguments__:
  -f FORMAT    file format for text files
  
  -h, --help   show this help message and exit
###Script: pybel\_analyze\_library_smarts.py
Copy of analyze\_library_smarts.py except has no dependencies with the project
This file can be downloaded and used with just Python 2.7 and pybel
