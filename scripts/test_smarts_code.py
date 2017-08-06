'''
Created on Jul 27, 2017

@author: Bilva

Contains a method for printing the incorrect results from a SMARTS code 
Script from command line prints these
'''
from src.smarts_tool import countMolecules,SmartsCode
from src.library_tool import LibraryReader

def testCode(self,code,positiveFile,negativeFile,fileFormat='smiles'):
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
    value = code
    smarts = SmartsCode(value)
    falseNegatives =_getNonmatchingMolecules(positiveFile,fileFormat,smarts,1)
    falsePositives =_getNonmatchingMolecules(negativeFile,fileFormat,smarts,0)
    return (falseNegatives,falsePositives)
def _getNonmatchingMolecules(fileName,fileFormat,smartsCode,value):
    falseResults =[]
    molecules = LibraryReader().load_data(fileName,fileFormat)
    for molecule in molecules:
        if (countMolecules([molecule],smartsCode)!=value):
            falseResults.append(molecule.write("smiles").rstrip())
    return falseResults
if __name__ == "__main__":
    import script_tools
    script_tools.build_path()
    parser = script_tools.StandardArgumentParser(description = 'Test a SMARTS code')
    parser.add_required_arg('-s', 'SMARTS', 'The SMARTS code to be tested')
    parser.add_required_arg('-p', 'PATH', 'Path to library of positive hits')
    parser.add_required_arg('-n', 'PATH', 'Path to library of negative hits')
    parser.add_optional_arg('-f', 'FORMAT', 'File format (needed for txt file libraries')
    arguments = parser.parse_args()
    (fn,fp) = testCode(arguments.s,arguments.p,arguments.n,arguments.f)
    print "False Negatives: "
    print [m for m in fn]
    print "False Positives: "
    print [m for m in fp]