@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Starting PostrgeSQL server
start %POSTGRESQL_HOME%\postgres -D "%POSTGRESQL_DATABASE_PATH%"
timeout /T 5 /NOBREAK

%POSTGRESQL_HOME%\pg_ctl -D "%POSTGRESQL_DATABASE_PATH%" status
