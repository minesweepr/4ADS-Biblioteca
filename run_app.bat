@echo off

echo =====================================
echo  Biblioteca Academica - 4ADS
echo =====================================
echo.

cd /d "%~dp0"

REM Checando se o Virtual Environment existe
if not exist ".venv\" (
    echo [SETUP] O Virtual Environment nao foi encontrado. Criando um Virtual Environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar um Virtual Environment.
        echo Garanta que seu Python está instalado e no PATH
        echo.
        pause
        exit /b 1
    )
    echo [SETUP] O Virtual Environment foi criado com sucesso.
    echo.
)

REM Ativando Virtual Environment
echo [1/3] Ativando Virtual Environment...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERRO: Falha ao ativar o Virtual Environment.
    echo.
    pause
    exit /b 1
)

REM Checando se as dependencias foram instaladas
echo [2/3] Instalando dependencias...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar as dependencias. Tente novamente.
    echo.
    pause
    exit /b 1
)
echo.
echo [SETUP] Dependencias instaladas com sucesso.
echo.

REM Inicializando  a aplicacao
echo [3/3] Inicializando a aplicacao.
echo.
python main.py

REM Checando saída
if errorlevel 1 (
    echo.
    echo A aplicacao fechou com um erro.
) else (
    echo.
    echo A aplicacao fechou com sucesso.
)

echo.
pause