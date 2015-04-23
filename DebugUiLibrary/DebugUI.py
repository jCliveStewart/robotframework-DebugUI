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
#    DebugUI.py
#    Debugger user interface to try commands for robotFramework scripts
# ---------------------------------------------------------------------------------------------------
import Tkinter as tk
listHeight=30
listWidth=100

import tkMessageBox

commandComboLabel='EXAMPLE commands - Click any command to use it'
historyComboLabel='HISTORY of commands tried - Click any command to use it'
programComboLabel='SAVED commands - these are now on the clipboard ready to use'
varsComboLabel   ='VARIABLES - robotFramework variables and their values'
helpText         ='''

RobotFramework Script Debug UI: 

The entryfield near the top takes commands to try. 
You can edit or type into it or select commands from the page below. 

Three commands are on buttons on the right and in the 'menu' at the left:
Try  - tries out whatever command you have in the entryfield.
Save - saves the current command to the saved page
Exit - quits the debugger and continues your program with the next line after the 'Debug' line

Three views are available depending on which menu item you click: 
Commands - shows a list of suggested available commands. 
History  - shows a list of all commands you try. 
Saved    - shows a list of commands you previously saved.

To use the Debug UI :
  Click on any command to put it into the entryfield. Edit the command, then try it by clicking the Try button or menu item. 
  Double click will load and execute in one go if you are feeling lucky.
  After a command is executed the list of available commands is refreshed. This may take some time where there are lots of controls. 
  When a command works click save to put it on the saved page
  You can step through several commands and save them. 
  Go to the saved page to get the commands into the paste buffer. 
  Paste them into your robotframework script (you need do this before exiting)
  
  When you have finished debugging click exit and robotframework resumes running your testcase on the line after 'Debug'. 
  
You can interact with the browser between tries to get the page ready or back to it's original state. 
You may need to experiment with editing the command to make it work correctly. 

When you open the 'Saved' page the list of saved commands is put on the clipboard ready to paste into your script.

You can use the debugger alongside checkXpath and firebug. It has been tested with firefox and Chrome. 
Check the robotFramework log in RIDE to see the current status. 
'''
class DebugUI:

    def __init__(self,rfInterface):    
    
        self.savedCommands=[]
                   
        self.rfInterface=rfInterface
    
        self.root = tk.Tk()
        self.root.title('RobotFramework DebugUI')
        self.root.bind('<Return>', self.tryCommand)                             # Put 'focus' on the try command button
    
        # Add a menu to select the different history lists - afraid it has to go at the top as far as I can see 
        menubar = tk.Menu(self.root)
        menubar.add_command(label="Try", command=self.tryCommand)
        menubar.add_command(label="Save", command=self.saveCommand)        
        menubar.add_command(label="Exit", command=self.fini)
        menubar.add_command(label="||")
        menubar.add_command(label="Commands", command=self.showCommands)
        menubar.add_command(label="History", command=self.showHistory)                                     
        menubar.add_command(label="Saved", command=self.showProgram)        
        menubar.add_command(label="||")
        menubar.add_command(label="Variables", command=self.showVars)
        menubar.add_command(label="||")
        menubar.add_command(label="Help", command=self.showHelp)
        self.root.config(menu=menubar)
                                
        # A button panel at the top 
        buttonPanel = tk.Frame(self.root)        
        buttonPanel.pack(side=tk.TOP)                                           # Add the buttons panel to the UI
                                     
        # Add an entry field for rf commands 
        self.commandEntryfield=tk.Entry(buttonPanel, width=listWidth)
        self.commandEntryValue=tk.StringVar()
        self.commandEntryfield["textvariable"]=self.commandEntryValue
        self.commandEntryValue.set('Click link  //a[contains(text(),"YOUR_TEXT_HERE")]')
        self.commandEntryfield.pack(side=tk.LEFT)
        self.commandEntryfield.bind('<Double-Button-1>',self.tryCommand)        # Double click trys the command    
        
        # Add a Try command button to the panel 
        PB1 = tk.Button(buttonPanel, text ="Try", command = self.tryCommand, bg="GREEN")
        PB1.pack(side=tk.LEFT)
        PB1.focus_set()                                                         # Set focus on the try command button
                
        # Add a save command button to the panel 
        PB2 = tk.Button(buttonPanel, text ="Save", command = self.saveCommand, bg="Yellow")
        PB2.pack(side=tk.LEFT)
                                              
        # Add an exit button to the panel
        EB = tk.Button(buttonPanel, text ="Exit", command=self.fini, bg="Red")        
        EB.pack(side=tk.LEFT)
                                
        # ---------- Add a combo panel for commands ----------
        self.comboPanel=tk.Frame(self.root)        
        self.comboPanel.pack(side=tk.BOTTOM, expand=tk.YES)                     # Add the combo panel to the UI
        
        # Add a label to it
        self.comboLabelText=tk.StringVar()
        self.comboLabelText.set(commandComboLabel)
        comboLabel=tk.Label(self.comboPanel, textvariable=self.comboLabelText)
        comboLabel.pack(side=tk.TOP, expand=tk.YES)
        
        # ---------- Add a combo panel for history - not packed initially ----------
        self.historyCombo=tk.Listbox(self.comboPanel,width=listWidth,height=listHeight)
        self.historyCombo.bind('<Double-Button-1>',self.listSelect)             # Make double clicks run the list select function
                                
        # ---------- Add a combo panel for variables ----------
        self.varsScroll = tk.Scrollbar(self.comboPanel)
        self.varsCombo = tk.Listbox(self.comboPanel, yscrollcommand=self.varsScroll.set, width=listWidth, height=listHeight)
        self.varsScroll.config(command=self.varsCombo.yview)
        self.varsCombo.bind('<Double-Button-1>',self.listSelect)                # Make double clicks run the list select function
        
        # ---------- Add a list of stored program steps ----------
        self.programList=tk.StringVar()                                         # Create a variable to hold the program steps
        
        # Diplayed program list
        self.progScroll = tk.Scrollbar(self.comboPanel)
        self.programCombo = tk.Text(self.comboPanel, yscrollcommand=self.progScroll.set, height=listHeight, borderwidth=0)        
        self.progScroll.config(command=self.programCombo.yview)
        
        self.programCombo.configure(bg=self.root.cget('bg'), relief=tk.FLAT)        
        self.programCombo.configure(state="disabled")                           # Make the program combo non editable

        # ---------- Make text selectable in the program panel ----------
        self.programCombo.bind('<Double-Button-1>',self.select_all)
        self.programCombo.bind("<Control-Key-a>", self.select_all)
        self.programCombo.bind("<Control-Key-A>", self.select_all)              # just in case caps lock is on        
                                
        # Add a listbox with the commands in
        self.commandScroll = tk.Scrollbar(self.comboPanel)        
        self.commandCombo=tk.Listbox(self.comboPanel, selectmode=tk.BROWSE, yscrollcommand=self.commandScroll.set, width=listWidth, height=listHeight)        
        self.commandScroll.config(command=self.commandCombo.yview)
               
        self.updateCommandsList()                                               # Put the available commands into the commands list - can take ages 
        
        self.commandScroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)     # Make this one show on startup
        self.commandCombo.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.commandCombo.bind('<<ListboxSelect>>',self.listSelect)                    # Clicks select from the list
        self.commandCombo.bind('<Double-Button-1>',self.listSelectRun)          # Double clicks select from the list and run the command

        self.root.mainloop()                                                    # This sits in this loop forever running the UI until you exit
    
    # ---------------- Command entryfield functions ----------------
    
    def select_all(self,event):                                                 # Select all the text in textbox
        self.programCombo.tag_add("sel", "1.0", "end")
        self.programCombo.mark_set("insert", "1.0")
        self.programCombo.see("insert")
        return 'break'
    
    def updateCommandsList(self):                                               # Refresh the contents of the list of commands available
        self.root.config(cursor="watch")                                        # Show an hourglass while selenium reads the controls 
        self.root.update()               
        commandsList=self.rfInterface.getAllPageControls()
        self.commandCombo.delete(0,tk.END)
        for command in commandsList:
            self.commandCombo.insert(tk.END,command)
        self.commandCombo.selection_set(first=0)        
        self.root.config(cursor="")

    def tryCommand(self,event=None):                                            # (Safely) try out the command from the entry field    
        # The event parameter because clicking the enter key passes in an enter event - which we ignore
        self.command=self.commandEntryfield.get()        
        self.commands=self.command.split('  ')
        self.commands=[c.strip() for c in self.commands  if c!='']
        self.rfInterface.runCommand(tuple(self.commands))
        self.historyCombo.insert(0,'  '.join(self.commands))
        self.updateCommandsList()                                               # Put the available commands into the commands list
                
    def saveCommand(self):                                                      # Save the entry field command in saved commands
        command=self.commandEntryfield.get()        
        self.savedCommands.append(command)        
        self.programList.set("\n".join(self.savedCommands))
        
    def listSelect(self,event):                                                 # Select an item from a list - put it into the entryfield
        widget = event.widget
        selection=widget.curselection()
        
        # Timing problems when people click around
        # should really poll but that seems like overkill ... 
        if len(selection)>0:
            value = widget.get(selection[0])
        else:
            value='Log  Drat - click it again...'
        
        self.commandEntryValue.set(value)

    def listSelectRun(self,event):                                              # Select and run an item from a list     
        self.listSelect(event)                                                  # put it into the entryfield
        self.tryCommand()                                                       # Try the command
        
    # ---------------- Show contents ----------------
        
    def clearView(self,label):                                                  # Clear the panel and set the label 
        self.programCombo.pack_forget()
        self.progScroll.pack_forget()
        
        self.commandCombo.pack_forget()
        self.commandScroll.pack_forget()
        
        self.varsCombo.pack_forget()
        self.varsScroll.pack_forget()
        
        self.historyCombo.pack_forget()
        
        self.comboLabelText.set(label)
    
    def showCommands(self):                                                     # Show the available commands
        self.clearView(commandComboLabel)
        self.commandScroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)     # Add the scrollbar
        self.commandCombo.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)       # Add the commands

    def showProgram(self):                                                      # Show the saved program
        self.clearView(programComboLabel)        
        progText=self.programList.get()                                         # Set the text - ie list of steps
        self.programCombo.configure(state="normal")
        self.programCombo.delete(1.0, "end") 
        self.programCombo.insert(1.0,progText)
        self.programCombo.configure(state="disabled")
                        
        self.root.clipboard_clear()                                             # Put the commands on the clipboard automagically 
        self.root.clipboard_append(progText)                                    # when the page is opened - (probably not sensible)
                                
        self.progScroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)        # Add the scroll bar
        self.programCombo.pack(side=tk.LEFT, expand=tk.YES)                     # Show the program steps list

    def showVars(self):                                                         # Show the list of available variables       
        varsDict=self.rfInterface.getVars()                                     # Get the values                
        varsList=dictAsList(varsDict)                                           # Convert to a displayable list
        self.varsCombo.delete(0, tk.END)                                        # Add the values to the control 
        for v in varsList: 
            self.varsCombo.insert(tk.END, v)                
        self.clearView(varsComboLabel)                                          # Show the list
        self.varsScroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)        # Add the scrollbar
        self.varsCombo.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)          # Show the list
        
    def showHistory(self):                                                      # Show the command history 
        self.clearView(historyComboLabel)
        self.historyCombo.pack(side=tk.BOTTOM, expand=tk.YES)

    def showHelp(self):                                                         # Show the help text    
        self.clearView(helpText)

    def fini(self):                                                             # Quit the program
            print "KTHXBYE"
            self.root.destroy()        
            return 

# Convert a dictionary into a list of strings to display
def dictAsList(varsDict):
        varsList=[]
        for key in varsDict.keys():
            varsList.append(str(key)+'  '+str(varsDict[key]))
        return varsList
                        
# ------------------
# Testing for this code 
# ------------------
class FakeRfInterface:

    def getVars(self):
        varsDict={1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,
                  }
        return varsDict
        
    def runCommand(self,args):    
        return 
        
    def getAllPageControls(self):    
        return []
        
if __name__ == '__main__':
    print "TESTING"
    fakeRfInterface=FakeRfInterface()    
    app = DebugUI(fakeRfInterface)
    #DebugUI.showVars()    
    
# -------- End of file --------
    