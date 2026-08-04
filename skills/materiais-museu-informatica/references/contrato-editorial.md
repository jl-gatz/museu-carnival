# Contrato editorial e de dados

## Estrutura-base

Usar o modelo abaixo, ajustando seções opcionais ao layout vigente:

```md
---
id: identificador-em-kebab-case
layout: layout-02
ano: 1995
numero: 95
---

# Nome oficial do equipamento

> Linha fina curta, memorável e tecnicamente honesta.

## o_que_e

Explique natureza, função, fabricante, período e configuração essencial.

## por_que_importa

Explique a transformação histórica representada pelo objeto.

## curiosidades

- Curiosidade verificável e significativa.
- Outro detalhe que ajude a observar o objeto.

## linha_do_tempo

- **1995** — Evento breve e documentado.

## explore_mais

Indicação curta para QR code, vídeo, demonstração ou recurso interativo.
```

## Regras do texto

- Preservar `id`, `layout`, `ano` e `numero` no YAML quando conhecidos.
- Usar nome oficial no H1; não modernizar a grafia do produto sem motivo.
- Fazer a linha fina soar convidativa, não publicitária.
- Em `o_que_e`, começar pela função antes da especificação.
- Em `por_que_importa`, explicar consequência histórica; não repetir a descrição.
- Escolher curiosidades que possam ser apontadas no objeto ou lembradas pelo visitante.
- Usar listas estruturadas para curiosidades e linha do tempo.
- Não criar seção sem conteúdo só para preencher o molde.
- Usar algarismos e unidades de modo consistente; expandir siglas na primeira ocorrência quando isso ajudar o público.

## Labels como API do layout

Tratar estes labels como estáveis quando existirem no projeto:

- `titulo`
- `linha_fina`
- `o_que_e`
- `por_que_importa`
- `curiosidades`
- `linha_do_tempo`
- `explore_mais`
- `metadados`
- `imagem`

O template decide posição e tamanho. O conteúdo não deve codificar decisões visuais.

## InDesign

- Nomear frames com os mesmos labels do contrato.
- Aplicar estilos por seção e por função, usando os prefixos do projeto: `P_` (parágrafo), `C_` (caractere) e `O_` (objeto).
- Manter título e corpo como estilos distintos dentro de cada seção.
- Representar a linha do tempo como dados estruturados para permitir múltiplos estilos e componentes duplicáveis.
- Gerar JSON em array quando houver processamento em lote.
- Tratar um item como uma página/registro, salvo quando o layout vigente determinar outra coisa.

## Critérios de passagem

Antes de entregar ao parser:

- YAML válido e sem campos duplicados;
- somente um H1 por item;
- labels escritos exatamente como o parser espera;
- listas realmente estruturadas;
- ausência de HTML ou formatação improvisada;
- arquivo e imagem associados pelo mesmo `id` ou por caminho explícito;
- texto revisado para caber, sem depender de redução extrema de fonte.
