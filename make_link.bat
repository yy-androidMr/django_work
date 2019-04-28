%~d0
CD  %~dp0

rd /s /q %CD%\exe\resources\config\shared
rd /s /q %CD%\exe\resources\level

rd /s /q %CD%\client\assetbundles\cdn\assetbundles
@echo off


set "str=%CD%"
:loop1
set "newstr=%newstr%%str:~-1%"
set "str=%str:~0,-1%"
if "%str%" neq "" goto loop1
echo %newstr%

for /f "delims=\" %%i in ("%newstr%") do (
    set version=%%i
)

echo %version%

set "str2=%version%"
:loop2
set "newstr2=%newstr2%%str2:~-1%"
set "str2=%str2:~0,-1%"
if "%str2%" neq "" goto loop2
set version=%newstr2%
echo %version%


echo %CD%|findstr "branches">nul&&(
     
    set path_pre=..\..\..\mr\b\%version%

)||(
    set path_pre=..\..\mr\Resources
)



mklink /D %CD%\client\assetbundles\cdn\assetbundles %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\android\assetbundles

rd /s /q %CD%\client\assetbundles\editorCdn\assetbundles
rd /s /q %CD%\client\assetbundles\cdn\assetbundles\audio\bgm
rd /s /q %CD%\client\assetbundles\cdn\assetbundles\audio\sound_effect
rd /s /q %CD%\client\assetbundles\cdn\assetbundles\config
rd /s /q %CD%\client\assetbundles\cdn\assetbundles\level

mklink /D %CD%\client\assetbundles\editorCdn\assetbundles %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\windows\assetbundles

mklink /D %CD%\client\assetbundles\cdn\assetbundles\audio\bgm %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\audio\bgm
mklink /D %CD%\client\assetbundles\cdn\assetbundles\audio\sound_effect %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\audio\sound_effect
mklink /D %CD%\client\assetbundles\cdn\assetbundles\config %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\config
mklink /D %CD%\client\assetbundles\cdn\assetbundles\level %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\level
mklink /D %CD%\client\assetbundles\cdn\assetbundles\luascript %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\luascript
mklink /D %CD%\exe\resources\config\shared %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\xml_sources\config\shared
mklink /D %CD%\exe\resources\level %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\level_source\level
mklink /D %CD%\exe\resources\config\shared\tencent_xg %CD%\client_build_config\config\shared\tencent_xg

mklink /D %CD%\client\GameLuaProject\luascript %CD%\%path_pre%\ResourcePublish\CDN\SourceFiles\crossplatform\luascript
pause