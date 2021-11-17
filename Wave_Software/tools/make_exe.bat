@echo off
setlocal

set NAME=run

cd %~dp0\..
pyinstaller.exe run.py --onefile --paths C:\Users\Cobin\PycharmProjects\pythonProject\venv\Lib\site-packages --clean -i=Logo.svg --noconsole --add-data app\data;app\data --hidden-import=statsmodels.tsa.statespace._kalman_filter --hidden-import=statsmodels.tsa.statespace._kalman_smoother --hidden-import=statsmodels.tsa.statespace._representation --hidden-import=statsmodels.tsa.statespace._simulation_smoother --hidden-import=statsmodels.tsa.statespace._statespace --hidden-import=statsmodels.tsa.statespace._tools --hidden-import=statsmodels.tsa.statespace.tools --hidden-import=statsmodels.tsa.statespace._filters._conventional --hidden-import=statsmodels.tsa.statespace._filters._inversions --hidden-import=statsmodels.tsa.statespace._filters._univariate --hidden-import=statsmodels.tsa.statespace._smoothers._alternative --hidden-import=statsmodels.tsa.statespace._smoothers._classical --hidden-import=statsmodels.tsa.statespace._smoothers._conventional --hidden-import=statsmodels.tsa.statespace._smoothers._univariate --hidden-import=statsmodels.tsa.statespace._smoothers._univariate_diffuse --hidden-import=statsmodels.tsa.statespace._filters._univariate_diffuse
move dist\%NAME%.exe %~dp0\
rmdir /S /Q build dist
cd %~dp0