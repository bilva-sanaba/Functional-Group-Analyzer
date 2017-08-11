# Library Functional Group Analyzer 

This is a python project, which uses pybel, in order to provide additional tools for pybel. It was intended to be expanded with scripts useful to chemoinformatics. 
<br>
Currently it serves one major function. Analyzing a library of molecules for functional group trends.  
<br>
For this, there is a module that can be added to PYTHONPATH in order to work in shell. 
Additionally, there exists a script for analyzing a library show below:


pybel\_analyze\_library_smarts.py is a standalone script which can be downloaded and run with Python 2.7
and pybel. It generates spreadsheets counting the occurences of various functional groups for each molecule in a library when used appropriately.

## Getting Started

### Prerequisites

Linux, Windows, or OSX Computer

### Downloads

Python 2.7: [Python 2.7](https://www.python.org/download/releases/2.7/)

Python 2 must be downloaded on your computer. Follow the link in order to do so. 

In order to use this program, you must install OpenBabel with dependencies. 

Follow the instructions here in order to download OpenBabel 2.3.1 and dependencies for Python 2.7: 
<br>
<br>
 [OpenBabel Download Instructions](https://openbabel.org/docs/dev/UseTheLibrary/PythonInstall.html)
 
 Note the instructions use older versions listed on the website. The older versions do not change usability for functional group analysis but may have bugs for other parts of OpenBabel. 
 Older versions can be found here for Windows:
<br>
 [OpenBabel Download](https://sourceforge.net/projects/openbabel/files/openbabel/)
 <br>
 [pybel Download](https://sourceforge.net/projects/openbabel/files/openbabel-python/1.8/openbabel-python-1.8.py27.exe/download)
 
Once Pybel is installed. Add the directory to your python path. You can check the success of this by typing import pybel
 in your python shell. If the library is installed, the prerequisites are complete.

Download the entire project unless you want to just use the independent script. For that,
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
