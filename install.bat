@echo off
CALL :NORMALIZEPATH "D:\Anaconda3\envs\stable-diffusion\python.exe"
if exist "D:\Anaconda3\envs\stable-diffusion\python.exe" (
    echo Custom Python build of ComfyUI standalone executable detected:
    echo "%RETVAL%"
    echo --------------------------------------------------
    D:\Anaconda3\envs\stable-diffusion\python.exe install.py %1
) else (
    for /f "tokens=*" %%i in ('where python') do set "PYTHON_PATH=%%i" & goto :done
    :done
    echo Custom Python not found. Use system's Python executable instead:
    echo %PYTHON_PATH%
    echo --------------------------------------------------
    python.exe install.py %1
)

:NORMALIZEPATH
    SET RETVAL=%~f1
    EXIT /B
