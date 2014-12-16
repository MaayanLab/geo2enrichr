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
				'<table id="g2e-main-tbl"><tr>' +
					'<td id="g2e-forms" class="g2e-column g2e-left">' +
						'<div class="g2e-form">' +
							'<h4>Method to identify differential expression</h4>' +
							'<div class="g2e-block">' +
								'<input id="g2e-chdir" type="radio" name="method" value="chdir" checked="checked">' +
								'<label for="g2e-chdir" class="g2e-lbl">' +
									'<span>Characteristic direction</span>' +
									'<a href="http://www.maayanlab.net/CD/" target="_blank">(more)</a>' +
								'</label>' +
							'</div>' +
							'<div class="g2e-block">' +
								'<input id="g2e-ttest" type="radio" name="method" value="ttest">' +
								'<label for="g2e-ttest" class="g2e-lbl">T-test</label>' +
							'</div>' +
						'</div>' +
						'<div class="g2e-form g2e-last">' +
							'<h4>Gene list inclusion</h4>' +
							'<div class="g2e-block">' +
								'<input id="g2e-up" type="radio" name="inclusion" value="up" checked="checked">' +
								'<label for="g2e-up" class="g2e-lbl">Up genes</label>' +
							'</div>' +
							'<div class="g2e-block">' +
								'<input id="g2e-down" type="radio" name="inclusion" value="down">' +
								'<label for="g2e-down" class="g2e-lbl">Down genes</label>' +
							'</div>' +
							'<div class="g2e-block">' +
								'<input id="g2e-both" type="radio" name="inclusion" value="both">' +
								'<label for="g2e-both" class="g2e-lbl">Both</label>' +
							'</div>' +
						'</div>' +
					'</td>' +
					'<td id="g2e-confirm" class="g2e-column g2e-right">' +
						'<div class="g2e-lowlight">GEO2Enrichr must screen scrape to collect some of the data.<br>Please confirm it is correct.</div>' +
						'<table id="g2e-confirm-tbl">' +
							'<tr>' +
								'<td class="g2e-subtitle">Accession #:</td>' +
								'<td id="g2e-confirm-tbl-acc" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Platform:</td>' +
								'<td id="g2e-confirm-tbl-pltf" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Organism:</td>' +
								'<td id="g2e-confirm-tbl-org" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Control:</td>' +
								'<td id="g2e-confirm-tbl-ctrl" class="g2e-strong"></td>' +
								'<td></td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Experimental:</td>' +
								'<td id="g2e-confirm-tbl-expmt" class="g2e-strong"></td>' +
								'<td></td>' +
							'</tr>' +
						'</table>' +
						'<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations.<br>They are useful as meta data and for file naming.</div>' +
						'<table id="g2e-confirm-tbl">' +
							'<tr>' +
								'<td class="g2e-subtitle">Cell type or tissue:</td>' +
								'<td id="g2e-confirm-cell" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Perturbation:</td>' +
								'<td id="g2e-confirm-pert" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
						'</table>' +
					'</td>' +
				'</tr></table>' +
				'<div id="g2e-footer">' +
					'<div class="g2e-lowlight">What would you like to do with your differentially expressed genes?</div>' +
					'<table><tr>' +
						'<td id="g2e-actions" class="g2e-column g2e-left">' +
							'<button id="g2e-submit-btn" class="g2e-btn">Submit to Enrichr</button>' +
						'</td>' +
						'<td id="g2e-output" class="g2e-column g2e-right">' +
							'<div id="g2e-progress-bar">' +
								'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
								'<div id="g2e-step2" class="g2e-progress">Identifying differential expression</div>' +
								'<div id="g2e-step3" class="g2e-progress">Submitting genes to Enrichr</div>' +
								'<div id="g2e-step4" class="g2e-progress">Done!</div>' +
							'</div>' +
							'<div id="g2e-results">' +
								'<h4>Your data is ready:</h4>' +
								'<button href="">Open in Enrichr</button>' +
								'<button id="g2e-download-btn" class="g2e-btn">Download gene list(s)</button>' +
							'</div>' +
						'</td>' +
					'</tr></table>' +
				'</div>' +
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
		return templates[app.mode.key][el] || templates[el];
	};
		
})(GEO2Enrichr, jQuery);