@echo off

NET SESSION

if %errorLevel% == 0 (
    echo prawa administratora nadane
) else (
    echo prawa administratora nie nadane
)

goto :eof