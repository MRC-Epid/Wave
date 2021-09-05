@echo off
setlocal

REM pyuic5 %~dp0\..\app\ui\app_2.ui -o %~dp0\..\app\ui\appgui_3.py

pyuic5 %~dp0\..\app\ui\settings_v3.ui -o %~dp0\..\app\ui\settingsgui_v3.py

REM pyuic5 %~dp0\..\app\ui\about.ui -o %~dp0\..\app\ui\aboutgui.py