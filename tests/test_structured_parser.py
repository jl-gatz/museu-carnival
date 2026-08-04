import unittest

from parsers.structured_parser import parse_structured


class StructuredParserTests(unittest.TestCase):
    def test_preserves_all_o_que_e_paragraphs(self):
        data = parse_structured(
            """# Equipamento

## o_que_e

Primeiro parágrafo.

Segundo parágrafo.

Terceiro parágrafo.
"""
        )

        self.assertEqual(
            data["o_que_e"]["texto"],
            "Primeiro parágrafo.\rSegundo parágrafo.\rTerceiro parágrafo.",
        )

    def test_keeps_single_paragraph_compatible(self):
        data = parse_structured(
            """# Equipamento

## o_que_e

Parágrafo único.
"""
        )

        self.assertEqual(data["o_que_e"]["texto"], "Parágrafo único.")

    def test_parses_curiosidade_destaque(self):
        data = parse_structured(
            """# Teleprint 390

## curiosidade_destaque

### 8 BITS

Cada linha da fita podia guardar oito bits por meio de pequenos furos.

Assim, textos e programas viravam sequências perfuradas.
"""
        )

        self.assertEqual(
            data["curiosidade_destaque"],
            {
                "titulo": "8 BITS",
                "texto": (
                    "Cada linha da fita podia guardar oito bits por meio "
                    "de pequenos furos.\rAssim, textos e programas viravam "
                    "sequências perfuradas."
                ),
            },
        )

    def test_curiosidade_destaque_is_optional(self):
        data = parse_structured("# Equipamento")

        self.assertEqual(
            data["curiosidade_destaque"],
            {"titulo": "", "texto": ""},
        )


if __name__ == "__main__":
    unittest.main()
