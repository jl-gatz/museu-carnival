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
	        texto + (addBreak ? "\r" : "");
	
	    // ponto final
	    var end = frame.insertionPoints[-1].index;
	
	    // pega o texto inserido
	    var insertedText =
	        frame.parentStory.characters.itemByRange(
	            start,
	            end - 1
	        );
	
	    // aplica estilo
	    insertedText.paragraphs[0]
	        .appliedParagraphStyle = style;
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
		
		// NUMERO
		var numeroFrame = getFrameFromPage(page, "numero");
		
		if (item.numero && numeroFrame) {
            applyParagraph(numeroFrame, item.numero, "P_Numero", false, false);

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