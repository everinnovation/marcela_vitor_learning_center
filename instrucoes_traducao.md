## Instruções para resolver problemas de tradução

### 1. Alterações realizadas
- Corrigimos o menu alterando "resume Us" para "Contact Us"
- Adicionamos traduções faltantes para a página About (missão)
- Compilamos o arquivo de tradução (django.mo)
- Corrigimos o problema com a seleção do idioma inglês (bandeira EUA)

### 2. Correções para o seletor de idiomas
As seguintes correções foram aplicadas para resolver o problema da alternância de idiomas:

1. **Formato do código de idioma**: 
   - Atualizado o código de idioma português para `pt_BR` (formato aceito pelo Django) no código JavaScript
   - Anteriormente estava usando `pt-br`, que pode causar inconsistências

2. **Context Processor**:
   - Melhorado o context processor para lidar com mais variantes dos códigos de idioma
   - Garante consistência entre o que é armazenado nas cookies/sessão e o que é usado nos templates

3. **Configuração Django**:
   - Atualizado LANGUAGES no settings.py para usar `pt_BR` em vez de `pt-br`
   - Adicionado código de debug para ajudar a diagnosticar problemas futuros

### 3. Se ainda houver problemas de tradução
Se as páginas about e resume ainda não estiverem sendo traduzidas corretamente, siga estas etapas:

1. **Atualize o contêiner Docker com gettext**:
   ```bash
   # Entre no contêiner em execução
   docker exec -it marcela_vitor_learning_center-web-project-1 bash
   
   # Instale o gettext
   apt-get update
   apt-get install -y gettext
   
   # Compile as traduções dentro do contêiner
   cd /usr/src/platform
   django-admin compilemessages
   
   # Saia do contêiner
   exit
   ```

2. **Reinicie o contêiner**:
   ```bash
   docker-compose restart web-project
   ```

3. **Verifique se as URLs de idioma estão funcionando**:
   - Navegue para /en/about/ para a versão em inglês
   - Navegue para /pt-br/about/ para a versão em português

4. **Limpe o cache do navegador**:
   - Às vezes, o navegador armazena em cache os conteúdos, impedindo que as traduções apareçam
   - Também limpe os cookies, pois o idioma pode estar salvo nos cookies

### 4. Verificação de caminho de arquivo
Certifique-se de que as estruturas de arquivos estejam corretas:
- O arquivo django.mo deve estar em `/platform/locale/pt_BR/LC_MESSAGES/`
- As tags de tradução ({% trans %} e {% blocktrans %}) devem estar em todas as strings que precisam ser traduzidas

### 5. Forçar idioma para teste
Você pode forçar um idioma específico em settings.py temporariamente para teste:
```python
LANGUAGE_CODE = 'en'  # Mude para 'pt_BR' para testar português
```

### 6. Verificar consistência nos códigos de idioma
Garanta que os códigos de idioma sejam consistentes em todo o projeto:
- Use `en` para inglês
- Use `pt-br` para português brasileiro nos formulários e configurações Django
  - O arquivo django.po deve estar no diretório `/platform/locale/pt_BR/LC_MESSAGES/`
  - No arquivo settings.py, use o formato `pt-br` (com hífen)
  - Nos formulários de alteração de idioma, use `pt-br` (com hífen)

### 7. Ajuste para correção da URL ao mudar para inglês
Foi implementada uma solução para remover o prefixo '/pt-br/' da URL quando o usuário clica na bandeira dos EUA para mudar para o inglês. A função `changeLanguage` agora verifica se:

1. O idioma selecionado é inglês ('en')
2. A URL atual começa com '/pt-br/'

Se ambas as condições forem verdadeiras, o prefixo '/pt-br/' é removido da URL antes de redirecionar, garantindo que o usuário navegue para a versão em inglês corretamente.

```javascript
// Trecho da função changeLanguage modificada:
let nextPath = window.location.pathname;
if (lang === 'en' && nextPath.startsWith('/pt-br/')) {
    nextPath = nextPath.replace('/pt-br/', '/');
}
```

Isso resolve o problema de navegação entre idiomas sem precisar ajustar as configurações de URL do Django.
