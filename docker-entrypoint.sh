#!/bin/bash
# Este script é executado no contêiner Docker antes de iniciar a aplicação

set -e  # Falha em caso de erro

echo "=== Script de inicialização do Learning Center ==="
echo "Verificando ambiente..."

# Verifica se as variáveis de ambiente estão definidas
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
  echo "DJANGO_SETTINGS_MODULE não definido, usando valor padrão: app.settings"
  export DJANGO_SETTINGS_MODULE="app.settings"
fi

# Adiciona o diretório do projeto ao PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/app

# Verifica se o Django está instalado
echo "Verificando instalação do Django..."
python -c "import django; print(f'Django versão {django.get_version()} encontrado.')" || {
  echo "Django não encontrado! Instalando dependências..."
  pip install -r requirements.txt
}

# Tenta acessar o banco de dados
echo "Verificando conexão com o banco de dados..."
python -c "from django.db import connection; connection.ensure_connection()" || {
  echo "Erro na conexão com o banco de dados!"
  echo "Aguardando 5 segundos e tentando novamente..."
  sleep 5
  python -c "from django.db import connection; connection.ensure_connection()" || {
    echo "Falha persistente na conexão com o banco de dados!"
  }
}

# Aplica migrações pendentes
echo "Aplicando migrações..."
python manage.py migrate

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Compila as traduções
echo "Compilando arquivos de tradução..."
python manage.py compilemessages

echo "=== Ambiente verificado e configurado ==="
echo "Iniciando aplicação..."

# Executa o comando passado para o script
exec "$@"
