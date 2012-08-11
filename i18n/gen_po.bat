@echo off
echo.
echo 生成 po 文件
echo.
python pygettext.py -a -v -d locals -o messages.po ../*.py ../templates/*.html
echo.
echo po 文件已生成
echo.
pause