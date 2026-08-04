# Pipeline editorial — Museu de Informática

Pipeline para converter materiais do Museu de Informática escritos em Markdown
para JSON estruturado e aplicar o conteúdo automaticamente aos templates do
Adobe InDesign.

O fluxo de produção é:

```text
Markdown → parser Python → JSON → script JSX → template InDesign
```

O projeto também inclui um watcher baseado em `watchdog`. Enquanto ele estiver
em execução, todo arquivo Markdown criado ou alterado em `content/md/` será
convertido automaticamente para o JSON correspondente em `content/json/`.

Além do pipeline técnico, o projeto documenta a habilidade **Materiais do Museu
de Informática**, responsável por padronizar a pesquisa, a redação, a produção
visual e a preparação editorial dos conteúdos do acervo.

## Habilidade Materiais do Museu de Informática

A habilidade **Materiais do Museu de Informática** organiza o processo de
produção dos materiais antes de sua entrada no pipeline automatizado. Ela reúne
as orientações necessárias para transformar fotografias, dados patrimoniais,
fontes históricas e informações técnicas em conteúdos consistentes para os
displays do Museu.

Seu escopo inclui:

- identificação e pesquisa do equipamento;
- organização e verificação das informações técnicas;
- redação segundo o contrato editorial dos layouts;
- adequação do conteúdo aos limites de cada seção;
- produção ou orientação da imagem principal;
- preparação do Markdown utilizado como fonte pelo parser;
- revisão do material antes da aplicação no InDesign.

A habilidade complementa o pipeline descrito neste repositório:

```text
pesquisa e produção editorial
             ↓
habilidade Materiais do Museu de Informática
             ↓
Markdown → parser Python → JSON → script JSX → template InDesign
```

### Formas de compartilhamento

A metodologia será distribuída por três abordagens complementares.

#### 1. Skill portátil

A habilidade será mantida como um pacote versionado, associado ao repositório.
Esse pacote deverá reunir:

- instruções operacionais;
- regras e critérios editoriais;
- limites de caracteres por seção;
- especificações para geração e seleção de imagens;
- modelos de entrada e saída;
- exemplos aprovados;
- schemas, referências e scripts auxiliares, quando aplicáveis.

A skill portátil é a **fonte oficial da metodologia editorial**. Ela permite que
o processo seja instalado, auditado, atualizado e reutilizado por outras
pessoas ou ambientes compatíveis, sem depender do histórico de uma conversa.

#### 2. GPT compartilhável

A habilidade também será disponibilizada por meio de um GPT configurado para a
produção dos materiais do Museu de Informática.

O GPT compartilhável funcionará como uma interface simplificada para usuários
que não precisam trabalhar diretamente com o repositório ou com a estrutura
interna da skill. Suas instruções e arquivos de referência deverão permanecer
alinhados à versão portátil.

O GPT facilita a execução da metodologia, mas não substitui a skill versionada
como fonte oficial.

#### 3. Projeto compartilhado

O projeto do ChatGPT poderá ser compartilhado com integrantes da equipe
responsáveis pela pesquisa, revisão, produção e acompanhamento dos materiais.

Esse ambiente preserva elementos de contexto que não pertencem necessariamente
à distribuição pública da habilidade, como:

- conversas de trabalho;
- arquivos e fotografias de referência;
- histórico de identificação dos equipamentos;
- decisões editoriais;
- revisões e exemplos em desenvolvimento.

Como pode conter materiais institucionais e informações internas, o acesso ao
projeto compartilhado deve ser concedido somente às pessoas envolvidas no
fluxo de produção.

### Responsabilidades de cada abordagem

| Abordagem | Responsabilidade principal |
| --- | --- |
| Skill portátil | Fonte oficial e versionada da metodologia editorial |
| GPT compartilhável | Interface simplificada para executar a habilidade |
| Projeto compartilhado | Ambiente colaborativo com contexto e histórico |
| Repositório | Fonte oficial do pipeline, dos arquivos e das versões publicadas |

### Atualização e consistência

