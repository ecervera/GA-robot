@echo off

rem Set AL_DIR to the root directory of the NaoQi SDK
SET AL_DIR=C:\UDK\naoqi-sdk-1.12.5-win32-vs2010
SET PATH=%PATH%;%AL_DIR%\bin;%AL_DIR%\lib

@echo on

set CONDA_FORCE_32BIT=1
activate pynao