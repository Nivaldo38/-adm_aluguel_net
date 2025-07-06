@echo off
echo ========================================
echo    CONFIGURADOR DS4 - DOCUSIGN
echo ========================================
echo.
echo Para configurar o DS4, você precisa:
echo 1. Criar conta em https://developers.docusign.com/
echo 2. Obter suas credenciais
echo 3. Configurar as variáveis abaixo
echo.
echo Configure as variáveis de ambiente:
echo.
set /p DS4_ACCOUNT_ID="Digite seu Account ID: "
set /p DS4_INTEGRATION_KEY="Digite sua Integration Key: "
set /p DS4_USER_ID="Digite seu User ID: "
set /p DS4_PRIVATE_KEY_PATH="Digite o caminho para sua private key (.pem): "
echo.
echo Configurando variáveis de ambiente...
setx DS4_ACCOUNT_ID "%DS4_ACCOUNT_ID%"
setx DS4_INTEGRATION_KEY "%DS4_INTEGRATION_KEY%"
setx DS4_USER_ID "%DS4_USER_ID%"
setx DS4_PRIVATE_KEY_PATH "%DS4_PRIVATE_KEY_PATH%"
echo.
echo ✅ Variáveis configuradas!
echo.
echo Para testar, execute:
echo python testar_ds4.py
echo.
pause 