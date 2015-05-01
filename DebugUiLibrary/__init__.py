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
# ---------------------------------------------------------------------------------------------------
from DebugUiLibrary import DebugUiLibrary

from version import VERSION

_version_ = VERSION

class DebugUiLibrary(DebugUiLibrary):
    """
    This test library provides a keywords 'Debug' 
    to allow easy UI based debugging of Robot Framework scripts.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
