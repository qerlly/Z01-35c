@echo off

set /p n= podaj liczbe n:

if %n% == 0 (
	echo 0
) else if %n% == 1 (
	echo 1
) else if %n% == 2 (
	echo 1
) else (
	call :power %n%
	goto :eof
)

:power
setlocal
set counter=%1
set buf=1
set firstFib=0 
set secondFib=1  
echo %firstFib%
:power_loop
if %counter% gtr 1 (
	set /a buf=firstFib+secondFib
	set /a counter=counter-1
	set /a firstFib=secondFib
	set /a secondFib=buf
	echo %buf%
	goto power_loop
)
endlocal
goto :eof