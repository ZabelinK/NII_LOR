@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

echo Stopping PostrgeSQL server
%POSTGRESQL_HOME%\pg_ctl -D "%POSTGRESQL_DATABASE_PATH%" stop
