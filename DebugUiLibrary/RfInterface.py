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

contentLimit=30             # Limit the number of controls found for performance - else you can be hanging around forever ...
                            # This gets me around 15 seconds response on Chrome, slower but safer with Firefox 
DEBUG=False                 # Optional verbose debugging messages

# This is the list of RF default variables not to display
from defaultVars import defaultVars

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

import traceback 

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
            
        
    # Get all controls of all types off the page and return a list of xpaths
    def getAllPageControls(self):
        
        # If testing or no browser open return an empty list
        if self.driver==None:
            self.logMsg( "No build context - ignored getAllPageControls" )
            return ['DOH !! You need the browser open to use the debugger !!']
                   
        self.xpathsFound=[]         # Keep a global list of xpaths so we can find inputs which as checkboxes and buttons and later ignore them when we look for links
        allControlStrings=[]
        
        # Get Page Title
        titleString="Title should be"+spcr+self.driver.title                        
        allControlStrings.append(titleString)
             
        # NOTE : Get the //inputs in this order to avoid getting bogus textfields
        
        # Get CHECKBOXES
        xpathCommands=self.getControlCommands('//input[@type="checkbox"]',"Select checkbox")
        allControlStrings=allControlStrings+xpathCommands
        
        # Get BUTTONS
        xpathCommands=self.getControlCommands('//input[@type="submit"]',"Click button")
        allControlStrings=allControlStrings+xpathCommands
        
        # Get RADIOS - this lists all radio options it finds - RF wants : Select Radio Button   name   value
        linkXpaths=self.__Get_Page_Controls__('//input[@type="radio"]')
        for linkXpath in linkXpaths:        
            # In case __Get_Page_Controls__ returns None
            if linkXpath.__class__.__name__!='WebElement':
                if DEBUG: self.logMsg("ERROR for RADIO linkXpath",linkXpath)
            else:    
                radioSelection=self.__get_webElement__(linkXpath)
                #if radioSelection==None:             # Seen an error where __get_webElement__ returns None 
                #    self.logMsg("ERROR for select linkXpath",linkXpath)
                #else:
                radioName=radioSelection.get_attribute("name")
                radioValue=radioSelection.get_attribute("value")
                linkString="Select Radio Button"+spcr+radioName+spcr+radioValue
                if not linkString in allControlStrings:
                    allControlStrings.append(linkString)

        # Get INPUT FIELDS
        xpathCommands=self.getControlCommands('//input',"Input text")
        # Add a dummy variable for the user to replace
        xpathCommands=[c+spcr+'${"VALUE"}' for c in xpathCommands]            
        allControlStrings=allControlStrings+xpathCommands
        
        # Get LINKS
        xpathCommands=self.getControlCommands('//a',"Click link")
        allControlStrings=allControlStrings+xpathCommands
                        
        # Get SELECTS
        linkXpaths=self.__Get_Page_Controls__('//select')                                     
        for linkXpath in linkXpaths:                
            selectControl=self.__get_webElement__(linkXpath)                
            # For condition where __get_webElement__ returns None - cannot compare WebElement with None
            if selectControl.__class__.__name__!='WebElement':
                if DEBUG: self.logMsg("ERROR for select xpath",linkXpath)
            else:
                # Find the available selections 
                selections=selectControl.find_elements_by_tag_name("option")
                # Take the first selection if there is one 
                if len(selections)==0:
                    self.logMsg( 'ERROR - a select with no selections - surely this is not possible' )
                elif len(selections)==1:
                    selection=selections[0]
                else:    
                    selection=selections[1]                    
                    linkString="Select From List"+spcr+linkXpath+spcr+selection.text   # +"SELECTION"
                    if not linkString in allControlStrings:
                        allControlStrings.append(linkString)
                        
        return allControlStrings

    # Given a generic xpath  find page controls and return a list of RF commands
    def getControlCommands(self,xpath,RfCommand):
        controlStrings=[]
        try: 
            xpaths=self.__Get_Page_Controls__(xpath)
            for xpath in xpaths:
                linkString=RfCommand+spcr+xpath
                if xpath in self.xpathsFound:
                    pass
                elif linkString in controlStrings:
                    pass
                else:    
                    controlStrings.append(linkString)                        
        except:
            self.logMsg( "Something broke while getting page contents for",xpath)
            msgs=traceback.format_exc().split('\n')
            for msg in msgs:
                self.logMsg( "Exception message:",msg )
    
        return controlStrings
        
    # ----------- End of functions used by the debug UI -----------
                
    def __Get_Page_Controls__(self,baseXpath):
        """Get a list of valid elements of a particular type from a page. You can use names like LINKS, INPUTS, SELECTS or xpath expressions"""    
        
        pageControls=[]    
        webElements=self.driver.find_elements_by_xpath(baseXpath)
        
        for webElement in webElements[:contentLimit]:

            # Ignore invisible items
            if not webElement.is_displayed():
                pass
            # Ignore disabled items
            elif not webElement.is_enabled():
                pass
            # Ignore empty links - no text, name, ID 
            elif baseXpath=="//a" and webElement.text=="":
                if DEBUG: self.logMsg( "Ignoring empty link" )
                pass
            # Ignore buttons and radios when we are searching for inputs 
            # find them separately when we search for specific types of inputs
            elif baseXpath=="//input" and webElement.get_attribute("type") in ["submit","button","radio","checkbox"]:
                pass               
            else:    
                xpath = self.__findSelector__(webElement,baseXpath)
                if xpath != None:
                    pageControls.append(xpath)
                            
        return pageControls
                                
    # Find an xpath selector for an element
    def __findSelector__(self,webElement,baseXpath):
        
        xpath=None    
        
        # Choose the attributes to use to select the specific element - ID first
        if webElement.get_attribute("id") not in ['',None]:
            xpath=webElement.get_attribute("id")
            
        # Then name    
        elif webElement.get_attribute("name") not in ['',None]:
            name=webElement.get_attribute("name")    
            xpath=baseXpath+'[@name="'+name+'"]'
            xpath=xpath.replace('][',' and ')
            
        # Then text    
        elif webElement.text!='':
        
            # Deal with strings that split across lines        
            pos=webElement.text.find("\n")
            if pos!=-1:
                webElementText=webElement.text[:pos].strip()
                xpath=baseXpath+'[starts-with(text(),"'+webElementText+'")]'                
            # Normal strings with no splitting     
            else:
                webElementText=webElement.text                    
                xpath=baseXpath+'[text()="'+webElementText+'"]'                
            xpath=xpath.replace('][',' and ')
            
        # For Next >> buttons - id and value 
        elif webElement.get_attribute("type")=='submit':
            value=webElement.get_attribute("value")
            xpath='//input[@type="submit" and @value="'+value+'"]'
            
        # For checkboxes - use id or name     
        elif webElement.get_attribute("type")=='checkbox':
            id=webElement.get_attribute("id")
            name=webElement.get_attribute("name")
            if id!='':
                xpath=id
            elif name!='':
                xpath='//input[@name="'+name+'"]'
            else:
                if DEBUG: self.logMsg( "PROBLEM finding an identifier for checkbox",xpath,webElement.text )
                xpath=None
                                    
        # After that we're jiggered    
        else:
            if DEBUG: self.logMsg( "PROBLEM finding an identifier for xpath",baseXpath,webElement.text )
            xpath=None
        
        return xpath
            
    # Get a list of matching web elements using an xpath or css expression. CARE these are volatile if the page is dynamic
    def __get_webElements__(self,linkXpath):
            
        if linkXpath.find('//')==0:                                     # If using an Xpath expression
            webElements=self.driver.find_elements_by_xpath(linkXpath)            
        else:                                                           # else we are using a CSS expression    
            webElements=self.driver.find_elements_by_id(linkXpath)        
            
        if len(webElements)==0:
            if DEBUG: self.logMsg( '__get_webElements__ - ELEMENT NOT FOUND',linkXpath )
            
        return webElements    

    # Get a single webElement using an xpath expression return either the element or None
    def __get_webElement__(self,linkXpath):
        webElements=self.__get_webElements__(linkXpath)
        if len(webElements)>1:
            if DEBUG: 
                self.logMsg('__get_webElement__ - MULTIPLE ELEMENTS FOUND',linkXpath)
                self.logMsg('returning the first element')
            webElement=webElements[0]
        elif len(webElements)==1:
            webElement=webElements[0]
        else:    
            webElement=None
        return webElement
        
    # This is a clumsy way of showing messages on the RF log    
    # Sadly they only show after the command completes
    def logMsg(self,*msgs):    
        msgs=[str(msg) for msg in msgs]
        BuiltIn().run_keyword('log',' '.join(msgs))
        # This is a better way but fails to print exceptions 
        #self._logger.debug(str(msgs))
        
# ------------------ Testing for this program ------------------      
if __name__=='__main__':
    testVars={1:1,2:2,3:3}      # Just for testing with no selenium 

# ------------------ End of File ------------------
