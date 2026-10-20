@echo off
chcp 65001 >nul
title Consulta Empresas - Dashboard CNPJ
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale em https://www.python.org/downloads/
    echo        e marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo Criando ambiente virtual pela primeira vez...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
)

echo Verificando dependencias...
"venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar as dependencias. Verifique sua conexao com a internet.
    pause
    exit /b 1
)

echo.
echo Iniciando a aplicacao em http://localhost:8501
echo Para encerrar, feche esta janela ou pressione Ctrl+C.
echo.
"venv\Scripts\python.exe" -m streamlit run app.py

pause
