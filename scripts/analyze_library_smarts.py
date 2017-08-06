import os
import script_tools
script_tools.build_path()
from src import smarts_tool,library_tool
#Handle arguments in command line
parser = script_tools.StandardArgumentParser('Analyze functional groups of a library \n Adds new files data files to same directory as library file')
parser.add_required_arg('-l', 'PATHNAME', 'the path to the library')
parser.add_required_arg('-s', 'PATHNAME', 'path to csv file containing SMARTS codes')
parser.add_optional_arg('-f','FORMAT','file format for text files')
arguments = parser.parse_args()
libraryFileName = arguments.l
smartsFileName=arguments.s
fileFormat=arguments.f
#Find Directory to write new files (same as chemical library directory)
myPath = os.path.normpath(libraryFileName)
directory= os.path.dirname(myPath)
#Creates titles for new files
basename = os.path.basename(myPath)
title = basename.split(".")[0]
fullLibTitle = title+" Functional Group Data.csv"
summaryLibTitle = title + " Functional Group Data Summary.csv"
#Reads input files to creates smarts codes and molecules
myLibTool = library_tool.LibraryReader()
moleculeList=myLibTool.load_data(libraryFileName,fileFormat) 
myDataReader = smarts_tool.SmartsReader()
smartsCodes = myDataReader.csvLoad(smartsFileName)
myDataWriter = smarts_tool.SMARTSDataWriter()
#Writes new files
myDataWriter.write_library_csv(os.path.join(directory,fullLibTitle),moleculeList, smartsCodes)
myDataWriter.write_data_summary_csv(os.path.join(directory,summaryLibTitle),moleculeList, smartsCodes)
