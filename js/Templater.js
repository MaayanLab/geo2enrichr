
var Templater = function(EXTENSION_ID) {

	var LOGO50X50 = 'chrome-extension://' + EXTENSION_ID + '/images/g2e-logo-50x50.png';

	var modal = '' +
		'<div id="g2e-container">' +
			'<div id="g2e-modal">' +
				'<div id="g2e-title">' +
					'<a href="http://maayanlab.net/g2e/" target="_blank">' +
						'<img src="' + LOGO50X50 + '">' +
						'<span>GEO+</span>' +
						'<span id="g2e-target-app" class="g2e-highlight">Enrichr</span>' +
					'</a>' +
				'</div>' +
            	'<div id="g2e-nav">' +
                    '<select>' +
                        '<option value="Enrichr">Enrichr</option>' +
                        '<option value="Sigine">Sigine</option>' +
                    '</select>' +
                    '<button id="g2e-close-btn" class="g2e-btn">&#10006</button>' +
                '</div>' +
                '<div class="g2e-clear"></div>' +
				'<table id="g2e-main-tbl">' +
					'<tr>' +
						'<td id="g2e-confirm">' +
							'<div class="g2e-lowlight">Please confirm that your data is correct, *required.</div>' +
							'<table class="g2e-confirm-tbl">' +
								'<tr id="g2e-diffexp">' +
									'<td class="g2e-title">' +
										'<label>Differential expression method</label>' +
									'</td>' +
									'<td class="g2e-value">' +
										'<select>' +
											'<option>Characteristic direction</option>' +
											'<option>T-test</option>' +
										'</select>' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-accession">' +
									'<td class="g2e-title">Accession num.&#42;</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-platform">' +
									'<td class="g2e-title">Platform</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-organism">' +
									'<td class="g2e-title">Organism</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-control">' +
									'<td class="g2e-title">Control samples&#42;</td>' +
									'<td class="g2e-value"></td>' +
								'</tr>' +
								'<tr id="g2e-experimental" class="g2e-last">' +
									'<td class="g2e-title">Treatment or condition samples&#42;</td>' +
									'<td class="g2e-value"></td>' +
								'</tr>' +
							'</table>' +
							'<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations, **if relevant.</div>' +
							'<table class="g2e-confirm-tbl">' +
								'<tr id="g2e-confirm-cell">' +
									'<td class="g2e-title">' +
										'<label>Cell type or tissue</label>' +
									'</td>' +
									'<td class="g2e-value">' +
										'<input placeholder="No data">' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-pert">' +
									'<td class="g2e-title">' +
										'<label>Perturbation</label>' +
									'</td>' +
									'<td class="g2e-value">' +
										'<input placeholder="No data">' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-gene" class="ui-widget">' +
									'<td class="g2e-title">' +
										'<label for="geneList">Manipulated gene**</label>' +
									'</td>' +
									'<td class="g2e-value">' +
										'<input id="geneList" placeholder="No data">' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-disease" class="ui-widget g2e-last">' +
									'<td class="g2e-title">' +
										'<label for="diseaseList">Rare disease**</label>' +
									'</td>' +
									'<td class="g2e-value g2e-last">' +
										'<input id="diseaseList" placeholder="No data">' +
									'</td>' +
								'</tr>' +
							'</table>' +
						'</td>' +
					'</tr>' +
				'</table>' +
				'<div id="g2e-footer">' +
					'<table>' +
						'<tr>' +
							'<td id="g2e-actions" class="g2e-title">' +
								'<button id="g2e-submit-btn" class="g2e-btn">Extract gene lists</button>' +
							'</td>' +
							'<td id="g2e-progress-bar">' +
								'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
								'<div id="g2e-step2" class="g2e-progress">Cleaning data and identifying differential expression</div>' +
								'<div id="g2e-step3" class="g2e-progress">Enriching gene lists</div>' +
								'<div id="g2e-step4" class="g2e-progress">Done!</div>' +
							'</td>' +
						'</tr>' +
						'<tr class="g2e-results">' +
							'<td class="g2e-title">' +
								'<strong>Enriched genes:</strong>' +
							'</td>' +
							'<td class="g2e-title">' +
								'<button id="g2e-enrichr-up">Up</button>' +
								'<button id="g2e-enrichr-down">Down</button>' +
								'<button id="g2e-enrichr-combined">All</button>' +
							'</td>' +
						'</tr>' +
						'<tr class="g2e-results">' +
							'<td class="g2e-title">' +
								'<strong>Downloads:</strong>' +
							'</td>' +
							'<td>' +
								'<button id="g2e-download-btn" class="g2e-btn">Download gene list</button>' +
							'</td>' +
						'</tr>' +
					'</table>' +
                    '<p id="g2e-credits">' + 
                        'GEO+ is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
                        ' See the <a href="http://maayanlab.net/g2e/" target="_blank">documentation</a> for details.' +
                    '</p>' +
                '</div>' +
			'</div>' +
		'</div>';

    var BUTTON_TEXT = 'Open <strong class="g2e-strong">GEO+</strong>';

	var templates = {
		'modal': modal,
		'gds': {
			'btn': '' +
				'<tr>' +
					// "azline" comes from the GEO website.
					'<td class="azline" id="g2e-embedded-button">' +
						'<b>Step 4: </b>' +
						'<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
						'<img src="' + LOGO50X50 + '">' +
					'</td>' +
				'</tr>'
		},
		'gse': {
			'btn': '' +
				'<tr>' +
					'<td id="g2e-embedded-button">' +
						'<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
						'<img src="' + LOGO50X50 + '">' +
					'</td>' +
				'</tr>',
			'thead': '' +
			    // TODO: Rename "table-title" to "title"
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

	return {
		get: function(el, key) {
		    var template;
			if (key) {
				template = templates[key][el];
			} else {
			    template = templates[el];
			}
			return $(template);
		}
	};
};
