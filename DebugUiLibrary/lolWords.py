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
#    lolWords.py
#    Optional lolspeak translations
# ---------------------------------------------------------------------------------------------------
lolWords={
            'ERROR - a select with no options'                  : 'OH NOEZ UH SELECT WIF NO OPSHUNS'                 , 
            'Exception message'                                 : 'EXCEPSHUN MESAGE'                                 ,
            'Getting page controls - sorry for any delay'       : 'GETTIN PAEG CONTROLS - SRY 4 ANY DELAY'           ,
            'Ignored the variable at the start of the command'  : 'IGNORD TEH VARIABLE AT TEH START OV TEH COMMAND'  ,
            'No browser open - ignored run command'             : 'NO BROWSR OPEN - IGNORD RUN COMMAND'              ,
            'OK got the controls'                               : 'K GOT TEH CONTROLS'                               ,
            'Running command'                                   : 'CHASIN TEH MOWSE'                                 ,
            'Something broke while getting page contents for'   : 'OH NOEZ - SoMETHIN BROKE GETTIN PAEG CONTENTS 4'  ,
            'ignored get all page controls'                     : 'IGNORD GIT ALL PAEG CONTROLS'                     , 
            'surely this is not possible'                       : 'SURELY DIS AR TEH NOT POSIBLE'                    ,
            'that didn\'t work'                                 : 'DAT DINT WERK'                                    ,
            'your turn'                                         : 'UR TURN'                                          ,
            }
            
def language_translate(msg):                                        
    for our_words in lolWords.keys():
        if msg.find(our_words)!=-1:
            katz_words=lolWords[our_words]
            msg=msg.replace(our_words,katz_words)
    return msg
                