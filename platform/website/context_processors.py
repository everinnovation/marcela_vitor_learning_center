def language_code(request):
    """
    Adds LANGUAGE_CODE to the template context.
    Normalizes language code format for consistency in templates.
    """
    # Get language from cookies or session or default
    lang_code = request.COOKIES.get('django_language', None)
    
    if not lang_code:
        lang_code = request.session.get('django_language', 'en')
        
    # Normalize language code format if needed
    if lang_code in ['pt_BR', 'pt-BR', 'pt_br', 'pt-br']:
        lang_code = 'pt-br'  # Format used in templates for comparison
    elif lang_code in ['en_US', 'en-US', 'en_us', 'en']:
        lang_code = 'en'  # Format used in templates for comparison
        
    return {
        'LANGUAGE_CODE': lang_code,
    }
