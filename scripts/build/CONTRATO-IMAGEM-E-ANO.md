# Contrato de aplicação da imagem e do ano

## Imagem principal

No Markdown, `imagem` informa o caminho real do arquivo. O nome não precisa ser
igual ao `id`, ao Markdown nem ao futuro arquivo do InDesign.

```yaml
imagem: imagens/foto-final.jpg
```

O parser promove o campo para `imagem` na raiz do JSON. Se o arquivo existir em
relação ao Markdown, o caminho é convertido em absoluto. Se ainda não existir
no ambiente do parser, o valor original é preservado para uma resolução
posterior.

No template do InDesign, o quadro gráfico deve receber o nome ou Script Label:

```text
imagem
```

O JSX substitui o conteúdo do quadro, usa preenchimento proporcional e
centraliza a imagem. Quando o caminho do JSON é relativo, procura primeiro ao
lado do JSON e depois nos diretórios-pai.

## Ano

O ano continua sem formatação visual no Markdown e no JSON:

```yaml
ano: 1990
```

```json
"ano": 1990
```

Somente o JSX, ao preencher o frame `ano`, converte quatro algarismos para:

```text
1\r9\r9\r0\r
```

Assim, a organização vertical pertence ao template, não ao dado. Anos da
seção `linha_do_tempo` não passam por essa transformação.
