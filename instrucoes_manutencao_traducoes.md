# Guia de Manutenção de Traduções - Marcela Vitor Learning Center

## Visão Geral do Sistema de Traduções

O site do Marcela Vitor Learning Center utiliza o sistema de internacionalização (i18n) do Django para oferecer conteúdo em inglês e português. Este guia descreve as melhores práticas para manter e atualizar as traduções.

## Estrutura dos Arquivos de Tradução

- `/platform/locale/pt_BR/LC_MESSAGES/django.po`: Arquivo de tradução principal (editável)
- `/platform/locale/pt_BR/LC_MESSAGES/django.mo`: Arquivo de tradução compilado (gerado automaticamente)

## Ferramentas de Suporte

### Scripts Disponíveis

- `fix_translations.py`: Corrige problemas de formatação básicos no arquivo de tradução
- `fix_duplicates.py`: Remove entradas duplicadas preservando a ordem
- `fix_dashes.py`: Remove separadores inválidos (--) do arquivo de tradução
- `check_translations.py`: Verifica estatísticas gerais do arquivo de tradução
- `check_untranslated.py`: Identifica strings não traduzidas em uma página específica

### Uso do Verificador de Strings Não Traduzidas

Para identificar strings não traduzidas em uma página específica:

```bash
python check_untranslated.py caminho/para/template.html caminho/para/django.po
```

Exemplo:
```bash
python check_untranslated.py platform/templates/front/home.html platform/locale/pt_BR/LC_MESSAGES/django.po
```

O script mostrará a porcentagem de conclusão e listará quaisquer strings que ainda precisam ser traduzidas.

### Correção de Problemas de Formatação

Se o arquivo de tradução apresentar erros de sintaxe ao compilar:

```bash
python fix_dashes.py  # Remove separadores inválidos '--'
python fix_translations.py  # Corrige problemas gerais de formatação
```

## Fluxo de Trabalho para Atualizar Traduções

### 1. Preparação do Ambiente

Certifique-se de que o pacote `gettext` está instalado no contêiner Docker:

```bash
docker-compose exec web-project apt-get update && apt-get install -y gettext
```

### 2. Extrair Novas Strings para Tradução

Quando novas strings são adicionadas ao código, execute:

```bash
docker-compose exec web-project python manage.py makemessages -l pt_BR
```

Este comando atualiza o arquivo `django.po` com as novas strings que precisam ser traduzidas.

### 3. Edição das Traduções

Edite o arquivo `django.po` para adicionar traduções para as novas strings. Cada entrada segue este formato:

```
msgid "Texto em inglês"
msgstr "Texto em português"
```

**Importante:** Mantenha o formato do arquivo intacto. Não adicione quebras de linha dentro das strings nem remova as aspas.

### 4. Compilação das Traduções

Após editar o arquivo `django.po`, compile-o para gerar o arquivo `django.mo`:

```bash
docker-compose exec web-project python manage.py compilemessages
```

### 5. Aplicação das Mudanças

Reinicie o contêiner para aplicar as mudanças:

```bash
docker-compose restart web-project
```

## Resolução de Problemas Comuns

### Erro: "duplicate message definition"

Se encontrar erros de duplicação durante a compilação, você pode usar o script `fix_duplicates.py` para corrigir o arquivo:

```bash
python3 fix_duplicates.py
```

### Erro: "end-of-line within string"

Este erro ocorre quando há quebras de linha dentro das strings. Certifique-se de que cada string esteja em uma única linha:

```
# Correto
msgid "Esta é uma string longa que deve estar em uma única linha mesmo que seja muito extensa."
msgstr "This is a long string that should be on a single line even if it's very extensive."

# Incorreto
msgid "Esta é uma string longa
que não deve ter quebras de linha."
msgstr "This is a long string
that should not have line breaks."
```

## Melhores Práticas

1. **Marcação de Strings para Tradução**: Sempre envolva strings destinadas à tradução com a tag `{% trans "..." %}` nos templates.

2. **Consistência Terminológica**: Mantenha consistência na tradução de termos específicos da escola.

3. **Backup Regular**: Faça backup do arquivo `django.po` antes de fazer alterações significativas.

4. **Teste as Traduções**: Após atualizar as traduções, teste o site em ambos os idiomas.

5. **Documentação**: Mantenha um registro das traduções adicionadas ou modificadas no arquivo `translation_updates_summary.md`.

6. **Verificação de Completude**: Use o script `check_untranslated.py` para verificar se há strings não traduzidas em uma página específica antes de publicar.

## Estatísticas Atuais

- Total de mensagens traduzidas: 217 (14 de agosto de 2025)
- Páginas com 100% de tradução: Home, About Us, Programs, Contact, Schedule, Footer
- Arquivos .mo e .po sincronizados e funcionando corretamente

## Contato para Suporte

Em caso de dúvidas ou problemas com o sistema de tradução, entre em contato com a equipe de desenvolvimento.

---

Última atualização: 14 de agosto de 2025
