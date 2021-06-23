set BIN_DIR=%~dp0
set PROJECT_DIR=%BIN_DIR%..

set WORKDIR_PATH=..\workdir\
set TEMP_DIR_PATH=%WORKDIR_PATH%\temp\
set SOFT_PATH=%PROJECT_DIR%\soft\
set APPLICATION_SCRIPT_DIR=%PROJECT_DIR%\libs\scripts\src\
set INPUT_DIRECTORY=..\data_set\
set PATH_TO_WORDS=%INPUT_DIRECTORY%\words\
set PATH_TO_NOISES=%INPUT_DIRECTORY%\noises\
set PATH_TO_BITMAPS=%PROJECT_DIR%\libs\scripts\bitmaps\
set PATH_TO_DOC_TEMPLATES=%PROJECT_DIR%\libs\scripts\templates\

set SEV_ZIP_PATH="%SOFT_PATH%\7-Zip\7z.exe"
set PYTHON_PATH=%WORKDIR_PATH%installed_soft\python

set PYTHON_HOME=%PYTHON_PATH%