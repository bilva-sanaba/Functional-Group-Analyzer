'''
Created on Jul 26, 2017

@author: Bilva

LibraryTool provides improved chemical Library reading and writing
'''

import pybel


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
        return self._default_load(fileName,fileExtension) 
    def _get_extension(self,fileName,fileFormat=None):  
        """ Determines the extension of a file based on the fileName path unless a fileFormat is specified"""
        if (fileFormat!=None):
            return fileFormat
        splitFileName = fileName.split(".")
        return splitFileName[-1]
    def _default_load(self,fileName,fileExtension):
        """ Uses pybel.readfile to read a file and returns a list of pybel.molecules"""
        return list(pybel.readfile(fileExtension,fileName))
    
class LibraryWriter:
    """ For writing list[pybel.Molecule] into chemical files, txt files, and provides pybel csv writer"""
    def __init__(self):
        None
    def write_library_file(self,molecules,writeFormat,fileName,overwrite=False):
        """
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
        """
        output = pybel.Outputfile(writeFormat,fileName, overwrite)
        for molecule in molecules:
            output.write(molecule)
        output.close()
    def write_csv_file(self, fileName, data, titles):
        """ An improved CSV writer for pybel data-based analysis
        
        For standard tables, all values inside the lists should be numbers or strings,
        the titleList sublists should have one element less than the dataList sublists.
        titleList is typically a list of one element which is another list of the titles. 
        
        Parameters
        ----------
        arg1 : data     list[list[object]]
            The data to be written where each sublist is a row. All objects are converted to strings
        arg2 : titles   list[list[object]] 
            The list of titles for columns. All objects are converted to strings. 
            Each sublist makes a title row
            Note: This is a list of list so that multiple rows of titles can exist
        """
        with open(fileName, "w") as output:
            for titleRow in titles:
                self._write_title_line(output,titleRow)
            for dataRow in data:
                self._write_row(output,dataRow)
        output.close()
    def _write_title_line(self,output, dataLine):
        """ Writes a list of information into a row of the output, skipping the first cell"""
        output.write(",")
        self._write_row(output,dataLine)
    def _write_row(self,output,dataLine):
        """ Writes a list of information into the output, ending the line after the list"""
        for dataPoint in dataLine:
            self._write_cell(output,dataPoint)
        self._write_new_line_character(output)
    def _write_cell(self,output,dataPoint):
        """ Writes a single object into a cell of a csv"""
        output.write('"'+str(dataPoint)+'"'+',')
    def _write_new_line_character(self,output):
        """ Writes a new line character to the output"""
        output.write('\n')