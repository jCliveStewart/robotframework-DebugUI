
del dist\*.*
rmdir dist /s /q

del robotFramework_DebugUiLibrary.egg-info\*.*
rmdir robotFramework_DebugUiLibrary.egg-info /s /q

python setup.py sdist

pip uninstall robotFramework_DebugUiLibrary

pause
pip install dist\robotFramework_DebugUiLibrary-0.9.0.zip

