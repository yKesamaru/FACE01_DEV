@ECHO OFF

REM Command file for Sphinx documentation
REM This file is a Windows batch file, if you want to use a Makefile with 
REM this configuration, use make.bat.

set SPHINXOPTS=
set SPHINXBUILD=sphinx-build
set SOURCEDIR=docs
set BUILDDIR=docs\_build

if "%1" == "" (
    %SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
) else (
    %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
)
