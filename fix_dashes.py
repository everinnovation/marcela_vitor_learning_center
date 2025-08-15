#!/usr/bin/env python3
"""
Script to fix the `--` syntax errors in the django.po file
"""
import os

def fix_dashes_in_po_file(input_file, output_file):
    print(f"Fixing translation file by removing dashes: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove lines that contain only '--'
    fixed_lines = []
    for line in lines:
        if line.strip() != '--':
            fixed_lines.append(line)
    
    # Ensure there's a blank line between msgstr and msgid
    result_lines = []
    for i, line in enumerate(fixed_lines):
        result_lines.append(line)
        if i < len(fixed_lines) - 1:
            if line.startswith('msgstr ') and fixed_lines[i+1].startswith('msgid '):
                result_lines.append('\n')
    
    # Write the fixed file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)
    
    print(f"Fixed file saved to: {output_file}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po")
    output_file = os.path.join(base_dir, "platform/locale/pt_BR/LC_MESSAGES/django.po.fixed")
    
    fix_dashes_in_po_file(input_file, output_file)
    print("Processing complete!")
