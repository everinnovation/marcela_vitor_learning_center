#!/usr/bin/env python3
"""
Script to identify remaining untranslated strings in a Django template.
This script parses a Django template file and identifies all strings
wrapped in {% trans "..." %} tags, then compares them with entries in
the translation file to find which ones are missing translations.
"""

import re
import os
import argparse
import polib

def extract_trans_strings(template_file):
    """Extract all strings wrapped in {% trans "..." %} tags from a template file."""
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regular expression to match {% trans "..." %} and {% blocktrans %}...{% endblocktrans %}
    trans_pattern = r'{%\s*trans\s*"([^"]+)"\s*%}'
    blocktrans_pattern = r'{%\s*blocktrans\s*%}(.*?){%\s*endblocktrans\s*%}'
    
    # Find all matches
    trans_matches = re.findall(trans_pattern, content)
    blocktrans_matches = re.findall(blocktrans_pattern, content, re.DOTALL)
    
    # Combine all matches
    all_matches = trans_matches + blocktrans_matches
    
    # Clean up matches (strip whitespace)
    return [match.strip() for match in all_matches]

def check_translations(template_file, po_file):
    """Check which strings from the template are not translated in the PO file."""
    template_strings = extract_trans_strings(template_file)
    
    # Load the PO file
    po = polib.pofile(po_file)
    
    # Get all msgids from the PO file
    translated_msgids = set(entry.msgid for entry in po if entry.msgstr)
    
    # Find untranslated strings
    untranslated = [s for s in template_strings if s not in translated_msgids]
    
    return {
        'total': len(template_strings),
        'translated': len(template_strings) - len(untranslated),
        'untranslated': untranslated
    }

def main():
    parser = argparse.ArgumentParser(description='Check for untranslated strings in Django templates')
    parser.add_argument('template', help='Path to the Django template file')
    parser.add_argument('po_file', help='Path to the .po translation file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.template):
        print(f"Error: Template file {args.template} does not exist")
        return
    
    if not os.path.exists(args.po_file):
        print(f"Error: PO file {args.po_file} does not exist")
        return
    
    result = check_translations(args.template, args.po_file)
    
    print(f"Template: {args.template}")
    print(f"Translation file: {args.po_file}")
    print(f"Total strings to translate: {result['total']}")
    print(f"Translated strings: {result['translated']}")
    print(f"Translation completion: {result['translated'] / result['total'] * 100:.2f}%")
    
    if result['untranslated']:
        print("\nUntranslated strings:")
        for i, s in enumerate(result['untranslated'], 1):
            print(f"{i}. \"{s}\"")
    else:
        print("\nAll strings are translated!")

if __name__ == "__main__":
    main()
