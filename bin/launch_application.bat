@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

mkdir %TEMP_DIR_PATH%

call %PYTHON_HOME%\python.exe %APPLICATION_SCRIPT_DIR%application.py %TEMP_DIR_PATH%
