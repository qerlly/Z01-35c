@echo off

set /p sciezka= podaj sciezke:
echo %sciezka%

cd %sciezka%

set /p rozszerzenie= podaj rozszerzenie:
echo %rozszerzenie%

dir /B *%rozszerzenie%

goto :eof