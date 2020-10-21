@echo off

set /p n= podaj liczbe n:

call :power %n%
goto :eof

:power
setlocal
set counter=%1
set buf=1  
:power_loop
if %counter% gtr 1 (
	set /a buf*=counter
	set /a counter=counter-1
	goto power_loop
)
echo %buf%
endlocal
goto :eof