import tempfile
import unittest
from pathlib import Path

from services.dataset_builder import process_file, promote_metadata


class DatasetBuilderTests(unittest.TestCase):
    def test_promotes_year_without_visual_formatting(self):
        data = promote_metadata({}, {"ano": "1990"})

        self.assertEqual(data["ano"], 1990)

    def test_promotes_image_path_even_when_file_is_not_present(self):
        data = promote_metadata({}, {"imagem": "imagens/foto-final.jpg"})

        self.assertEqual(data["imagem"], "imagens/foto-final.jpg")

    def test_resolves_existing_image_relative_to_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            image_dir = base / "imagens"
            image_dir.mkdir()
            image_path = image_dir / "nome-livre.jpg"
            image_path.write_bytes(b"imagem-de-teste")

            md_path = base / "equipamento.md"
            md_path.write_text(
                """---
id: equipamento
layout: layout-01
ano: 1990
numero: 1
imagem: imagens/nome-livre.jpg
---

# Equipamento
""",
                encoding="utf-8",
            )

            data = process_file(md_path)

            self.assertEqual(data["imagem"], str(image_path.resolve()))
            self.assertEqual(data["ano"], 1990)


if __name__ == "__main__":
    unittest.main()
