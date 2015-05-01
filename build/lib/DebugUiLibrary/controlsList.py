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
#    controlsList.py
# 
#   a list of control types to find with base xpaths
#   the debugger finds specific examples for each of these 
#   make sure you get the commas right if you edit this     
#
# ---------------------------------------------------------------------------------------------------
controlsList=[
        ('Select From List',    '//select'),                    # Get SELECTS        
        
        ('Select Radio Button', '//input[@type="radio"]'),      # Get RADIOS                
        ('Select checkbox',     '//input[@type="checkbox"]'),   # Get CHECKBOXES                
        ('Click button',        '//input[@type="submit"]'),     # Get BUTTONS
        
        # NOTE : Get remaining //inputs last to avoid creating bogus textfield definitions
        ('Input text',          '//input[@type="text"]'),       # Get TEXT INPUT FIELDS        
        ('Input text',          '//input[@type="textarea"]'),   # Get TEXT INPUT FIELDS        
        ('Click button',        '//input[@type="button"]'),     # Get INPUT BUTTONS
                
        ('Click link',          '//a'),                         # Get LINKS
        ]

print 'controlsList',controlsList        