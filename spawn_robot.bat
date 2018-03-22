@echo off

rem Set AL_DIR to the root directory of the NaoQi SDK
SET AL_DIR=C:\UDK\naoqi-sdk-1.12.5-win32-vs2010
SET PATH=%PATH%;%AL_DIR%\bin;%AL_DIR%\lib
SET PYTHONPATH=%AL_DIR%\lib

@echo on

usarnaoqi labyrinth_crawlconfig.xml