Quando uma regra editorial, um modelo ou uma etapa do processo for alterado, a
atualização deve seguir esta ordem:

1. atualizar a skill portátil;
2. registrar a mudança no repositório;
3. replicar a alteração no GPT compartilhável;
4. atualizar as instruções do projeto compartilhado, quando necessário.

Conversas e exemplos do projeto compartilhado podem fornecer contexto para
novas decisões, mas não devem substituir a documentação versionada. Essa regra
evita que diferentes versões da habilidade passem a produzir resultados
incompatíveis.

## Requisitos

- Git;
- Python 3.13 ou superior (menor que 4.0);
- Poetry;
- Adobe InDesign para a etapa de diagramação;
- template do Museu com os frames, Script Labels e estilos esperados pelo JSX.

O projeto usa o `pyproject.toml` e o `poetry.lock` para administrar as
dependências. Não é necessário instalar um arquivo `requirements.txt`.

## Clonar o projeto

Substitua `<URL-DO-REPOSITORIO>` pelo endereço HTTPS ou SSH do repositório:

```bash
git clone <URL-DO-REPOSITORIO>
cd museu-carnival
```

## Instalar com Poetry

Na raiz do projeto, ative o ambiente virtual e instale as dependências:

```bash
poetry shell
poetry install
```

O projeto utiliza o Taskipy. Depois de entrar no `poetry shell`, os comandos
podem ser executados diretamente como `task ...`.

> No Poetry 2, `poetry shell` pode exigir o plugin oficial
> `poetry-plugin-shell`. Se o comando não estiver disponível, instale-o uma
> única vez com `poetry self add poetry-plugin-shell`. Como alternativa, use
> `poetry run task <comando>` sem ativar o shell.

## Estrutura de arquivos

```text
museu-informatica/
├── assets/
│   └── imagens/                 # imagens usadas nos displays
├── content/
│   ├── md/                      # Markdown: fonte editorial
│   └── json/                    # JSON: saída do parser
├── producao/
│   └── erros/                   # relatórios gerados pelo watcher
├── scripts/
│   ├── build/
│   │   ├── main.py              # conversor manual
│   │   ├── watcher.py           # conversor automático
│   │   ├── config/
│   │   ├── parsers/
│   │   ├── renders/
│   │   ├── services/
│   │   └── utils/
│   └── indesign/
│       └── populate-from-JSON.v2.js
├── templates/                   # templates do InDesign
├── pyproject.toml
├── poetry.lock
└── README.md
```

Os caminhos padrão são calculados a partir da raiz do projeto:

| Conteúdo | Pasta |
| --- | --- |
| Markdown de entrada | `content/md/` |
| JSON gerado | `content/json/` |
| Imagens | `assets/imagens/` |
| Erros do watcher | `producao/erros/` |
| Parser e watcher | `scripts/build/` |
| Script do InDesign | `scripts/indesign/` |
| Templates | `templates/` |

## Como rodar

### `task run` — fluxo normal com watcher

```bash
task run
```

Esse é o comando recomendado para a produção. Ao iniciar, ele:

1. procura Markdown ainda não convertidos ou mais recentes que seus JSONs;
2. converte os arquivos pendentes;
3. continua observando `content/md/`;
4. converte automaticamente cada `.md` criado, alterado ou movido para a
   pasta.

Exemplo:

```text
content/md/095-apple-performa-5215.md
                         ↓
content/json/095-apple-performa-5215.json
```

O processo permanece ativo no terminal. Para encerrá-lo, pressione `Ctrl+C`.
Fechar o terminal também encerra o watcher.

### `task convert` — conversão manual

```bash
task convert
```

Executa o conversor manual (`scripts/build/main.py`) e encerra. Sem argumentos,
processa os Markdown de `content/md/` e grava o lote em:

```text
content/json/dataset.json
```

Esse modo é mantido para manutenção, testes e compatibilidade com o fluxo
anterior. Para a produção cotidiana, prefira `task run` ou `task once`, que
mantêm um JSON individual por material.

