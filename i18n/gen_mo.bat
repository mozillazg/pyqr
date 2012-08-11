@echo off
echo.
echo 生成 mo 文件
echo.
python msgfmt.py -o en_US/LC_MESSAGES/messages.mo en_US/LC_MESSAGES/messages.po
python msgfmt.py -o zh_CN/LC_MESSAGES/messages.mo zh_CN/LC_MESSAGES/messages.po
echo mo 文件已生成
echo.
pause