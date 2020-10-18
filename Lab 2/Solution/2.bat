@echo off
set /p sciezka= podaj sciezke:
echo %sciezka%

XCOPY %sciezka% /t /e

goto :eof