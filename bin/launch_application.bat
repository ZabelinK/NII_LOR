@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

call %PYTHON_HOME%\python.exe %APPLICATION_SCRIPT_DIR%application.py %TEMP_DIR_PATH% %INPUT_DIRECTORY% %PATH_TO_WORDS% %PATH_TO_NOISES% %PATH_TO_BITMAPS%
