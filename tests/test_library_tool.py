'''
Created on Aug 4, 2017

@author: Bilva
'''
import unittest
from src import library_tool
import pybel
import csv

class Test(unittest.TestCase):
    def test_load_data(self):
        libTool = library_tool.LibraryReader()
        moleculeList = libTool.load_data("Data/NALDB.txt", 'smiles')
        self.assertEqual(len(list(pybel.readfile('smiles',"Data/NALDB.txt"))),len(moleculeList))
        moleculeList = libTool.load_data("Data/FDA.smiles")
        self.assertEqual(len(list(pybel.readfile('smiles',"Data/FDA.smiles"))),len(moleculeList))
        moleculeList = libTool.load_data("Data/SingleMolecule.cdx")
        self.assertEqual(len(list(pybel.readfile('cdx',"Data/SingleMolecule.cdx"))),len(moleculeList))
    def test_write_library_file(self):
        libTool = library_tool.LibraryReader()
        libWriter = library_tool.LibraryWriter()
        molecules = libTool.load_data("Data/NALDB.txt", 'smiles')
        libWriter.write_library_file(molecules, 'smiles', "Data/NALDB2.txt", True)
        self.assertEqual(len(list(pybel.readfile('smiles',"Data/NALDB2.txt"))),len(molecules))
        molecules = libTool.load_data("Data/FDA.smiles")
        libWriter.write_library_file(molecules, 'smiles', "Data/FDA2.txt", True)
        self.assertEqual(len(list(pybel.readfile('smiles',"Data/FDA2.txt"))),len(molecules))
    def test_write_library_csv(self):
        libWriter = library_tool.LibraryWriter()
        data = [ ["First Set",1,2,3,4],["Second Set", 5,6,7,8]]
        titles = [ ['First','Second','Third','Fourth'], ["%4=1","%4=2","%4=3","%4=0]"]]
        libWriter.write_csv_file("Data/TestCSVWriting.csv",data,titles)
        with open('Data/TestCSVWriting.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            count= 0
            for row in reader:
                count+=1
        csvfile.close()
        self.assertEqual(count,4)
if __name__ == "__main__":
    unittest.main()