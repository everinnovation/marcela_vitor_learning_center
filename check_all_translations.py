#!/usr/bin/env python3
import os
import re
import polib
from pathlib import Path

def extract_strings_from_template(template_path):
    """Extract translatable strings from a Django template."""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    strings = set()
    
    # Pattern for {% trans "..." %}
    trans_pattern = r'{%\s*trans\s+["\']([^"\']+)["\']\s*%}'
    strings.update(re.findall(trans_pattern, content))
    
    # Pattern for {% blocktrans %}...{% endblocktrans %}
    blocktrans_pattern = r'{%\s*blocktrans[^%]*%}(.*?){%\s*endblocktrans\s*%}'
    for match in re.finditer(blocktrans_pattern, content, re.DOTALL):
        block_content = match.group(1).strip()
        # Remove HTML tags and extra whitespace
        clean_content = re.sub(r'<[^>]+>', '', block_content)
        clean_content = ' '.join(clean_content.split())
        if clean_content:
            strings.add(clean_content)
    
    return strings

def get_translated_strings(po_file_path):
    """Get all translated strings from a .po file."""
    po = polib.pofile(po_file_path)
    translated = set()
    untranslated = set()
    
    for entry in po:
        if entry.msgstr:
            translated.add(entry.msgid)
        else:
            untranslated.add(entry.msgid)
    
    return translated, untranslated

def main():
    # Base directory
    base_dir = Path('/Users/everinnovation/Documents/CODE/LEARNING CENTER/marcela_vitor_learning_center/platform')
    
    # Templates directory
    templates_dir = base_dir / 'templates'
    
    # PO file
    po_file = base_dir / 'locale' / 'pt_BR' / 'LC_MESSAGES' / 'django.po'
    
    if not po_file.exists():
        print(f"PO file not found: {po_file}")
        return
    
    # Get all translated strings
    translated_strings, untranslated_strings = get_translated_strings(po_file)
    
    print("=== TRANSLATION STATUS ===\n")
    print(f"Total translated strings: {len(translated_strings)}")
    print(f"Total untranslated strings: {len(untranslated_strings)}")
    
    if untranslated_strings:
        print("\n=== UNTRANSLATED STRINGS ===")
        for string in sorted(untranslated_strings):
            print(f"  - '{string}'")
    
    # Check specific templates
    template_files = [
        'front/home.html',
        'front/about.html', 
        'front/programs.html',
        'front/resume.html',
        'front/calendar.html',
        'front/schedule.html',
        'front/contact.html',
        'parciais/menu.html',
        'parciais/footer.html'
    ]
    
    print("\n=== TEMPLATE-SPECIFIC ANALYSIS ===")
    
    for template_name in template_files:
        template_path = templates_dir / template_name
        
        if not template_path.exists():
            print(f"\nTemplate not found: {template_path}")
            continue
        
        template_strings = extract_strings_from_template(template_path)
        
        if not template_strings:
            print(f"\n{template_name}: No translatable strings found")
            continue
        
        missing = template_strings - translated_strings
        
        total = len(template_strings)
        translated_count = total - len(missing)
        percentage = (translated_count / total * 100) if total > 0 else 0
        
        print(f"\n{template_name}: {translated_count}/{total} ({percentage:.1f}%)")
        
        if missing:
            print("  Missing translations:")
            for string in sorted(missing):
                print(f"    - '{string}'")

if __name__ == "__main__":
    main()
