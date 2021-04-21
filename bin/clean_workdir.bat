@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Cleaning the working directory: '%WORKDIR_PATH%'
rmdir /s /q %WORKDIR_PATH%
mkdir %WORKDIR_PATH%

echo Cleaning the result directory: '%RESULT_DIR%'
rmdir /s /q %RESULT_DIR%
mkdir %RESULT_DIR%

echo Cleaning the system logs directory: '%SYSTEM_LOGS_PATH%'
rmdir /s /q %SYSTEM_LOGS_PATH%
mkdir %SYSTEM_LOGS_PATH%
