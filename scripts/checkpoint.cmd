@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."

echo ============================================
echo   dsh-claude-slider  存档检查点
echo ============================================
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo [错误] 这里不是 git 仓库，请先在项目根目录执行 git init
  pause
  exit /b 1
)

echo [1/3] 语法检查...
node --check lib\client.js
if errorlevel 1 (
  echo [中止] lib\client.js 语法错误，未提交。
  pause
  exit /b 1
)

echo [2/3] 地雷扫描（引用但未声明的常量）...
node scripts\check-undefined.cjs lib\client.js
if errorlevel 1 (
  echo [中止] 发现未定义符号，请先修复再存档。
  pause
  exit /b 1
)

echo [3/3] 提交...
git add -A
git commit -m "checkpoint: %date% %time%" 
if errorlevel 1 (
  echo [提示] 没有需要提交的改动。
) else (
  echo.
  echo 已存档。撤回本次改动： git reset --soft HEAD~1
  echo 丢弃全部改动：     git checkout -- .
)

echo.
pause
