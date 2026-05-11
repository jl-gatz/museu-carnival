#include "json2.js"
#target "InDesign"

(function () {

    var file = File.openDialog("Selecione o JSON");
    if (!file) return;

    file.open("r");
    var json = JSON.parse(file.read());
    file.close();

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
            if (frames[i].name === name) {
                return frames[i];
            }
        }

        // alert("❌ Frame não encontrado na página: " + name);
        return null;
    }

    // 🔧 aplicar parágrafo (com validação de estilo)
    function applyParagraph(frame, texto, style, append) {
		// SE o frame não for encontrado, não executa
		if (!frame) return;

    	if (texto === undefined || texto === null || texto === "") {
        	return; // 🔒 NÃO FAZ NADA
    	}
		
        if (!append) {
            frame.contents = "";
        }

        var ip = frame.insertionPoints[-1];
        ip.contents = texto + "\r";

        var p = frame.paragraphs[-1];
        p.appliedParagraphStyle = style;
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
		
		if (item.ano && anoFrame) {
            applyParagraph(anoFrame, item.ano, "P_Ano");

		}
		
		// O QUE É
		var oQueEFrame = getFrameFromPage(page, "o_que_e")
			
		if (item.o_que_e && oQueEFrame) {
			applyParagraph(oQueEFrame, item.o_que_e.titulo, "P_OQueE_Titulo", false);
	        applyParagraph(oQueEFrame, item.o_que_e.texto, "P_OQueE_Texto", true);
	    }
		
		// POR QUE IMPORTA?
		var porQueImportaFrame = getFrameFromPage(page, "por_que_importa")
		
		if (item.por_que_importa && porQueImportaFrame) {
			applyParagraph(porQueImportaFrame, item.por_que_importa.titulo,  "P_PorQueImporta_Titulo", false);
			applyParagraph(porQueImportaFrame, item.por_que_importa.texto,  "P_PorQueImporta_Texto", true);

	    }
		
		// LINHA DO TEMPO
		var timelineFrame = getFrameFromPage(page, "linha_do_tempo");

		if (item.linha_do_tempo && timelineFrame) {
			// Limpa o texto atual
			timelineFrame.contents = "";
		    var doc = app.activeDocument;
		
		    var timeline = item.linha_do_tempo;
		    var itens = timeline.itens;
		
		    // estilos
		    var pStyle = doc.paragraphStyles.itemByName("P_Timeline_Item");
			
			if (!pStyle.isValid) {
    			alert("❌ Estilo P_Timeline_Item não encontrado!");
    			exit();
			}
		
		    var cTituloLinha = doc.characterStyles.itemByName("C_Timeline_Titulo");
		    var cAno = doc.characterStyles.itemByName("C_Timeline_Ano");
		    var cTitulo = doc.characterStyles.itemByName("C_Timeline_Subtitulo");
		    var cTexto = doc.characterStyles.itemByName("C_Timeline_Texto");
		
		    // ----------------------------
		    // TÍTULO DA SEÇÃO
		    // ----------------------------
		    var pTituloStyle = doc.paragraphStyles.itemByName("P_LinhaDoTempo_Titulo");

			if (!pTituloStyle.isValid) {
    			alert("❌ P_LinhaDoTempo_Titulo não encontrado");
    			exit();
			}

			// insere
			timelineFrame.insertionPoints[-1].contents = timeline.titulo + "\r";
			
			var pTitulo = timelineFrame.paragraphs[-1];
			
			// aplica estilo de parágrafo (com linha)
			pTitulo.appliedParagraphStyle = pTituloStyle;
			
			// limpa character style (opcional, mas seguro)
			pTitulo.characters.everyItem().appliedCharacterStyle = doc.characterStyles.item(0);
		
		    // ----------------------------
		    // ITENS
		    // ----------------------------
		    if (itens && itens.length > 0) {
		
		        for (var i = 0; i < itens.length; i++) {
		
		            var entry = itens[i];
		
		            var ano = entry.ano || "";
		            var subtitulo = entry.subtitulo || "";
		            var texto = entry.texto || "";
		
		            // conteúdo do parágrafo (1 bloco por item)
		            var conteudo =
		                ano + " " +
		                subtitulo + "\r" +
		                texto;
		
		            timelineFrame.insertionPoints[-1].contents = conteudo + "\r";
					var paragraph = timelineFrame.paragraphs[-1];
		            paragraph.appliedParagraphStyle = pStyle;
					
					// 💥 limpa herança de estilo
					paragraph.characters.everyItem().appliedCharacterStyle = doc.characterStyles.item(0);
		
		            // ----------------------------
					// ANO
					// ----------------------------
					if (ano && ano.length > 0) {
					    var start = paragraph.contents.indexOf(ano);
					    if (start !== -1) {
					        var end = start + ano.length - 1;
					        paragraph.characters.itemByRange(start, end).appliedCharacterStyle = cAno;
					    }
					}
					
					// ----------------------------
					// SUBTÍTULO
					// ----------------------------
					if (subtitulo && subtitulo.length > 0) {
					    var start = paragraph.contents.indexOf(subtitulo);
					    if (start !== -1) {
					        var end = start + subtitulo.length - 1;
					        paragraph.characters.itemByRange(start, end).appliedCharacterStyle = cTitulo;
					    }
					}
					
					// ----------------------------
					// TEXTO
					// ----------------------------
					if (texto && texto.length > 0) {
					    var start = paragraph.contents.indexOf(texto);
					    if (start !== -1) {
					        var end = start + texto.length - 1;
					        paragraph.characters.itemByRange(start, end).appliedCharacterStyle = cTexto;
					    }
					}
		        }
		    }
		}

		
		
		// CURIOSIDADES
		var curiosidadesFrame = getFrameFromPage(page, "curiosidades")
		
		if (item.curiosidades && curiosidadesFrame) {
			applyParagraph(curiosidadesFrame, item.curiosidades.titulo, "P_Curiosidades_Titulo", false);
			applyParagraph(curiosidadesFrame, item.curiosidades.itens, "P_Curiosidades", true);
	    }
		
		// EXPLORE MAIS
		var exploreMaisFrame = getFrameFromPage(page, "explore_mais")
		
		if (item.explore_mais && exploreMaisFrame) {
			applyParagraph(exploreMaisFrame, item.explore_mais.titulo, "P_ExploreMais_Titulo", false);
			applyParagraph(exploreMaisFrame, item.explore_mais.texto, "P_ExploreMais_Texto", true);

	    }
		
	}

    alert("✅ Página(s) populada(s)!");

})();