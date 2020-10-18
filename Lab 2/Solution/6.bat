@echo off
set /p sciezka= podaj sciezke:
echo %sciezka%
cd %sciezka%

call :drukujFoldery
goto :eof

:drukujFoldery
for %%f in (*) do echo %%f
for /D %%d in (*) do (
	echo %%d
    cd %%d
    call :drukujFoldery
	cd..
)
goto :eof