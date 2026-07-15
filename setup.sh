#!/bin/bash
# Script de setup para Makis Digital - Base Central | makisdigital.com
# Execute com: source setup.sh

echo "🚀 Iniciando setup do Makis Digital - Base Central"
echo "---------------------------------------------"

# Ativa o ambiente virtual
source venv/bin/activate

# Gera SECRET_KEY segura
echo "🔑 Gerando sua SECRET_KEY..."
python -c "from django.core.management.utils import get_random_secret_key; print('\nCole essa chave no seu .env:\nSECRET_KEY='+get_random_secret_key()+'\n')"

echo "📋 Próximos passos:"
echo "1. Crie o banco MySQL: CREATE DATABASE base_central CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "2. Atualize o .env com a SECRET_KEY gerada acima"
echo "3. Execute: python manage.py migrate"
echo "4. Crie superusuário: python manage.py createsuperuser"
echo "5. Inicie o servidor: python manage.py runserver"
echo "---------------------------------------------"
echo "✅ Makis Digital - Base Central pronto!"