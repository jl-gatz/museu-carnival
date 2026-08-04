---
name: produzir-material-museu-informatica
description: Produzir materiais de exposição para itens do acervo do Museu de Informática da Unicamp, do levantamento de fotos e pesquisa histórica/técnica à redação museológica em Markdown, direção ou geração da imagem panorâmica e preparação do conteúdo para o pipeline MD→JSON→InDesign. Usar para criar, revisar, completar ou padronizar fichas de equipamentos, terminais, computadores, periféricos e infraestrutura segundo o método editorial do usuário.
---

# Produzir materiais do Museu de Informática

## Princípio

Tratar cada item como uma pequena investigação curatorial. Preservar a distinção entre:

- o que as fotos e etiquetas da unidade do acervo comprovam;
- o que fontes confiáveis documentam sobre o modelo ou a família;
- o que é inferência, hipótese ou identificação ainda incerta.

Não inventar especificações para preencher lacunas. Fazer uma pergunta somente quando a ausência impedir uma decisão material; caso contrário, avançar, explicitar a incerteza e indicar como verificá-la.

## Executar o fluxo

1. **Examinar o material recebido**
   - Inspecionar todas as fotos, placas, etiquetas, textos anteriores e observações do usuário.
   - Transcrever números de modelo, datas, fabricantes, interfaces e inscrições visíveis.
   - Separar identidade da unidade, identidade do modelo e contexto de uso.
   - Se a identificação estiver incerta, propor candidatos e dizer qual evidência resolveria a dúvida.

2. **Definir as perguntas de pesquisa**
   - Confirmar fabricante, nome oficial, variante, período, função e ambiente de uso.
   - Investigar arquitetura, mídias, interfaces, software, compatibilidade, mercado e relevância histórica apenas quando ajudarem o visitante a compreender o objeto.
   - Procurar vínculos documentáveis com Brasil, Unicamp, CCUEC/Detic ou o acervo quando pertinentes.
   - Para detalhes da estratégia e hierarquia de fontes, ler [pesquisa-e-validacao.md](references/pesquisa-e-validacao.md).

3. **Pesquisar e conferir**
   - Usar pesquisa web para fatos históricos/técnicos; priorizar manuais, catálogos, documentação do fabricante, museus técnicos e fontes acadêmicas.
   - Cruzar alegações centrais em mais de uma fonte quando possível.
   - Registrar divergências de datas, nomes ou capacidades e adotar a formulação mais cautelosa.
   - Não apresentar como fato aquilo que só pode ser inferido das fotos.

4. **Construir o argumento museológico**
   - Responder primeiro: “o que é?”, “para que servia?” e “por que importa?”.
   - Traduzir a técnica por função e experiência concreta antes de usar números.
   - Escolher poucos detalhes memoráveis; evitar transformar o painel em ficha de especificações.
   - Relacionar o equipamento à mudança histórica que ele representa.

5. **Redigir no contrato Markdown**
   - Ler [contrato-editorial.md](references/contrato-editorial.md).
   - Entregar Markdown puro, com YAML e labels estáveis; não alterar labels para combinar com a prosa.
   - Manter parágrafos curtos, linguagem clara, precisão técnica e tom institucional com leve vivacidade.
   - Preservar o modelo solicitado pelo usuário quando ele fornecer um exemplo mais recente.

6. **Planejar ou gerar a imagem**
   - Ler [direcao-visual.md](references/direcao-visual.md).
   - Usar as fotografias do acervo como referência do objeto, não como cenário a ser copiado.
   - Manter o equipamento reconhecível, historicamente plausível e protagonista.
   - Quando solicitado, gerar a imagem diretamente e revisar proporções, conexões, teclado, tela, portas, logotipos e acessórios.
   - Preparar por padrão uma composição horizontal para **190 mm × 83 mm** (razão aproximada **2,289:1**).

7. **Preparar para MD→JSON→InDesign**
   - Considerar o Markdown a interface humana e o JSON a interface da máquina.
   - Manter frontmatter e seções estruturadas; listas e linha do tempo não devem virar texto solto.
   - Manter labels dos frames independentes do layout. Templates podem mudar ordem e dimensões sem mudar o contrato.
   - Usar a imagem final em frame nomeado, destinada a posicionamento por script com `.place()`.
   - Preservar a separação: Python orquestra dataset/arquivos; JSX renderiza no InDesign, aplica estilos, salva e fecha.

8. **Fazer a revisão final**
   - Conferir identidade do modelo e data da unidade.
   - Conferir cada número, sigla e superlativo.
   - Remover repetições entre `o_que_e` e `por_que_importa`.
   - Verificar que linha fina, texto e curiosidades cabem no layout.
   - Validar YAML, labels, listas e caminhos de imagem antes da conversão.
   - Confirmar que a imagem não acrescenta peças inexistentes nem confunde a unidade do acervo com uma variante.

## Entregas

Adaptar a entrega ao pedido:

- **Pesquisa:** síntese factual, pontos incertos e fontes.
- **Texto:** bloco Markdown pronto para o parser.
- **Imagem:** prompt final ou imagem gerada na proporção correta.
- **Pacote completo:** pesquisa resumida, Markdown, direção/arquivo visual e checklist de produção.
- **Revisão:** apontar problemas primeiro e devolver uma versão corrigida.

Ao concluir um pacote completo, informar de forma compacta: identificação adotada, incertezas remanescentes, arquivos produzidos e qualquer validação manual ainda necessária no InDesign.
