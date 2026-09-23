@echo off
chcp 65001 >nul
echo =======================================================
echo   DSH Claude 风格推理滑块插件一键安装脚本
echo =======================================================
echo.
echo 正在安装插件至 DSH Desktop 配置文件...
call dsh plugin --profile desktop add link:%~dp0
if %errorlevel% neq 0 (
    echo [警告] Desktop 挂载可能需要重启 DSH。
)

echo.
echo 正在安装插件至 DSH Web 配置文件...
call dsh plugin --profile web add link:%~dp0
if %errorlevel% neq 0 (
    echo [提示] Web 挂载完成。
)

echo.
echo =======================================================
echo   安装完毕！请完全重启 DSH (DeepSeek Harness) 客户端。
echo =======================================================
pause
