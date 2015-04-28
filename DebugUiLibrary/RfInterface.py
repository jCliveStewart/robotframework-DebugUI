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
#    RfInterface.py
#    Interface to allow Debug to discover xpaths and RF variables
# ---------------------------------------------------------------------------------------------------
DEBUG=False                  # Optional verbose debugging messages
contentLimit=50             # Limit the number of controls found for performance 
                            # Fastest response on Chrome, slower but safer with Firefox 
                            
from time import clock 

# This is the list of RF default variables not to display
from defaultVars import defaultVars
from controlsList import controlsList

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

import traceback 
from time import clock

spcr='   '                  # A spacer between RF command elements

class RfInterface:

    # This should only be initialised once the browser is open ... 
    def __init__(self):
        self._logger = logger
        try: 
            se2lib = BuiltIn().get_library_instance('Selenium2Library')
            self.driver=se2lib._current_browser()
            self.logMsg('DEBUG UI OPEN: '+self.driver.current_url)         # Show a message in the robotframework log
        except:                
            self.driver=None
            
    # ----------- Functions used by the debug UI -----------
            
    # This is a clumsy way of showing messages on the RF log    
    # Sadly they only show after the command completes
    def logMsg(self,*msgs):    
        msgs=[str(msg) for msg in msgs]
        BuiltIn().run_keyword('log',' '.join(msgs))
        # This is a better way but fails to print exceptions 
        #self._logger.debug(str(msgs))
        
    # Get a list of all the currently defined variables in RobotFramework
    def getVars(self):

        # If testing return some test values 
        if self.driver==None:
            print "No build context - ignored getVars"                              # Message for no browser open
            vars={'DOH !! You need the browser open to use the debugger !!':''}     # Shown on the debugger panel
        else:
            vars=BuiltIn().get_variables()                                          # Get the current vars from RF
            # Remove any default variables so we can see the script specific ones 
            for name in vars.keys():
                if name in defaultVars:
                    vars.pop(name, None)           
        return vars
                      
    # Run an RF command         
    def runCommand(self,args):

        # If testing ignore the command - no browser to click ...
        if self.driver==None:
            self.logMsg( "No browser open - ignored runCommand",args )
            return
        else:
            try:             # Saw a UnicodeEncodeError error here which I don't have time to fix
                argsString='   '.join([str(a) for a in args])
                self.logMsg('Running command: '+argsString)    # Log in the RF message log
            except:
                self.logMsg('ERROR ENCODING COMMAND - PROBABLY a UNICODE ERROR')
            
        # If the first thing is a variable name remove it so we can call the RF command
        # Bad luck if there are several commands 
        if args[0].find('${')==0 or args[0].find('@{')==0:
            args=args[1:]
            varName=args[0]
            self.logMsg('Ignored the variable at the start of the command: ${'+str(varName)+'}')
            
        try:                                            # Try catch so we can retry until we get it right
            BuiltIn().run_keyword(*args)
            
        except Exception, err:
            self.logMsg(' ---- Drat - that didn\'t work ---- ')
            self.logMsg(traceback.format_exc())
            self.logMsg(' ---- Drat - that didn\'t work ---- ')
            
        
