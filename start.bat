@echo off

:: 确保脚本以UTF-8编码运行
chcp 65001 > nul

echo 欢迎使用GitBlog - 基于GitHub Issues的博客系统
echo =======================================

:: 检查Python是否安装
where python > nul 2> nul
if %errorlevel% neq 0 (
    echo 错误: Python 未安装，请先安装Python 3.7+
    pause
    exit /b 1
)

:: 检查pip是否安装
python -m pip --version > nul 2> nul
if %errorlevel% neq 0 (
    echo 错误: pip 未安装，请先安装pip
    pause
    exit /b 1
)

:: 安装依赖
echo 正在安装项目依赖...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败，请检查网络连接或requirements.txt文件
    pause
    exit /b 1
)

echo 依赖安装成功！

:: 提示用户输入GitHub Token和仓库名称
echo.
echo 请输入您的GitHub Personal Access Token (获取地址: https://github.com/settings/tokens)
echo 注意: Token需要有repo权限
set /p GITHUB_TOKEN=

echo.
echo 请输入您的GitHub仓库名称 (格式: owner/repo)
set /p REPO_NAME=

:: 验证输入
echo.
echo 正在验证输入信息...
if "%GITHUB_TOKEN%" == "" ( 
    echo 错误: GitHub Token不能为空
    pause
    exit /b 1
)

if "%REPO_NAME%" == "" (
    echo 错误: 仓库名称不能为空
    pause
    exit /b 1
)

:: 运行博客生成器
echo.
echo 正在运行博客生成器...
python blog_generator.py "%GITHUB_TOKEN%" "%REPO_NAME%"

if %errorlevel% equ 0 (
echo.
echo 🎉 博客生成成功！请查看README.md文件
echo.
echo 下一步建议：
echo 1. 将项目推送到GitHub仓库
echo 2. 配置GitHub Actions自动更新
echo 3. 创建第一个Issue作为博客文章
) else (
echo.
echo 错误: 博客生成失败，请查看错误信息
)

pause