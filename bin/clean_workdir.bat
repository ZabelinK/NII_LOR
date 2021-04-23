@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Cleaning the working directory: '%WORKDIR_PATH%'
rmdir /s /q %WORKDIR_PATH%
mkdir %WORKDIR_PATH%
mkdir %TEMP_DIR_PATH%
