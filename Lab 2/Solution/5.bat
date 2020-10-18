@echo off

set /p sciezka= podaj sciezke do pliku wideo:
echo %sciezka%

cd %sciezka%

set /p nazwa= podaj nazwe wideo:
echo %nazwa%

FFmpeg -i %nazwa% -vcodec png miniature.png

goto :eof