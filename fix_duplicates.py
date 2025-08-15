#!/usr/bin/env python3
"""
Script para remover entradas duplicadas do arquivo de tradução django.po
"""
import re
import os
from collections import OrderedDict

def fix_po_file(input_file, output_file):
    print(f"Corrigindo arquivo de tradução: {input_file}")
    
    # Lê o cabeçalho e o corpo do arquivo
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Separa o cabeçalho e o corpo
    header_match = re.match(r'(.*?msgid "".*?msgstr "".*?)(\n\n.*)', content, re.DOTALL)
    if not header_match:
        print("Formato de cabeçalho não reconhecido.")
        return
    
    header = header_match.group(1)
    body = header_match.group(2)
    
    # Extrai todas as entradas de tradução
    pattern = r'\nmsgid "(.*?)"\nmsgstr "(.*?)"'
    entries = re.findall(pattern, body, re.DOTALL)
    
    # Remove duplicatas preservando a ordem
    unique_entries = OrderedDict()
    for msgid, msgstr in entries:
        if msgid not in unique_entries:
            unique_entries[msgid] = msgstr
    
    # Reconstrói o arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header + "\n\n")
        for msgid, msgstr in unique_entries.items():
            f.write(f'msgid "{msgid}"\nmsgstr "{msgstr}"\n\n')
    
    print(f"Arquivo corrigido salvo em: {output_file}")
    print(f"Número de entradas originais: {len(entries)}")
    print(f"Número de entradas únicas: {len(unique_entries)}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po")
    output_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po.fixed")
    
    fix_po_file(input_file, output_file)
    print("Processamento concluído!")