# -------------------------------------------------
# Functions for getting page contents 
# -------------------------------------------------
        
    # Get all controls of all types off the page and return a list of xpaths
    def getAllPageControls(self):
        self.logMsg("Getting page controls - sorry for any delays")
        if DEBUG: startTime=clock()
        # If testing or no browser open return an empty list
        if self.driver==None:
            self.logMsg( "No build context - ignored getAllPageControls" )
            return ['DOH !! You need the browser open to use the debugger !!']
                   
        self.allControlStrings=[]                               # Keep a global list of controls so we can check for duplicates
        
        # Add Page Title should be command
        titleString="Title should be"+spcr+self.driver.title                        
        self.allControlStrings.append(titleString)
            
        # Add all the control types listed in the controls list 
        for rfCommand, baseXpath in controlsList:                    
            if DEBUG: self.logMsg('    ',baseXpath)
            self.addControlCommands(rfCommand, baseXpath)
                        
        if DEBUG: self.logMsg("TIME TAKE",clock()-startTime)
        self.logMsg("OK got the controls - your turn")
        return self.allControlStrings

    # Given a generic xpath  find page controls and return a list of RF commands
    def addControlCommands(self,RfCommand,baseXpath):
        
        try:                                                        # Exception handling to cast iron guarantee no breakages for the debugger        
            
            self.getPageControls(baseXpath)                         # This updates self.pageControls for speed 
            
            if baseXpath.find("//select")==0:                                                     
                for xpath,webelement in self.pageControls:
                    options=webelement.find_elements_by_tag_name("option")          # Get SELECT OPTIONS                                        
                    # Take the first selection if there is one 
                    if len(options)==0:
                        self.logMsg( 'ERROR - a select with no options - surely this is not possible' )
                    elif len(options)==1:
                        selection=options[0]
                    else:    
                        selection=options[1]                    
                    linkString="Select From List"+spcr+xpath+spcr+selection.text   # +"SELECTION"
                    
                    if not linkString in self.allControlStrings:        # Avoid adding the same control to this list twice 
                        self.allControlStrings.append(linkString)                        
                                        
            elif baseXpath.find('//input')==0:                    
                for xpath,webelement in self.pageControls:
                    # Note checking the baseXpath here rather than the webelement for speed and safety 
                    # Checking for webElement type is slow and can get exceptions 
                    
                    # Get RADIO VALUES - this lists all radio options it finds - RF wants : Select Radio Button   name   value
                    if baseXpath.find('@type="radio"')!=-1:                    
                        radioName=webelement.get_attribute("name")
                        radioValue=webelement.get_attribute("value")
                        linkString="Select Radio Button"+spcr+radioName+spcr+radioValue            
                        
                    # Add values to the command for controls like selects, checkboxes, entryfields 
                    elif baseXpath.find('@type="text"')!=-1:                    
                        linkString=RfCommand+spcr+xpath+spcr+'YOUR-VALUE'         
                        
                    else:
                        linkString=RfCommand+spcr+xpath
                    
                    if not linkString in self.allControlStrings:        # Avoid adding the same control to this list twice 
                        self.allControlStrings.append(linkString)                        
                        
            else:
                for xpath,webelement in self.pageControls:
                    linkString=RfCommand+spcr+xpath                        
                    if not linkString in self.allControlStrings:        # Avoid adding the same control to this list twice 
                        self.allControlStrings.append(linkString)                        
                
        except:
            self.logMsg( "Something broke while getting page contents for",baseXpath)
            msgs=traceback.format_exc().split('\n')
            for msg in msgs:
                self.logMsg( "Exception message:",msg )
            
    # this takes around 3 ms as opposed to up to 15 for get_attribute etc 
    # Sadly it breaks for some pages ... 
    def get_text_excluding_children(self, element):
        return self.driver.execute_script("""
        return jQuery(arguments[0]).contents().filter(function() {
            return this.nodeType == Node.TEXT_NODE;
        }).text();
        """, element)            
            
    # Find an xpath selector for an element
    def findSelector(self,webElement,baseXpath):
        xpath=None    
        
        # This is expensive in terms of time 
        #webElementText=self.get_text_excluding_children(webElement)  # 3 ms this is way faster but fragile
        webElementText=webElement.get_attribute('textContent')        # 8 ms fastish and ok for all but IE 
        #webElementText=webElement.text                               # 15 ms   

        # Choose the properties to use to select the specific element - ID first
        if webElement.get_attribute("id") not in ['',None]:
            xpath=webElement.get_attribute("id")
            
        # Then name    
        elif webElement.get_attribute("name") not in ['',None]:
            name=webElement.get_attribute("name")    
            xpath=baseXpath+'[@name="'+name+'"]'
            xpath=xpath.replace('][',' and ')                   # If the incoming xpath specified properties add 'and' between them     

        # Selects tend to be defined by class name            
        elif baseXpath in ['//select']:
            elementClass=webElement.get_attribute("class")    
            if elementClass not in ['',None]:
                xpath=baseXpath+'[@class="'+elementClass+'"]'
                xpath=xpath.replace('][',' and ')                   # If the incoming xpath specified properties add 'and' between them     
            else:    
                xpath=None
            
        # Then text    
        elif webElementText!='':            
            # Deal with strings that split across lines        
            pos=webElementText.find("\n")
            if pos>1:
                xpath=baseXpath+'[starts-with(text(),"'+webElementText[:pos].strip()+'")]'                
                xpath=xpath.replace('][',' and ')           # If the incoming xpath specified properties add 'and' between them     
            # Normal strings with no splitting     
            else:
                xpath=baseXpath+'[text()="'+webElementText+'"]'                                
                xpath=xpath.replace('][',' and ')           # If the incoming xpath specified properties add 'and' between them     
            
        # For Next >> buttons - id and value 
        elif webElement.get_attribute("type")=='submit':
            value=webElement.get_attribute("value")
            xpath='//input[@type="submit" and @value="'+value+'"]'
                                    
        # After that we're jiggered    
        else:
            if DEBUG: self.logMsg( "Failed to find an identifier for xpath",baseXpath,webElementText )
            xpath=None
            
        return xpath
                                   
    # Get a list of xpath selectors for a particular type from the page
    def getPageControls(self,baseXpath):
    
        self.pageControls=[]    
        self.getWebElements(baseXpath)                                  # This updates newWebElements for speed 

        for webElement in self.newWebElements[:contentLimit]:
            xpath = self.findSelector(webElement,baseXpath)
            if xpath != None:
                self.pageControls.append((xpath,webElement))            # Pass back the webelement so we can get select options etc 
                                
    # Get a list of matching web elements using an xpath or css expression. CARE these are volatile if the page is dynamic
    def getWebElements(self,xpath):            
    
        self.newWebElements=[]
        webElementsFound=self.driver.find_elements_by_xpath(xpath)                    
        
        for webElementFound in webElementsFound:            
            try: 
                if not webElementFound.is_enabled():                      # Ignore disabled items
                    pass            
                elif not webElementFound.is_displayed():                    # Ignore invisible items
                    pass            
                elif xpath=="//a" and webElementFound.text=="":             # Ignore empty links with no text, name, ID 
                    pass                
                else:
                    self.newWebElements.append(webElementFound)
                    
            except:
                # Sometimes get stale element exceptions for some page dynamic content
                pass
                
# ------------------ Testing for this program ------------------      
if __name__=='__main__':
    testVars={1:1,2:2,3:3}      # Just for testing with no selenium 

# ------------------ End of File ------------------
