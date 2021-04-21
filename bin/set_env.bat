set BIN_DIR=%~dp0
set PROJECT_DIR=%BIN_DIR%..

set WORKDIR_PATH=..\workdir\
set SOFT_PATH=%PROJECT_DIR%\soft\
set PY_SCRIPT_DIR=%PROJECT_DIR%\libs\scripts\
set APPLICATION_SCRIPT_DIR=%PROJECT_DIR%\libs\
set RESULT_DIR=%PROJECT_DIR%\result\
set INPUT_DIRECTORY=..\data_set\

set SEV_ZIP_PATH="%SOFT_PATH%\7-Zip\7z.exe"
@rem set JDK_PATH=%WORKDIR_PATH%installed_soft\jdk
@rem set POSTGRESQL_PATH=%WORKDIR_PATH%installed_soft\postgresql
set PYTHON_PATH=%WORKDIR_PATH%installed_soft\python

@rem set JAVA_HOME=%JDK_PATH%\jdk-11.0.2\bin
@rem set POSTGRESQL_HOME=%POSTGRESQL_PATH%\pgsql\bin
@rem set POSTGRESQL_ADMIN_HOME=%POSTGRESQL_PATH%\pgsql\pgAdmin 4\bin\pgAdmin4.exe
set PYTHON_HOME=%PYTHON_PATH%

set SYSTEM_LOGS_PATH=%PROJECT_DIR%\system_logs\
set LOGS_GENERAL_FILE=%SYSTEM_LOGS_PATH%setup.log
set LOGS_SOFT_VERSION_FILE=%SYSTEM_LOGS_PATH%installed_soft.log
set LOGS_POSTGRESQL_FILE=%SYSTEM_LOGS_PATH%postgresql.log

set USER_NAME="DOCTOR"
@rem set POSTGRESQL_DATABASE_PATH=%WORKDIR_PATH%postgresql\data
set DATABASE_NAME=SPB_NII_LOR
