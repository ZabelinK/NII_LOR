@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat
SETLOCAL

echo Where to take the data from:
echo   - (1) local 'input' directory,
echo   - (2) Download from OpenEdu by provided settings from 'config/application.yml'
set /p TAKE_INPUT_DATA_FROM="Selected: "

IF NOT DEFINED TAKE_INPUT_DATA_FROM SET "TAKE_INPUT_DATA_FROM=1"

IF "%TAKE_INPUT_DATA_FROM%"=="1" goto handle_local_input_folder
IF "%TAKE_INPUT_DATA_FROM%"=="2" goto download_data

echo Selected unsupported option.
goto end


:handle_local_input_folder
    set /A FILE_CNT=0
    echo The list of files in '%INPUT_DIRECTORY%' directory is:
    for /r %%i in (%INPUT_DIRECTORY%*) do (
        echo   -  %%~nxi
        set /A FILE_CNT+=1
    )

    @rem get first file name
    for /r %%i in (%INPUT_DIRECTORY%*) do (
        IF NOT DEFINED FIRST_FILE_IN_DIRECTORY SET "FIRST_FILE_IN_DIRECTORY=%%~nxi"
        goto select_file
    )

    IF NOT DEFINED FIRST_FILE_IN_DIRECTORY (
        echo No files in directory '%INPUT_DIRECTORY%'
        goto end
    )


:select_file
    IF "%FILE_CNT%"=="1" (
        set FILE_NAME=%FIRST_FILE_IN_DIRECTORY%
        goto file_has_been_selected
    )

    echo Print file name to analyze. If no name is entered, then the '%FIRST_FILE_IN_DIRECTORY%' is taken.
    set /p FILE_NAME="Selected file name: "

    IF "%FILE_NAME%"=="" set FILE_NAME=%FIRST_FILE_IN_DIRECTORY%
    goto file_has_been_selected


:file_has_been_selected
    set FILE_TO_PROCESS=%INPUT_DIRECTORY%%FILE_NAME%

    IF not exist "%FILE_TO_PROCESS%" (
        echo The file '%FILE_TO_PROCESS%' doesn't exist.
        goto end
    )

    FOR %%i IN ("%FILE_TO_PROCESS%") DO (
        set FILE_EXTENSION=%%~xi
    )

    mkdir "%WORKDIR_PATH%init_data_for_analysis

    IF "%FILE_EXTENSION%"==".zip" goto handle_zip_format
    IF "%FILE_EXTENSION%"==".log" goto handle_json_and_log_format
    IF "%FILE_EXTENSION%"==".json" goto handle_json_and_log_format

    echo Unsupported file extension '%FILE_EXTENSION%' of file '%FILE_TO_PROCESS%'.
    goto end


:handle_zip_format
    echo Extracting logs from '%FILE_TO_PROCESS%' to '%WORKDIR_PATH%init_data_for_analysis\'
    mkdir "%WORKDIR_PATH%init_data_for_analysis
    %SEV_ZIP_PATH% x %FILE_TO_PROCESS% -o"%WORKDIR_PATH%init_data_for_analysis\"
    goto load_data


:handle_json_and_log_format
    echo Copying logs from '%FILE_TO_PROCESS%' to '%WORKDIR_PATH%init_data_for_analysis\'
    copy %FILE_TO_PROCESS% %WORKDIR_PATH%init_data_for_analysis\"
    set LOGS_TO_ANALYZE=%FILE_NAME%
    goto load_data


:load_data
    @rem get first file name from folder
    @rem ingesting multiple files is not supported
    for /r %%i in (%WORKDIR_PATH%init_data_for_analysis\*) do (
        IF NOT DEFINED LOGS_TO_ANALYZE SET "LOGS_TO_ANALYZE=%%~nxi"
        goto ingest
    )


:ingest
    echo %LOGS_TO_ANALYZE%
    echo Loading the logs from '%WORKDIR_PATH%init_data_for_analysis\%LOGS_TO_ANALYZE%' to PostgreSQL '%DATABASE_NAME%' database for analytics
    call %PYTHON_HOME%\python.exe %PY_SCRIPT_DIR%load_logs_to_database.py %DATABASE_NAME% %USER_NAME% %WORKDIR_PATH%init_data_for_analysis\%LOGS_TO_ANALYZE%
    goto end


:download_data
    @rem There should be an invocation of a program (java, python, whatever else)
    @rem that performing authorization to OpenEdu based on provided credentials in 'application.yml' file
    @rem and downloading logs from course, that is specified by id in 'application.yml' file
    echo TODO: implement missing functionality
    goto end


:end
    echo Exit.
    EXIT /B 1
    ENDLOCAL
