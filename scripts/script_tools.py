'''
Created on Aug 3, 2017

@author: Bilva Sanaba
Class containing classes and methods for the purpose of scripting
'''
import argparse
import sys
import os

def build_path():
    """Adds the working directory to the python path temporarily.
    
    This python package must be in the scripts folder which is in the top level of the directory
    """
    path= os.path.realpath(__file__)
    outer = os.path.dirname(os.path.dirname(path))
    sys.path.append(outer)
    
class StandardArgumentParser:
    """ An encapsulation of argparse.ArgumentParser with a preset group called required arguments"""
    def __init__(self, parserDescription):
        """ Creates an argparse.ArgumentParser with an argument group called 'required arguments' """
        self.parser = argparse.ArgumentParser(description=parserDescription)
        self.requiredArguments = self.parser.add_argument_group('required arguments')
    def add_required_arg(self,key,paramMetavar,helpMessage):
        """ Adds a required argument to the argument parser
        
         Parameters
        ----------
        arg1 : str
            The typed in key for command prompt that defines this argument
        paramMetavar : str
            The string to appear in the help of command prompt giving a title of what the variable is
            for the argument
        helpMessage : str
            The message to appear in command prompt for the argument when help is run
        """
        self.requiredArguments.add_argument(key, metavar=paramMetavar,required=True,help=helpMessage)
    def add_optional_arg(self,key,paramMetavar,helpMessage):
        """ Adds an optional argument to the argument parser 
        
        Parameter 
        ---------
        See add_required_arg
        """
        self.parser.add_argument(key, metavar=paramMetavar, required=False,help=helpMessage)
    def parse_args(self):
        """ Returns an ArgumentParser.parse_args() """
        return self.parser.parse_args()