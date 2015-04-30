README.rst

Robot Framework Debug User Interface
Introduction
Installation
Example
Usage
Documentation
License
Introduction

robotFramework-DebugUILibrary is hosted on GitHub where you can find source code, an issue tracker, and some further documentation. 
Downloads are hosted at PyPI.

Latest version Number 0.9.0


Installation

If you already have Python with pip installed, you can simply install from the command line:
pip install robotFramework-DebugUILibrary

Alternatively you can get robotFramework-DebugUILibrary source code by downloading the source distribution from GitHub. 
After that you can install the library with python setup.py install


Usage Example
Below is a simple example of using the debug UI. You can paste it directly into the RIDE text edit page to try it.

*** Settings ***
Documentation     This is a simple example of using the debugger

Library           DebugUiLibrary

*** Test Cases ***
Simple Test
    Open Browser   http://www.ucas.ac.uk
    Debug
    Log   Test Complete
    
    
Usage Instructions
Add the command 'Debug' at the line before you want to start debugging. 
The Debug UI panel surfaces when robotframework executes the "Debug" command. 
The UI will find xpaths for controls on the page and offer simple commands that may be useful. 
Click a command to select it and use the Try button to try it out. 
Experiment with the xpath until the command works as expected. 
You can use tools like firebug, xpath checker, or you can click and type into the page between attempts. 
When you are happy with the command click the Save button. 
When you have finished your debugging session click 'Saved' to see the saved commands. 
The commands will be automatically put in the paste buffer. 
Switch to the RIDE Text Edit tab and paste the commands in before you exit the debugger. 
Click the exit button. 
The script will continue from the line after the 'Debug' command. 

License
Robot Framework DebugUI is open source software provided under under Apache License 2.0. 
Robot Framework DebugUI documentation and other similar content use Creative Commons Attribution 3.0 Unported license. 
