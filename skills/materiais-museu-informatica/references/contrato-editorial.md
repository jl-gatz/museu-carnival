# Contrato editorial e de dados

## Estrutura-base vigente

Usar o modelo abaixo como contrato atual de produção. Preservar a ordem, os identificadores das seções e o formato dos itens estruturados, pois eles são consumidos pelo parser e pelo script do InDesign.

```md
---
id: identificador-em-kebab-case
layout: layout-02
ano: 1995
numero: 95
imagem: assets/imagens/095-identificador-principal.png
---

# Nome oficial do equipamento

> Linha fina curta, memorável e tecnicamente honesta.

## o_que_e

Explique natureza, função, fabricante, período e configuração essencial.

## por_que_importa

Explique a transformação histórica representada pelo objeto.

## linha_do_tempo

- 1984 | Evento histórico: descrição breve e documentada
- 1995 | Equipamento: descrição breve e documentada

## curiosidades

- Curiosidade verificável e significativa.
- Outro detalhe que ajude a observar ou compreender o objeto.

## curiosidade_destaque

### 1 GB

Apresente um dado, contraste ou ideia especialmente memorável em um texto curto.

Uma segunda frase ou parágrafo pode aproximar a informação da experiência atual do visitante.

## explore_mais

Texto curto de observação, comparação, pergunta ou convite para QR code, vídeo, demonstração ou recurso interativo.
```

## Regras do frontmatter

- Preservar `id`, `layout`, `ano`, `numero` e `imagem` quando conhecidos.
- Escrever `id` em kebab-case.
- Usar em `imagem` um caminho relativo à raiz do projeto, normalmente `assets/imagens/<numero>-<id>-principal.png`.
- Usar barras normais (`/`) no caminho, inclusive em ambientes Windows.
- Não inventar `numero`, ano da unidade ou caminho de imagem quando esses dados ainda não estiverem definidos; registrar a pendência nas notas curatoriais.

## Regras do texto

- Usar o nome oficial no H1; não modernizar a grafia do produto sem motivo.
- Fazer a linha fina soar convidativa, não publicitária.
- Em `o_que_e`, começar pela função antes da especificação.
- Em `por_que_importa`, explicar consequência histórica; não repetir a descrição do objeto.
- Na linha do tempo, usar o formato exato `- ANO | Título do evento: descrição`.
- Ordenar a linha do tempo cronologicamente e evitar eventos que não ajudem a interpretar o equipamento.
- Escolher curiosidades verificáveis, observáveis ou fáceis de recordar.
- Não repetir nas curiosidades o mesmo argumento usado em `o_que_e` ou `por_que_importa`.
- Não criar seção vazia só para preencher o molde.
- Usar algarismos e unidades de modo consistente; expandir siglas na primeira ocorrência quando isso ajudar o público.
- Manter parágrafos curtos e revisar o volume de texto para o layout indicado.

## Curiosidade em destaque

A seção `curiosidade_destaque` alimenta a área visual de maior ênfase do painel. Ela possui dois componentes obrigatórios:

1. um título em H3, curto e de forte leitura visual;
2. um texto explicativo breve, que dê sentido ao título.

O título pode ser um número com unidade, uma capacidade, uma velocidade, uma quantidade ou uma expressão curta, por exemplo `### 1 GB`, `### 32 QUILOS` ou `### QUATRO CORES`.

O texto deve:

- explicar por que o dado é interessante;
- transformar a especificação em experiência compreensível;
- usar comparação contemporânea apenas quando ela for correta e esclarecedora;
- evitar repetir literalmente uma curiosidade da lista;
- evitar superlativos, equivalências ou cálculos sem sustentação documental.

O parser representa a seção aproximadamente assim:

```json
{
  "curiosidade_destaque": {
    "titulo": "1 GB",
    "texto": "O disco rígido de 1 GB parecia espaçoso em 1995. Hoje, um único vídeo gravado por um celular pode ocupar capacidade semelhante."
  }
}
```

No template do InDesign, o frame correspondente usa o nome ou Script Label `curiosidade_destaque`. O título e o texto usam, respectivamente, os estilos `P_CuriosidadeDestaque_Titulo` e `P_CuriosidadeDestaque_Texto`.

## Labels como API do layout

Tratar estes labels como estáveis quando existirem no projeto:

- `titulo`
- `linha_fina`
- `ano`
- `numero`
- `imagem`
- `o_que_e`
- `por_que_importa`
- `linha_do_tempo`
- `curiosidades`
- `curiosidade_destaque`
- `explore_mais`

O template decide posição e tamanho. O conteúdo não deve codificar decisões visuais nem renomear labels para combinar com a prosa.

## InDesign

- Nomear frames com os mesmos labels do contrato.
- Aplicar estilos por seção e por função, usando os prefixos do projeto: `P_` (parágrafo), `C_` (caractere) e `O_` (objeto).
- Manter título e corpo como estilos distintos dentro de cada seção.
- Representar a linha do tempo como dados estruturados para permitir múltiplos estilos e componentes duplicáveis.
- Gerar JSON em array quando houver processamento em lote.
- Tratar um item como uma página/registro, salvo quando o layout vigente determinar outra coisa.
- A ausência de uma seção opcional ou de seu frame não deve interromper o preenchimento das demais áreas.

## Critérios de passagem

Antes de entregar ao parser:

- YAML válido e sem campos duplicados;
- somente um H1 por item;
- labels escritos exatamente como o parser espera;
- linha do tempo no formato `ANO | Título: descrição`;
- curiosidades realmente estruturadas como lista;
- `curiosidade_destaque` com H3 e texto explicativo;
- ausência de HTML ou formatação improvisada;
- arquivo e imagem associados por caminho relativo explícito;
- texto revisado para caber, sem depender de redução extrema de fonte;
- nenhuma afirmação apresentada como pertencente à unidade quando foi confirmada apenas para o modelo ou para a família.
