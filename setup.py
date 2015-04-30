#!/usr/bin/python
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
"""A RobotFramework Debug User Interface
"""
import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='robotFramework-DebugUiLibrary',
    version='0.9.0',
    description='Debug robotFramework scripts simply',
    
    long_description=(read('readme.rst') 
                        + '\n\n' + read('history.rst') 
                        ),
    #                   + '\n\n' + read('authors.rst')
    #                   ),
                      
    url='http://github.com/UCAS/RF_DebugUI',
    license='Apache 2.0',
    author='J C Stewart',
    author_email='jCliveStewart@users.noreply.github.com',
    
    packages=['DebugUiLibrary'],
    
    include_package_data=True,
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Apache 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
