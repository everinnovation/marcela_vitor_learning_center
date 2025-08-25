#!/usr/bin/env python
"""
Script de diagnóstico para problemas com WSGI.
Este script verifica a configuração do ambiente WSGI e Django.
"""
import os
import sys
import importlib

def check_django_installation():
    """Verifica se o Django está instalado corretamente."""
    print("Verificando instalação do Django...")
    try:
        import django
        print(f"Django versão {django.get_version()} encontrado.")
        return True
    except ImportError:
        print("Django não encontrado no PYTHONPATH!")
        return False

def check_settings_module():
    """Verifica se o módulo de configurações pode ser importado."""
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'app.settings')
    print(f"Verificando módulo de configurações: {settings_module}")
    
    try:
        importlib.import_module(settings_module)
        print(f"Módulo {settings_module} importado com sucesso.")
        return True
    except ImportError as e:
        print(f"Erro ao importar {settings_module}: {e}")
        return False

def check_wsgi_application():
    """Verifica se a aplicação WSGI pode ser carregada."""
    print("Verificando aplicação WSGI...")
    try:
        from django.core.wsgi import get_wsgi_application
        print("Módulo WSGI importado com sucesso.")
        
        try:
            # Tente carregar a aplicação WSGI
            application = get_wsgi_application()
            print("Aplicação WSGI carregada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao carregar a aplicação WSGI: {e}")
            return False
    except ImportError as e:
        print(f"Erro ao importar o módulo WSGI: {e}")
        return False

def check_pythonpath():
    """Verifica o PYTHONPATH atual."""
    print("\nPYTHONPATH atual:")
    for path in sys.path:
        print(f" - {path}")

def main():
    """Função principal de diagnóstico."""
    print("=== Diagnóstico de Configuração WSGI Django ===")
    print(f"Python versão: {sys.version}")
    print(f"Diretório atual: {os.getcwd()}")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'Não definido')}")
    
    check_pythonpath()
    
    django_ok = check_django_installation()
    settings_ok = check_settings_module()
    wsgi_ok = check_wsgi_application()
    
    print("\n=== Resumo do Diagnóstico ===")
    print(f"Django instalado: {'✓' if django_ok else '✗'}")
    print(f"Módulo de configurações: {'✓' if settings_ok else '✗'}")
    print(f"Aplicação WSGI: {'✓' if wsgi_ok else '✗'}")
    
    if django_ok and settings_ok and wsgi_ok:
        print("\n✅ Todos os testes passaram! A configuração WSGI parece estar correta.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os erros acima.")

if __name__ == "__main__":
    # Garante que o Django settings está definido
    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    
    # Adiciona o diretório atual ao path se não estiver lá
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    main()
