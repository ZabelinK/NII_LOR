@echo off
set BIN_DIR=%~dp0
call %BIN_DIR%set_env.bat

@rem =======================Cleaning Working Directory===========================================
call %BIN_DIR%clean_workdir.bat
@rem ============================================================================================


@rem =======================Installing required soft=============================================
call %BIN_DIR%install_soft.bat
@rem ============================================================================================


@rem =======================Running application=====================================================
@rem At this point we are running the application
call %BIN_DIR%launch_application.bat
@rem ============================================================================================
