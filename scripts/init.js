#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// 📁 Nome do projeto (pode virar argumento depois)
const ROOT = "project";

// 🌳 Estrutura declarativa
const structure = {
  content: {
    md: {},
    json: {},
    schema: {},
    drafts: {}
  },
  templates: {
    base: {
      "museu_base.indd": null
    },
    variants: {
      "timeline.indd": null,
      "destaque.indd": null,
      "compacto.indd": null
    },
    snippets: {}
  },
  assets: {
    imagens: {
      originais: {},
      processadas: {}
    },
    icones: {},
    logos: {}
  },
  scripts: {
    build: {
      "md-to-json.js": null
    },
    indesign: {
      "populate-document.jsx": null
    },
    utils: {
      "validators.js": null
    }
  },
  builds: {
    "2026-04-30": {
      "museu_v1.indd": null,
      "museu_v1.pdf": null
    },
    latest: {}
  },
  config: {
    "styles-map.json": JSON.stringify({
      titulo: "P_Titulo_Principal",
      linha_fina: "P_LinhaFina",
      "o_que_e.titulo": "P_OQueE_Titulo",
      "o_que_e.texto": "P_OQueE_Texto"
    }, null, 2),
    "project.json": JSON.stringify({
      name: "Museu de Informática",
      version: "1.0.0"
    }, null, 2)
  },
  logs: {
    "build.log": ""
  },
  "README.md": `# Museu de Informática

Pipeline editorial:

.md → JSON → InDesign → PDF

## Scripts

- node scripts/build/md-to-json.js
- InDesign: populate-document.jsx
`
};

// 🛠️ Criador recursivo
function createTree(basePath, tree) {
  Object.entries(tree).forEach(([name, value]) => {
    const fullPath = path.join(basePath, name);

    if (value === null || typeof value === "string") {
      // 📄 arquivo
      if (!fs.existsSync(fullPath)) {
        fs.writeFileSync(fullPath, value || "");
        console.log("📄", fullPath);
      }
    } else {
      // 📁 diretório
      if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
        console.log("📁", fullPath);
      }
      createTree(fullPath, value);
    }
  });
}

// 🚀 execução
function main() {
  const rootPath = path.resolve(process.cwd(), ROOT);

  if (!fs.existsSync(rootPath)) {
    fs.mkdirSync(rootPath);
    console.log("📁", rootPath);
  }

  createTree(rootPath, structure);

  console.log("\n✅ Estrutura criada com sucesso!");
}

main();