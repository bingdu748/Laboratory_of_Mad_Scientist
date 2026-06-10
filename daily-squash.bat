@echo off
setlocal enabledelayedexpansion

:: ============================================
:: Windows 每日 Git 提交合并脚本（批处理包装器）
:: 调用 Git Bash 执行 daily-squash.sh
:: ============================================

:: 配置参数
set "SCRIPT_DIR=%~dp0"
set "REPO_DIR=%SCRIPT_DIR%"
set "LOG_FILE=%SCRIPT_DIR%daily-squash.log"
set "GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe"

:: 检查 Git Bash 是否存在
if not exist "%GIT_BASH_PATH%" (
    echo [ERROR] Git Bash not found at: %GIT_BASH_PATH%
    echo Please install Git for Windows and update GIT_BASH_PATH in this script
    pause
    exit /b 1
)

:: 检查脚本文件是否存在
if not exist "%SCRIPT_DIR%daily-squash.sh" (
    echo [ERROR] daily-squash.sh not found at: %SCRIPT_DIR%daily-squash.sh
    pause
    exit /b 1
)

:: 获取当前时间
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do (
    set "YEAR=%%d"
    set "MONTH=%%b"
    set "DAY=%%c"
)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set "HOUR=%%a"
    set "MINUTE=%%b"
    set "SECOND=%%c"
)
set "TIMESTAMP=%YEAR%-%MONTH%-%DAY% %HOUR%:%MINUTE%:%SECOND%"

:: 记录日志
echo [%TIMESTAMP%] Starting daily-squash script... >> "%LOG_FILE%"

:: 切换到仓库目录
cd /d "%REPO_DIR%"

:: 执行 Bash 脚本
"%GIT_BASH_PATH%" --login -i -c "cd '%REPO_DIR%' && ./daily-squash.sh"

:: 检查执行结果
if %errorlevel% equ 0 (
    echo [%TIMESTAMP%] Script executed successfully >> "%LOG_FILE%"
    echo [SUCCESS] Daily squash completed successfully
) else (
    echo [%TIMESTAMP%] Script failed with error: %errorlevel% >> "%LOG_FILE%"
    echo [ERROR] Script failed. Check log file for details: %LOG_FILE%
    exit /b 1
)

endlocal