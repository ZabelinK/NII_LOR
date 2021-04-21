@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Extracting Python to '%PYTHON_PATH%'
%SEV_ZIP_PATH% x "%SOFT_PATH%python-3.7.4.zip" -o"%PYTHON_PATH%"

call %PYTHON_HOME%\python.exe -V

@rem =======================Install Python Packages=========================================
echo Installing Python packages with 'pip'
call %PYTHON_HOME%\python.exe %SOFT_PATH%PythonAddons\get-pip.py
@rem for visualization
call %PYTHON_HOME%\Scripts\pip install -U wxPython
call %PYTHON_HOME%\Scripts\pip install -U sounddevice
call %PYTHON_HOME%\Scripts\pip install -U soundfile
call %PYTHON_HOME%\Scripts\pip install -U requests
call %PYTHON_HOME%\Scripts\pip install -U numpy
@rem ============================================================================================
