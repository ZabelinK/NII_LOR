@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Start PostrgeSQL admin
"%POSTGRESQL_PATH%\pgsql\pgAdmin 4\bin\pgAdmin4.exe"
