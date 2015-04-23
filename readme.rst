README.rst

Robot Framework Debug User Interface - DebugUiLibrary
Introduction
Installation
Example
Usage
Documentation
License
Introduction

Robot Framework DebugUiLibrary is hosted on GitHub where you can find source code, an issue tracker, and some further documentation. 
Downloads will eventually be hosted at PyPI for pip install.

Latest version Number 0.9.0


Installation

You can get robotFramework DebugUiLibrary source code by downloading the source distribution from GitHub. 

download to a local folder and open a command prompt there. 
You should see a folder called dist
Type or paste:
pip install dist\robotFramework_DebugUiLibrary-0.9.0.zip

Pip should install the library ready for robotFramework to use. 


Usage notes
Add the command Debug at the line before you want to start debugging. 
The Debug UI panel surfaces when robotframework executes the "Debug" command. 
Use the debug 


Example Usage
Below is a simple example of using the debug UI. 

*** Settings ***
Documentation     This is a simple exapmple for the DebugUI

Resource          DebugUiLibrary.py

*** Test Cases ***
Simple Test
    Open Browser   http://www.ucas.ac.uk
    Debug
    Log   Test Complete
    
    
License
Robot Framework DebugUI is open source software provided under under Apache License 2.0. 
Robot Framework DebugUI documentation and other similar content use Creative Commons Attribution 3.0 Unported license. 
