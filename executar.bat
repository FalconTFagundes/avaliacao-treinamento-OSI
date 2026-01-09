@echo off
chcp 65001 >nul
title BigCard Training - Servidor

echo.
echo ========================================================================
echo   BIGCARD TRAINING - INICIANDO SERVIDOR
echo ========================================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3 em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica se o arquivo server.py existe
if not exist "server.py" (
    echo [ERRO] Arquivo server.py nao encontrado!
    echo.
    echo Certifique-se de que este arquivo .bat esta na mesma pasta que server.py
    echo.
    pause
    exit /b 1
)

REM Verifica se o arquivo perguntas.txt existe
if not exist "perguntas.txt" (
    echo [ERRO] Arquivo perguntas.txt nao encontrado!
    echo.
    echo Certifique-se de que o arquivo perguntas.txt esta na mesma pasta
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo [OK] Arquivos verificados
echo.
echo Iniciando servidor...
echo.

REM Executa o servidor
python server.py

REM Se chegou aqui, é porque o servidor foi parado
echo.
echo ========================================================================
echo   SERVIDOR PARADO
echo ========================================================================
echo.
pause