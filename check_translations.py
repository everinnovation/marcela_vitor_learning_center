#!/usr/bin/env python3
"""
Script para verificar a saúde do sistema de tradução
Verifica se o arquivo .mo contém todas as traduções e identifica problemas potenciais
"""
import os
import subprocess
import re
from datetime import datetime

def check_po_file(po_file_path):
    """Verifica a integridade do arquivo .po"""
    if not os.path.exists(po_file_path):
        return False, "Arquivo .po não encontrado"
    
    # Verificar formato do cabeçalho
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se há entradas duplicadas
    msgids = re.findall(r'msgid "(.*?)"', content, re.DOTALL)
    unique_msgids = set(msgids)
    
    if len(msgids) != len(unique_msgids):
        return False, f"Encontradas {len(msgids) - len(unique_msgids)} entradas duplicadas"
    
    # Verificar quebras de linha dentro de strings
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('msgid "') or line.startswith('msgstr "'):
            if not line.endswith('"') and i+1 < len(lines) and not lines[i+1].startswith('"'):
                return False, f"Quebra de linha encontrada na string na linha {i+1}"
    
    return True, f"Arquivo .po válido com {len(msgids)} entradas"

def check_mo_file(mo_file_path):
    """Verifica a integridade do arquivo .mo"""
    if not os.path.exists(mo_file_path):
        return False, "Arquivo .mo não encontrado"
    
    # Verificar o número de mensagens no arquivo .mo
    try:
        result = subprocess.run(['file', mo_file_path], capture_output=True, text=True)
        output = result.stdout
        
        match = re.search(r'(\d+) messages', output)
        if match:
            num_messages = int(match.group(1))
            if num_messages < 10:
                return False, f"Arquivo .mo contém apenas {num_messages} mensagens, o que parece insuficiente"
            return True, f"Arquivo .mo contém {num_messages} mensagens"
        else:
            return False, "Não foi possível determinar o número de mensagens no arquivo .mo"
    except Exception as e:
        return False, f"Erro ao verificar arquivo .mo: {str(e)}"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    po_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po")
    mo_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.mo")
    
    print(f"=== Relatório de Saúde do Sistema de Tradução ===")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"===================================================")
    
    po_ok, po_message = check_po_file(po_file)
    print(f"Arquivo PO: {'✅' if po_ok else '❌'} {po_message}")
    
    mo_ok, mo_message = check_mo_file(mo_file)
    print(f"Arquivo MO: {'✅' if mo_ok else '❌'} {mo_message}")
    
    print(f"===================================================")
    print(f"Status geral: {'✅ Saudável' if po_ok and mo_ok else '❌ Problemas detectados'}")
    
    if not (po_ok and mo_ok):
        print("\nRecomendações:")
        if not po_ok:
            print("- Execute o script fix_duplicates.py para corrigir problemas no arquivo .po")
        if not mo_ok:
            print("- Recompile o arquivo de tradução com: docker-compose exec web-project python manage.py compilemessages")
    
    print(f"===================================================")

if __name__ == "__main__":
    main()