### `task once` — converter pendências e encerrar

```bash
task once
```

Converte somente os Markdown que ainda não têm JSON ou que foram alterados
depois da última conversão. Cada material recebe seu próprio arquivo em
`content/json/`; em seguida, o processo encerra.

Para reconstruir todos os JSONs, mesmo os já atualizados:

```bash
python scripts/build/watcher.py --once --force
```

Se os eventos nativos do sistema de arquivos não funcionarem corretamente —
por exemplo, em algumas pastas de rede — use:

```bash
python scripts/build/watcher.py --polling
```

## Convenção de nomes

Use nomes previsíveis e um prefixo comum entre o Markdown, o JSON e a imagem
principal. A convenção recomendada é:

```text
NNN-slug-do-equipamento.ext
```

- `NNN`: número do display com três dígitos e zeros à esquerda;
- `slug-do-equipamento`: nome em minúsculas, sem espaços, acentos ou caracteres
  especiais; separe as palavras com hífens;
- extensão: use letras minúsculas (`.md`, `.json`, `.png`, `.jpg` ou `.tif`).

Exemplo completo:

```text
content/md/095-apple-performa-5215.md
content/json/095-apple-performa-5215.json
assets/imagens/095-apple-performa-5215-principal.png
```

No frontmatter, o número pode permanecer sem zeros à esquerda, enquanto o
prefixo do arquivo usa três dígitos:

```yaml
---
id: apple-performa-5215
layout: layout-02
ano: 1995
numero: 95
imagem: assets/imagens/095-apple-performa-5215-principal.png
---
```

Use sempre um caminho relativo à raiz do projeto para `imagem`. Isso permite
mover ou clonar o projeto sem reescrever caminhos locais. Mesmo no Windows,
use barras normais (`/`) no Markdown:

```yaml
# Recomendado
imagem: assets/imagens/095-apple-performa-5215-principal.png

# Evitar
imagem: C:\Museu\museu-informatica\assets\imagens\foto.png
```

Para fotografias complementares, mantenha o mesmo prefixo:

```text
095-apple-performa-5215-detalhe-01.png
095-apple-performa-5215-detalhe-02.png
095-apple-performa-5215-etiqueta-01.png
```

Atualmente, apenas a imagem indicada no campo `imagem` é aplicada
automaticamente pelo JSX.

## Formato básico do Markdown

O arquivo deve começar com o frontmatter e utilizar os nomes de seção definidos
pelo contrato editorial:

```markdown
---
id: apple-performa-5215
layout: layout-02
ano: 1995
numero: 95
imagem: assets/imagens/095-apple-performa-5215-principal.png
---

# Apple Macintosh Performa 5215

> Um Macintosh multimídia feito para ocupar a mesa de casa.

## o_que_e

Texto da seção.

## por_que_importa

Texto da seção.

## linha_do_tempo

- 1984 | Primeiro Macintosh: descrição do acontecimento
- 1995 | Performa 5215: descrição do acontecimento

## curiosidades

- Primeira curiosidade.
- Segunda curiosidade.

## curiosidade_destaque

### 1 GB

Texto da curiosidade em destaque.

## explore_mais

Texto ou perguntas para observação do objeto.
```

Não altere os identificadores das seções. Eles são usados pelo parser e pelo
script do InDesign.

## Aplicar o JSON ao template do InDesign

### 1. Disponibilizar o JSX no painel Scripts

No InDesign:

1. abra **Janela → Utilitários → Scripts**;
2. no painel, localize a pasta de scripts do usuário;
3. use a opção **Revelar no Explorer** ou **Revelar no Finder**;
4. copie `scripts/indesign/populate-from-JSON.v2.js` para a pasta
   `Scripts Panel`.

Se uma versão anterior do script já estiver instalada, substitua-a e atualize o
painel Scripts ou reinicie o InDesign.

### 2. Preparar o template

Abra o template correspondente ao valor de `layout` do Markdown. Os frames
devem possuir estes nomes ou Script Labels, conforme as seções disponíveis no
layout:

