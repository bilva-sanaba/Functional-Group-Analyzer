# Library Functional Group Analyzer 

Python project, which uses pybel, and provides additional tools for pybel. Intended to be expanded with other scripts useful to chemoinformatics. 
<br>
Currently it has a module designed to better read and write libraries. 
<br>
As well as a module for analyzing libraries by functional groups using SMARTS. 
There also exist scripts in order to analyze library functional groups. 

pybel\_analyze\_library_smarts.py is a standalone script which can be downloaded and run with Python 2.7
and pybel. It generates spreadsheets counting the occurences of various functional groups for each molecule in a library when used appropriately.

## Getting Started

### Prerequisites

Linux, Windows, or OSX Computer

### Downloads

Python 2.7: [Python 2.7](https://www.python.org/download/releases/2.7/)

Python 2 must be downloaded on the computer. Follow the link in order to do so. 

In order to use this program, you must install OpenBabel with dependencies. 

Follow the instructions here in order to download OpenBabel 2.3.1 and dependencies for Python 2.7: 
<br>
<br>
 [OpenBabel Download Instructions](https://openbabel.org/docs/dev/UseTheLibrary/PythonInstall.html)
 
 Note you must download the older versions listed on the website. 
 Older versions can be found here for Windows:
<br>
 [OpenBabel Download](https://sourceforge.net/projects/openbabel/files/openbabel/)
 <br>
 [pybel Download](https://sourceforge.net/projects/openbabel/files/openbabel-python/1.8/openbabel-python-1.8.py27.exe/download)
 
Once Pybel is installed. Add the directory to your python path. You can check the success of this by typing import pybel
 in your python shell. If the library is installed, the prerequisites are complete.

Fork and clone this project onto your computer unless you want to just use the independent script. For that,
just download the script pybel\_analyze\_library_smarts.py 


## Script Example
The most important feature of this project is the generation of functional group data which can be done with the terminal command: 

python.exe analyze\_library_smarts.py -l LibraryFile.* -s SMARTSFile.csv

If you download just the python script: 
python.exe pybel\_analyze\_library_smarts.py -l LibraryFile.* -s SMARTSFile.csv


## Versioning

Version 1.0

## Authors

* **Bilva Sanaba** 
* **Pybel Authors**- *Initial work* - [Pybel](https://sourceforge.net/projects/openbabel/files/openbabel/)


## License

This project is licensed under the GNU3 License - see the LICENSE.md file for details

## Acknowledgments

* Hargrove Lab, Duke University
