@echo off
setlocal

set NAME=run

cd %~dp0\..
pyinstaller.exe %NAME%.py --onefile --hidden-import=pampro --hidden-import=pandas --paths C:\Users\Cobin\PycharmProjects\pythonProject\venv\Lib\site-packages --icon=logo_2.ico --clean --noconsole --add-data app\data;app\data
move dist\%NAME%.exe %~dp0\
rmdir /S /Q build dist
cd %~dp0
