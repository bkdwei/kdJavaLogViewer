echo begin package
rm dist/main.exe
pyinstaller -w -F main.py --add-dat="data;data"
echo finish package
start dist
pause