@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Starting PostrgeSQL database
%POSTGRESQL_HOME%\initdb.exe -D "%POSTGRESQL_DATABASE_PATH%" -U %USER_NAME% -E UTF8
