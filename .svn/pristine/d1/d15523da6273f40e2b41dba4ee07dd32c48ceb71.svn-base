var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.html = {};

	var modal = '' +
		'<div id="g2e-container">' +
			'<div id="g2e-modal">' +
				'<div id="g2e-title">' +
					'<a href="http://amp.pharm.mssm.edu/Enrichr/" target="_blank">' +
						'<img src="http://amp.pharm.mssm.edu/Enrichr/images/enrichr-icon.png">' +
						'<span>GEO2</span><span class="g2e-highlight">Enrichr</span>' +
					'</a>' +
					'<button id="g2e-close-btn" class="g2e-btn">&#10006</button>' +
				'</div>' +
				'<div id="g2e-forms" class="column left">' +
					'<div class="g2e-form">' +
						'<h4>Method to identify differential expression</h4>' +
						'<div class="g2e-block">' +
							'<input id="g2e-chdir" type="radio" name="method" value="chdir" checked="checked">' +
							'<label for="g2e-chdir" class="g2e-lbl">Characteristic direction</label>' +
						'</div>' +
						'<div class="g2e-block">' +
							'<input id="g2e-ttest" type="radio" name="method" value="ttest">' +
							'<label for="g2e-ttest" class="g2e-lbl">T-test</label>' +
						'</div>' +
						'<div class="g2e-block">' +
							'<input id="g2e-limma" type="radio" name="method" value="limma">' +
							'<label for="g2e-limma" class="g2e-lbl">Limma</label>' +
						'</div>' +
						'<div class="g2e-block">' +
							'<input id="g2e-sam" type="radio" name="method" value="sam">' +
							'<label for="g2e-sam" class="g2e-lbl">SAM</label>' +
						'</div>' +
					'</div>' +
					'<div class="g2e-form g2e-last">' +
						'<h4>Gene list inclusion</h4>' +
						'<div class="g2e-block">' +
							'<input id="g2e-combined" type="radio" name="inclusion" value="combined" checked="checked">' +
							'<label for="g2e-combined" class="g2e-lbl">Combined</label>' +
						'</div>' +
						'<div class="g2e-block">' +
							'<input id="g2e-up" type="radio" name="inclusion" value="up">' +
							'<label for="g2e-up" class="g2e-lbl">Up genes</label>' +
						'</div>' +
						'<div class="g2e-block">' +
							'<input id="g2e-down" type="radio" name="inclusion" value="down">' +
							'<label for="g2e-down" class="g2e-lbl">Down genes</label>' +
						'</div>' +
					'</div>' +
				'</div>' +
				'<div id="g2e-confirm" class="column right">' +
					'<span class="g2e-lowlight">GEO2Enrichr must screen scrape to collect some of the data.<br>Please confirm it is correct.</span>' +
					// These values will be dynamically filled at load time.
					'<table id="g2e-confirm-tbl">' +
						'<tr>' +
							'<td class="g2e-subtitle">Accession #:</td>' +
							'<td id="g2e-confirm-tbl-acc"></td>' +
							'<td class="g2e-edit">Edit</td>' +
						'</tr>' +
						'<tr>' +
							'<td class="g2e-subtitle">Platform:</td>' +
							'<td id="g2e-confirm-tbl-pltf"></td>' +
							'<td class="g2e-edit">Edit</td>' +
						'</tr>' +
						'<tr>' +
							'<td class="g2e-subtitle">Species:</td>' +
							'<td id="g2e-confirm-tbl-spcs"></td>' +
							'<td class="g2e-edit">Edit</td>' +
						'</tr>' +
						'<tr>' +
							'<td class="g2e-subtitle">Control:</td>' +
							'<td id="g2e-confirm-tbl-ctrl"></td>' +
							'<td></td>' +
						'</tr>' +
						'<tr>' +
							'<td class="g2e-subtitle">Experimental:</td>' +
							'<td id="g2e-confirm-tbl-expmt"></td>' +
							'<td></td>' +
						'</tr>' +
					'</table>' +
				'</div>' +
				'<div id="g2e-footer">' +
					'<div class="g2e-lowlight">What would you like to do with your differentially expressed genes?</div>' +
					'<div id="g2e-actions" class="column left">' +
						'<button id="g2e-submit-btn" class="g2e-btn">Submit to Enrichr</button>' +
						'<button id="g2e-download-btn" class="g2e-btn">Download as text files</button>' +
					'</div>' +
					'<div id="g2e-progress-bar" class="column right">' +
						'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
						'<div id="g2e-step2" class="g2e-progress">Identifying differential expression</div>' +
						'<div id="g2e-step3" class="g2e-progress">Submitting genes to Enrichr</div>' +
						'<div id="g2e-step4" class="g2e-progress">Done!</div>' +
					'</div>' +
				'</div>'
			'</div>' +
		'</div>';

	var templates = {
		'gds': {
			'modal': modal,
			'btn': '' +
				'<tr>' +
					// "azline" comes from the GEO website.
					'<td class="azline" id="g2e-embedded-button">' +
						'<b>Step 4: </b>' +
						'<span id="g2e-link">Pipe into Enrichr</span>' +
						'<img src="http://amp.pharm.mssm.edu/Enrichr/images/enrichr-icon.png">' +
					'</td>' +
				'</tr>'
		},
		'gse': {
			'modal': modal,
			'btn': '' +
				'<tr>' +
					'<td id="g2e-embedded-button">' +
						'<span id="g2e-link">Pipe into Enrichr</span>' +
						'<img src="http://amp.pharm.mssm.edu/Enrichr/images/enrichr-icon.png">' +
					'</td>' +
				'</tr>',
			'thead': '' +
				'<tr valign="top" id="g2e-table-title">' +
					'<td></td>' +
					'<td></td>' +
					'<td class="g2e-ctrl">Ctrl</td>' +
					'<td class="g2e-expmt">Expmt</td>' +
				'</tr>',
			'chkbxs': '' +
				'<td>' +
					'<input class="g2e-chkbx g2e-control" type="checkbox" />' +
				'</td>' +
				'<td>' +
					'<input class="g2e-chkbx g2e-experimental" type="checkbox" />' +
				'</td>'
		}
	};

	app.html.get = function(el) {
		return templates[app.mode.key][el];
	};
		
})(GEO2Enrichr, jQuery);