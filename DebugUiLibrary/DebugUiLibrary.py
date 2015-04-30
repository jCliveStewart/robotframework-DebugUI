#!/usr/bin/python
# ---------------------------------------------------------------------------------------------------
# Copyright 2015 UCAS 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#    DebugUiLibrary.py
#    The main debug program - we can't call it DebugLibrary because there is already one of that name
# ---------------------------------------------------------------------------------------------------
from RfInterface import RfInterface  # This allows acccess to robotFramework calls and data
from DebugUI import DebugUI          # This is the pop up UI

# This is the main library function used in robotFramework scripts        
class DebugUiLibrary:
    """
    This test library provides a single keyword 'Debug' to allow debugging of robotFramework scripts 

    *Before running tests*

    Prior to running tests, DebugUiLibrary be added as an imported library in your Robot test suite.

    Example:
        | Library | DebugUiLibrary |

    """
    
    def Debug(self):
        """The command "Debug" surfaces the debugger user interface. 
        This suggests possible commands and lets you edit and try them. 
        The commands use valid xpaths found from the page by the debugger. 
        The debugger also lists the current variables in case you want to use them. 
        
        Add "Library   Debug.py" to your project settings section.
        Add "Debug" in your script where you want to start debugging test steps (the line before a problem).
        Experiment with commands until you fix the problem.
        You can manually interact with the page and use browser tools to view xpaths and page source while you debug. 
        When a command works "Save" it
        When you are finished paste the saved commands into your script.    
        
        NOTES: 
        Paste buffer content vanishes when the Debugger closes so paste your new commands into your script before exiting it.
        The debugger may take around 15-30 seconds to surface or update while it searches the page content. 
        Not all controls are found by the debugger - you may have to add or tinker with the command you try. 
        """
        # create an interface to robbotFramework - so we can send commands
        rfInterface=RfInterface()

        # Open up the debug UI 
        debugUI=DebugUI(rfInterface)
           
        # Print a message on exiting the debugger
        print "Debug complete"
    
# Testing for this code     
if __name__=='__main__':
    DebugUiLibrary().Debug()
    
# ------------------ End of File ------------------
