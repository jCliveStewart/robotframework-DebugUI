README.rst

Robot Framework Debug User Interface
Introduction
Installation
Example
Usage
Documentation
License
Introduction

Robot Framework DebugUI is hosted on GitHub where you can find source code, an issue tracker, and some further documentation. 
Downloads are hosted at PyPI.

Latest version Number 0.1.0


Installation

If you already have Python with pip installed, you can simply install from the command line:
pip install robotframework - DebugUI

Alternatively you can get Robot Framework DebugUI source code by downloading the source distribution from GitHub. 
After that you can install the library with python setup.py install

Example
Below is a simple example of using the debug UI. 

*** Settings ***
Documentation     This is a simple exapmple for the DebugUI

Resource          DebugUI.py

*** Test Cases ***
Simple Test
    Open Browser   http://www.ucas.ac.uk
    Debug
    Log   Test Complete
    
    
Usage
Add the command Debug at the line before you want to start debugging. 
The Debug UI panel surfaces when robotframework executes the "Debug" command. 
Use the debug 

License
Robot Framework DebugUI is open source software provided under under Apache License 2.0. 
Robot Framework DebugUI documentation and other similar content use Creative Commons Attribution 3.0 Unported license. 
