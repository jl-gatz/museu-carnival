# Curiosidade em destaque

A área vermelha de destaque usa uma seção opcional própria no Markdown:

```md
## curiosidade_destaque

### 8 BITS

Cada linha da fita podia guardar oito bits por meio de pequenos furos.
Assim, textos e programas eram transformados em sequências perfuradas no papel.
```

O parser gera:

```json
{
  "curiosidade_destaque": {
    "titulo": "8 BITS",
    "texto": "Cada linha da fita podia guardar oito bits por meio de pequenos furos. Assim, textos e programas eram transformados em sequências perfuradas no papel."
  }
}
```

No template do InDesign:

- o frame deve receber o Script Label `curiosidade_destaque`;
- o título usa o estilo `P_CuriosidadeDestaque_Titulo`;
- o texto usa o estilo `P_CuriosidadeDestaque_Texto`.

Se a seção ou o frame não existirem, o restante do documento continua sendo
preenchido normalmente.
