#include "json2.js"
#target "InDesign"

// Museu de Informática — versão 2.2
// Corrige a aplicação de estilos em seções com múltiplos parágrafos.

(function () {

    var jsonFile = File.openDialog("Selecione o JSON");
    if (!jsonFile) return;

    jsonFile.open("r");
    var json = JSON.parse(jsonFile.read());
    jsonFile.close();

    var doc = app.activeDocument;
    var pages = doc.pages;

    // 🔍 DEBUG: listar frames (mantido)
    // var frames = doc.textFrames;
    // var list = "";
    // for (var i = 0; i < frames.length; i++) {
    //    list += "[" + i + "] " + frames[i].name + "\n";
    // }
    // alert("Frames disponíveis:\n" + list);

	
    // 🔧 getFrame agora POR PÁGINA
    function getFrameFromPage(page, name) {
        var frames = page.textFrames;

        for (var i = 0; i < frames.length; i++) {
            if (
                frames[i].name === name ||
                frames[i].label === name
            ) {
                return frames[i];
            }
        }

        // alert("❌ Frame não encontrado na página: " + name);
        return null;
    }

    // Localiza qualquer item da página. Imagens normalmente ficam em
    // retângulos, não em textFrames.
    function getPageItemFromPage(page, name) {
        var items = page.allPageItems;

        for (var i = 0; i < items.length; i++) {
            if (
                items[i].name === name ||
                items[i].label === name
            ) {
                return items[i];
            }
        }

        return null;
    }

    function hasValue(value) {
        return !(
            value === undefined ||
            value === null ||
            value === ""
        );
    }

    // Metadados de produção pertencem ao bloco meta. A leitura na raiz é
    // mantida apenas para compatibilidade com JSONs gerados anteriormente.
    function getMetadataValue(data, name) {
        if (data.meta && hasValue(data.meta[name])) {
            return data.meta[name];
        }

        if (hasValue(data[name])) {
            return data[name];
        }

        return null;
    }

    // O JSON mantém o ano como dado puro. A quebra entre algarismos é
    // exclusivamente uma decisão de apresentação do template.
    function formatHeaderYear(value) {
        var year = String(value).replace(/[\r\n]/g, "");

        if (/^\d{4}$/.test(year)) {
            return year.split("").join("\r");
        }

        return year;
    }

    function getImageSource(data) {
        var image = getMetadataValue(data, "imagem");

        if (image && typeof image === "object") {
            image = image.caminho || image.path || image.origem;
        }

        return image;
    }

    function resolveImageFile(source, sourceJsonFile, attempts) {
        if (!hasValue(source)) return null;

        var normalizedSource = String(source).replace(/\\/g, "/");

        var directFile = File(normalizedSource);
        attempts.push(directFile.fsName);
        if (directFile.exists) return directFile;

        // Para caminhos relativos, tenta a pasta do JSON e até quatro
        // diretórios-pai. Isso cobre, por exemplo, content/json + imagens/.
        var baseFolder = sourceJsonFile.parent;

        for (var level = 0; level < 5; level++) {
            var candidate = File(
                baseFolder.fsName + "/" + normalizedSource
            );

            attempts.push(candidate.fsName);

            if (candidate.exists) return candidate;

            if (!baseFolder.parent) break;
            baseFolder = baseFolder.parent;
        }

        return null;
    }

    function placeImage(frame, imageFile) {
        if (!frame || !imageFile) return false;

        try {
            while (frame.allGraphics.length > 0) {
                frame.allGraphics[0].remove();
            }

            frame.place(imageFile);
            frame.fit(FitOptions.FILL_PROPORTIONALLY);
            frame.fit(FitOptions.CENTER_CONTENT);
            return true;
        } catch (error) {
            alert(
                "❌ Não foi possível aplicar a imagem no frame 'imagem':\n" +
                error
            );
            return false;
        }
    }

    function getParagraphStyle(styleName) {
        var style = doc.paragraphStyles.itemByName(styleName);

        if (!style.isValid) {
            alert("❌ Estilo não encontrado: " + styleName);
            return null;
        }

        return style;
    }

    function normalizeParagraphBreaks(value) {
        return String(value)
            .replace(/\r\n/g, "\r")
            .replace(/\n/g, "\r");
    }

    function applyStyleToParagraph(paragraph, style) {
        paragraph.appliedParagraphStyle = style;
        paragraph.clearOverrides(OverrideType.ALL);
    }

    // Insere uma seção completa e aplica os estilos diretamente pelos
    // índices dos parágrafos no frame. Isso evita que os parágrafos seguintes
    // herdem o estilo do título quando o corpo contém quebras de parágrafo.
    function setStructuredSection(
        frame,
        title,
        body,
        titleStyleName,
        bodyStyleName
    ) {
        if (!frame) return;

        var hasTitle = hasValue(title);
        var hasBody = hasValue(body);

        if (!hasTitle && !hasBody) return;

        var titleStyle = hasTitle
            ? getParagraphStyle(titleStyleName)
            : null;
        var bodyStyle = hasBody
            ? getParagraphStyle(bodyStyleName)
            : null;

        if ((hasTitle && !titleStyle) || (hasBody && !bodyStyle)) {
            return;
        }

        var content = "";

        if (hasTitle) {
            content = normalizeParagraphBreaks(title);
        }

        if (hasBody) {
            if (content !== "") content += "\r";
            content += normalizeParagraphBreaks(body);
        }

        frame.contents = content;

        var bodyStart = 0;

        if (hasTitle) {
            applyStyleToParagraph(frame.paragraphs[0], titleStyle);
            bodyStart = 1;
        }

        if (hasBody) {
            for (
                var paragraphIndex = bodyStart;
                paragraphIndex < frame.paragraphs.length;
                paragraphIndex++
            ) {
                applyStyleToParagraph(
                    frame.paragraphs[paragraphIndex],
                    bodyStyle
                );
            }
        }

        frame.parentStory.recompose();
    }

    // 🔧 aplicar parágrafo (com validação de estilo)
    function applyParagraph(
	    frame,
	    texto,
	    style,
	    append,
	    addBreak
	) {
	
	    if (!frame) return;
	
	    if (
	        texto === undefined ||
	        texto === null ||
	        texto === ""
	    ) {
	        return;
	    }
	
	    if (append !== true) {
	        frame.contents = "";
	    }
	
	    if (addBreak === undefined) {
	        addBreak = true;
	    }
	
	    // ponto inicial
	    var start = frame.insertionPoints[-1].index;
	
	    // insere conteúdo
	    frame.insertionPoints[-1].contents =
	        normalizeParagraphBreaks(texto) +
	        (addBreak ? "\r" : "");
	
	    // ponto final
	    var end = frame.insertionPoints[-1].index;
	
	    // pega o texto inserido
	    var insertedText =
	        frame.parentStory.characters.itemByRange(
	            start,
	            end - 1
	        );
	
	    var paragraphStyle = getParagraphStyle(style);

	    if (!paragraphStyle) return;

	    // aplica o estilo a todos os parágrafos inseridos
	    for (
	        var paragraphIndex = 0;
	        paragraphIndex < insertedText.paragraphs.length;
	        paragraphIndex++
	    ) {
	        applyStyleToParagraph(
	            insertedText.paragraphs[paragraphIndex],
	            paragraphStyle
	        );
	    }
	}
	
	// 🔧 aplicar parágrafo
    function setText(frame, text, styleName) {

        if (!frame || !text) return;

        var style = doc.paragraphStyles.itemByName(styleName);

        if (!style.isValid) {
            alert("❌ Estilo não encontrado: " + styleName);
            return;
        }

        frame.contents = text;
        frame.paragraphs[0].appliedParagraphStyle = style;
    }

	// 🚀 LOOP POR PÁGINAS
	// Aqui está tudo HARDCODED, chumbado no código mesmo
	var item = json[0];
	var imageSource = getImageSource(item);
	var imageSearchAttempts = [];
	var imageFile = resolveImageFile(
		imageSource,
		jsonFile,
		imageSearchAttempts
	);
	var imagePlaced = false;
	var imageFrameFound = false;

	if (hasValue(imageSource) && !imageFile) {
		alert(
			"❌ Imagem não encontrada:\n" + imageSource +
			"\n\nJSON selecionado:\n" + jsonFile.fsName +
			"\n\nCaminhos verificados:\n- " +
			imageSearchAttempts.join("\n- ")
		);
	}

	for (var p = 0; p < pages.length; p++) {
	
	    var page = pages[p];
	
	    // TÍTULO
	    var tituloFrame = getFrameFromPage(page, "titulo");
	
	    if (item.titulo && tituloFrame) {
	        applyParagraph(tituloFrame, item.titulo, "P_Titulo");
	    }
	
	    // LINHA FINA
	    var linhaFinaFrame = getFrameFromPage(page, "linha_fina");
	
	    if (item.linha_fina && linhaFinaFrame) {
	        applyParagraph(linhaFinaFrame, item.linha_fina, "P_LinhaFina");
	    }
		
		// ANO (se mudar para texto no caminho precisamos mudar toda a lógica aqui)
		var anoFrame = getFrameFromPage(page, "ano");
		
		var anoValue = getMetadataValue(item, "ano");

		if (hasValue(anoValue) && anoFrame) {
            applyParagraph(
                anoFrame,
                formatHeaderYear(anoValue),
                "P_Ano"
            );

		}
		
		// NUMERO
		var numeroFrame = getFrameFromPage(page, "numero");
		
		var numeroValue = getMetadataValue(item, "numero");

		if (hasValue(numeroValue) && numeroFrame) {
            applyParagraph(numeroFrame, numeroValue, "P_Numero", false, false);

		}

		// IMAGEM PRINCIPAL
		var imagemFrame = getPageItemFromPage(page, "imagem");
		if (imagemFrame) imageFrameFound = true;

		if (imageFile && imagemFrame) {
			imagePlaced = placeImage(imagemFrame, imageFile) || imagePlaced;
		}
		
		// O QUE É
		var oQueEFrame = getFrameFromPage(page, "o_que_e")
			
		if (item.o_que_e && oQueEFrame) {
			setStructuredSection(
				oQueEFrame,
				item.o_que_e.titulo,
				item.o_que_e.texto,
				"P_OQueE_Titulo",
				"P_OQueE_Texto"
			);
	    }
		
		// POR QUE IMPORTA?
		var porQueImportaFrame = getFrameFromPage(page, "por_que_importa")
		
		if (item.por_que_importa && porQueImportaFrame) {
			setStructuredSection(
				porQueImportaFrame,
				item.por_que_importa.titulo,
				item.por_que_importa.texto,
				"P_PorQueImporta_Titulo",
				"P_PorQueImporta_Texto"
			);

	    }
		
		// ----------------------------
		// LINHA DO TEMPO
		// ----------------------------
		var timelineFrame = getFrameFromPage(
		    page,
		    "linha_do_tempo"
		);

		if (item.linha_do_tempo && timelineFrame) {
		
		    var doc = app.activeDocument;
		
		    var timeline = item.linha_do_tempo;
		
		    // ----------------------------
		    // ESTILOS
		    // ----------------------------
		    var pTituloStyle =
		        doc.paragraphStyles.itemByName(
		            "P_LinhaDoTempo_Titulo"
		        );
		
		    var pTimelineStyle =
		        doc.paragraphStyles.itemByName(
		            "P_Timeline_Item"
		        );
		
		    if (!pTituloStyle.isValid) {
		        alert("❌ P_LinhaDoTempo_Titulo não encontrado");
		        exit();
		    }
		
		    if (!pTimelineStyle.isValid) {
		        alert("❌ P_Timeline_Item não encontrado");
		        exit();
		    }
		
		    // ----------------------------
		    // LIMPA FRAME
		    // ----------------------------
		
		    timelineFrame.contents = "";
		
		    // ----------------------------
		    // CONTEÚDO COMPLETO
		    // ----------------------------
		
		    var fullContent =
		        timeline.titulo +
		        "\r" +
		        timeline.markup;
		
		    timelineFrame.contents = fullContent;
		
		    // ----------------------------
			// PRIMEIRO PARÁGRAFO = TÍTULO
			// ----------------------------
			var firstParagraph =
			    timelineFrame.texts[0].paragraphs[0];
			
			firstParagraph.appliedParagraphStyle =
			    pTituloStyle;
			
			firstParagraph.clearOverrides(
			    OverrideType.ALL
			);
		
		    // ----------------------------
		    // RESTANTE = TIMELINE
		    // ----------------------------
		    for (
		        var tfp = 1;
		        tfp < timelineFrame.paragraphs.length;
		        tfp++
		    ) {

		        var paragraph =
		        timelineFrame.paragraphs[tfp];

			    // ignora parágrafos vazios
			    if (
			        paragraph.contents.replace(/\r/g, "") === ""
			    ) {
			        continue;
			    }
			
			    // aplica estilo
			    paragraph.appliedParagraphStyle =
			        pTimelineStyle;
			
			    // 🔥 equivalente ao ALT+clique
			    paragraph.clearOverrides(
			        OverrideType.ALL
			    );
			}

			// 🔥 força recomposição GREP
			timelineFrame.parentStory.recompose();
		}
		
		// CURIOSIDADES
		var curiosidadesFrame = getFrameFromPage(page, "curiosidades")
		
		if (item.curiosidades && curiosidadesFrame) {
			setStructuredSection(
				curiosidadesFrame,
				item.curiosidades.titulo,
				item.curiosidades.itens.join("\r"),
				"P_Curiosidades_Titulo",
				"P_Curiosidades"
			);
	    }

		// CURIOSIDADE EM DESTAQUE
		var curiosidadeDestaqueFrame = getFrameFromPage(
			page,
			"curiosidade_destaque"
		);

		if (
			item.curiosidade_destaque &&
			curiosidadeDestaqueFrame
		) {
			setStructuredSection(
				curiosidadeDestaqueFrame,
				item.curiosidade_destaque.titulo,
				item.curiosidade_destaque.texto,
				"P_CuriosidadeDestaque_Titulo",
				"P_CuriosidadeDestaque_Texto"
			);
	    }
		
		// EXPLORE MAIS
		var exploreMaisFrame = getFrameFromPage(page, "explore_mais")
		
		if (item.explore_mais && exploreMaisFrame) {
			setStructuredSection(
				exploreMaisFrame,
				item.explore_mais.titulo,
				item.explore_mais.texto,
				"P_ExploreMais_Titulo",
				"P_ExploreMais_Texto"
			);

	    }
		
	}

	if (imageFile && !imageFrameFound) {
		alert(
			"❌ A imagem foi localizada, mas não existe na página um " +
			"quadro com nome ou Script Label 'imagem'."
		);
	}

	var completionMessage = "✅ Página(s) populada(s)!";
	if (imagePlaced) {
		completionMessage += "\n✅ Imagem aplicada: " + imageFile.fsName;
	}
	alert(completionMessage);

})();
