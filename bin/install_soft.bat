@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat
@rem 
@rem set JAVA_DISTR_FILE=%SOFT_PATH%openjdk-11.0.2_windows-x64_bin.zip
@rem if exist %JAVA_DISTR_FILE% (
@rem   echo Extracting the JDK to '%JDK_PATH%'
@rem   %SEV_ZIP_PATH% x %JAVA_DISTR_FILE% -o"%JDK_PATH%"
@rem )

@rem echo Extracting PostgreSQL to '%POSTGRESQL_PATH%'
@rem %SEV_ZIP_PATH% x "%SOFT_PATH%postgresql-12.0-1-windows-x64-binaries.zip" -o"%POSTGRESQL_PATH%"
echo Extracting Python to '%PYTHON_PATH%'
%SEV_ZIP_PATH% x "%SOFT_PATH%python-3.7.4.zip" -o"%PYTHON_PATH%"

@rem call %JAVA_HOME%\java.exe -version
@rem call %POSTGRESQL_HOME%\psql --version
call %PYTHON_HOME%\python.exe -V

@rem =======================Install Python Packages=========================================
echo Installing Python packages with 'pip'
call %PYTHON_HOME%\python.exe %SOFT_PATH%PythonAddons\get-pip.py
call %PYTHON_HOME%\Scripts\pip.exe install psycopg2
call %PYTHON_HOME%\Scripts\pip install XlsxWriter
@rem for visualization
call %PYTHON_HOME%\Scripts\pip install tabulate
call %PYTHON_HOME%\Scripts\pip install plotly==4.1.0
call %PYTHON_HOME%\Scripts\pip install psutil requests
call %PYTHON_HOME%\Scripts\pip install pandas
call %PYTHON_HOME%\Scripts\pip install -U wxPython
call %PYTHON_HOME%\Scripts\pip install -U sounddevice
call %PYTHON_HOME%\Scripts\pip install -U soundfile
call %PYTHON_HOME%\Scripts\pip install -U requests
call %PYTHON_HOME%\Scripts\pip install -U numpy
@rem ============================================================================================
