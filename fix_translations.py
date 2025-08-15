#!/usr/bin/env python3
"""
Script para corrigir problemas no arquivo de tradução django.po
"""
import re
import os

def fix_po_file(input_file, output_file):
    print(f"Corrigindo arquivo de tradução: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrigir casos onde há múltiplos msgid antes de um msgstr
    pattern = r'(msgid "[^"]*")\s+(msgid "[^"]*")\s+(msgstr "[^"]*")'
    fixed_content = re.sub(pattern, r'\1\n\3', content)
    
    # Certificar que há uma linha em branco entre as entradas
    pattern = r'(msgstr "[^"]*")\n(msgid)'
    fixed_content = re.sub(pattern, r'\1\n\n\2', fixed_content)
    
    # Remover linhas em branco duplicadas
    while "\n\n\n" in fixed_content:
        fixed_content = fixed_content.replace("\n\n\n", "\n\n")
    
    # Escrever o arquivo corrigido
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Arquivo corrigido salvo em: {output_file}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po")
    output_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po.fixed")
    
    fix_po_file(input_file, output_file)
    print("Processamento concluído!")
