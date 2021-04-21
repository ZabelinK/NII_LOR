@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

call %PYTHON_HOME%\python.exe %PY_SCRIPT_DIR%application.py 