| Nome/Script Label | Tipo de quadro | Conteúdo |
| --- | --- | --- |
| `titulo` | texto | título do equipamento |
| `linha_fina` | texto | linha fina |
| `ano` | texto | ano do cabeçalho |
| `numero` | texto | número do display |
| `imagem` | gráfico | imagem principal |
| `o_que_e` | texto | título e corpo de “O que é?” |
| `por_que_importa` | texto | título e corpo de “Por que importa?” |
| `linha_do_tempo` | texto | linha do tempo |
| `curiosidades` | texto | lista de curiosidades |
| `curiosidade_destaque` | texto | curiosidade em destaque |
| `explore_mais` | texto | convite à exploração |

O label `imagem` deve ser aplicado ao quadro gráfico que receberá a imagem, não
ao arquivo de imagem colocado dentro dele. Os estilos de parágrafo usados pelo
JSX também devem existir no template.

Estilos esperados pela versão atual do script:

```text
P_Titulo
P_LinhaFina
P_Ano
P_Numero
P_OQueE_Titulo
P_OQueE_Texto
P_PorQueImporta_Titulo
P_PorQueImporta_Texto
P_LinhaDoTempo_Titulo
P_Timeline_Item
P_Curiosidades_Titulo
P_Curiosidades
P_CuriosidadeDestaque_Titulo
P_CuriosidadeDestaque_Texto
P_ExploreMais_Titulo
P_ExploreMais_Texto
```

### 3. Executar o preenchimento

1. mantenha o documento do template aberto e ativo;
2. dê duplo clique em `populate-from-JSON.v2.js` no painel Scripts;
3. na janela **Selecione o JSON**, escolha o arquivo correspondente em
   `content/json/`;
4. aguarde a mensagem de conclusão;
5. revise o preenchimento, os vínculos e a diagramação antes de salvar ou
   exportar.

O JSX usa o primeiro item do JSON, localiza os frames em cada página por nome ou
Script Label, aplica o texto e os estilos, posiciona a imagem de forma
proporcional e centralizada e formata verticalmente o ano do cabeçalho.

## Erros e verificações

### O watcher encontrou um erro

O processo continua ativo e preserva o JSON anterior. Consulte o relatório
correspondente em:

```text
producao/erros/<nome-do-material>.error.log
```

Corrija o Markdown e salve-o novamente para disparar uma nova conversão.

### A imagem não foi encontrada no InDesign

Verifique se:

- o frontmatter contém `assets/imagens/...`;
- o nome e a extensão coincidem exatamente com o arquivo;
- o JSON foi regenerado depois da alteração do Markdown;
- o caminho usa barras `/`;
- o arquivo está realmente dentro da raiz clonada do projeto.

O JSX informa os caminhos examinados quando não consegue localizar a imagem.

### O conteúdo não apareceu no template

Verifique se o frame correto possui o nome ou Script Label esperado. Ausência de
uma seção opcional ou de seu frame não impede o preenchimento das demais áreas.

### Texto excedente, fontes e vínculos

Nesta versão, a inspeção final ainda é manual. Use o painel **Preflight** do
InDesign e confira especialmente:

- texto excedente;
- fontes ausentes;
- vínculos de imagem ausentes ou modificados;
- preenchimento e estilos dos frames;
- adequação do conteúdo ao layout escolhido.

Um módulo de observabilidade e preflight específico do projeto está previsto
como evolução futura. Ele não faz parte do fluxo automatizado atual.

## Fluxo recomendado de produção

1. execute `task run` na raiz do projeto;
2. crie ou atualize o Markdown em `content/md/`;
3. confirme no terminal que o JSON foi gerado em `content/json/`;
4. abra o template correto no InDesign;
5. execute o JSX e selecione o JSON do material;
6. faça a revisão visual e o preflight do documento;
7. salve o arquivo de produção e exporte o material final.

O pipeline já pode ser usado em teste de produção. A revisão final no InDesign
continua obrigatória, sobretudo enquanto o módulo próprio de observabilidade e
preflight não estiver implementado.
