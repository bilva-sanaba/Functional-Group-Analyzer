'''
Created on Aug 5, 2017

@author: Bilva
'''
import unittest
from src import smarts_tool, library_tool

class Test(unittest.TestCase):


    def test_count_occurrences(self):
        libTool = library_tool.LibraryReader()
        moleculeList = libTool.load_data("Data/NALDB.txt", 'smiles')
        occurrences =smarts_tool.countOccurrences(moleculeList, smarts_tool.SmartsCode("[#7^3]","Test Code (sp3 Nitrogen)"))
        #Via counting
        self.assertEqual(98, occurrences)
    def test_count_molecules(self):
        libTool = library_tool.LibraryReader()
        moleculeList = libTool.load_data("Data/NALDB.txt", 'smiles')
        molecules = smarts_tool.countMolecules(moleculeList, smarts_tool.SmartsCode("[#7^3]","Test Code (sp3 Nitrogen)"))
        #Via counting
        self.assertEqual(74,molecules)


if __name__ == "__main__":
    unittest.main()