# Conversão automática de Markdown para JSON

O `watcher.py` observa `content/md` e atualiza o arquivo correspondente em
`content/json` sempre que um Markdown é criado, alterado ou movido para a pasta.
Ele reutiliza o parser existente; não há uma segunda implementação do contrato
editorial.

## Instalação

As dependências do projeto são administradas pelo Poetry. Na raiz do
repositório, instale o ambiente e ative-o:

```bash
poetry shell
poetry install
```

Não é necessário criar nem instalar um arquivo `requirements.txt`. A
dependência `watchdog` está declarada no `pyproject.toml` e é instalada pelo
Poetry.

## Uso normal

Com o ambiente Poetry ativo, inicie o fluxo contínuo pelo Taskipy:

```bash
task run
```

Esse é o comando normal de produção. Ao iniciar, ele converte os Markdown
pendentes e depois mantém o watcher observando alterações até ser encerrado.
Para encerrar, pressione `Ctrl+C`.

Também é possível executar o task sem ativar o shell:

```bash
poetry run task run
```

Pastas padrão, relativas à raiz do projeto:

```text
content/md/        entrada
content/json/      saída
producao/erros/    relatórios de falha
```

Um arquivo `content/md/095-apple-performa-5215.md` produz:

```text
content/json/095-apple-performa-5215.json
```

## Outros modos

Converter apenas os arquivos pendentes e encerrar:

```bash
task once
```

Executar a conversão manual em lote pelo ponto de entrada legado:

```bash
task convert
```

Os argumentos abaixo são opções avançadas do watcher. Com o ambiente Poetry
ativo, chame diretamente o script a partir da raiz do repositório.

Reconstruir todos os JSONs individuais e encerrar:

```bash
python scripts/build/watcher.py --once --force
```

Usar varredura periódica quando a pasta estiver em rede ou quando eventos
nativos do sistema de arquivos não funcionarem corretamente:

```bash
python scripts/build/watcher.py --polling
```

Usar pastas personalizadas:

```bash
python scripts/build/watcher.py \
  --input caminho/md \
  --output caminho/json \
  --errors caminho/erros
```

Sem `poetry shell`, prefixe essas chamadas com `poetry run`.

## Regras operacionais

- eventos repetidos são agrupados por `debounce`;
- a conversão espera tamanho e data do arquivo estabilizarem;
- arquivos temporários de editores são ignorados;
- cada JSON é publicado por substituição atômica;
- um erro não encerra o observador nem sobrescreve o JSON anterior;
- a exclusão de um Markdown não apaga automaticamente seu JSON;
- `task run` converte arquivos sem saída ou mais recentes que a saída antes de
  iniciar a observação;
- subpastas de `content/md` são espelhadas em `content/json` e em
  `producao/erros`.
