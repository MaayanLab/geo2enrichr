
var Html = function() {

	var LOGO50X50 = 'chrome-extension://jmocdkgcpalhikedehcdnofimpgkljcj/images/g2e-logo-50x50.png';

	var modal = '' +
		'<div id="g2e-container">' +
			'<div id="g2e-modal">' +
				'<div id="g2e-title">' +
					'<a href="http://amp.pharm.mssm.edu/Enrichr/" target="_blank">' +
						'<img src="' + LOGO50X50 + '">' +
						'<span>GEO2</span><span class="g2e-highlight">Enrichr</span>' +
					'</a>' +
					'<button id="g2e-close-btn" class="g2e-btn">&#10006</button>' +
				'</div>' +
				'<table id="g2e-main-tbl">' +
					'<tr>' +
						'<td id="g2e-confirm" class="g2e-column g2e-left">' +
							'<div class="g2e-lowlight">Please confirm that your data is correct. An asterisk denotes a required field.</div>' +
							'<table class="g2e-confirm-tbl">' +
								'<tr id="g2e-confirm-tbl-diffexp">' +
									'<td class="g2e-tbl-title">' +
										'<label>Differential expression method</label>' +
									'</td>' +
									'<td class="g2e-tbl-value">' +
										'<select>' +
											'<option>Characteristic direction</option>' +
											'<option>T-test</option>' +
										'</select>' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-tbl-acc">' +
									'<td class="g2e-tbl-title">Accession num.&#42;</td>' +
									'<td class="g2e-tbl-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-confirm-tbl-pltf">' +
									'<td class="g2e-tbl-title">Platform</td>' +
									'<td class="g2e-tbl-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-confirm-tbl-org">' +
									'<td class="g2e-tbl-title">Organism</td>' +
									'<td class="g2e-tbl-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-confirm-tbl-ctrl">' +
									'<td class="g2e-tbl-title">Control samples&#42;</td>' +
									'<td class="g2e-tbl-value"></td>' +
								'</tr>' +
								'<tr id="g2e-confirm-tbl-expmt" class="g2e-tbl-last">' +
									'<td class="g2e-tbl-title">Treatment or condition samples&#42;</td>' +
									'<td class="g2e-tbl-value"></td>' +
								'</tr>' +
							'</table>' +
							'<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations.</div>' +
							'<table class="g2e-confirm-tbl">' +
								'<tr id="g2e-confirm-cell">' +
									'<td class="g2e-tbl-title">' +
										'<label>Cell type or tissue</label>' +
									'</td>' +
									'<td class="g2e-tbl-value">' +
										'<input placeholder="No data">' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-pert">' +
									'<td class="g2e-tbl-title">' +
										'<label>Perturbation</label>' +
									'</td>' +
									'<td class="g2e-tbl-value">' +
										'<input placeholder="No data">' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-confirm-gene" class="ui-widget g2e-tbl-last">' +
									'<td class="g2e-tbl-title">' +
										'<label for="genemap">Manipulated gene (if relevant)</label>' +
									'</td>' +
									'<td class="g2e-tbl-value g2e-tbl-last">' +
										'<input id="genemap" placeholder="No data">' +
									'</td>' +
								'</tr>' +
							'</table>' +
						'</td>' +
						'<td class="g2e-column g2e-right">' +
							'<p>GEO2Enrichr performs the following operations:</p>' +
							'<ol id="g2e-process">' +
								'<li>Downloads SOFT file from GEO.</li>' +
								'<li >Discards data with missing values or one-to-many probe-to-gene mappings.</li>' +
								'<li>log2 transforms the data if necessary.</li>' +
								'<li>Quantile normalizes the data if necessary.</li>' +
								'<li>Averages multiple probes to single genes.</li>' +
								'<li>Identifies differentially expressed genes with the selected method.</li>' +
								'<li>Returns the top and bottom differentially expressed genes.</li>' +
								'<li>Pipes the gene lists to <a href="http://amp.pharm.mssm.edu/Enrichr/" target="_blank">Enrichr</a> for further analysis.</li>' +
							'</ol>' +
							'<p>After the data is processed, you will be able to download your gene lists and open them directly in Enrichr.</p>' +
							'<p id="g2e-credits">GEO2Enrichr is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
						'</td>' +
					'</tr>' +
				'</table>' +
				'<div id="g2e-footer">' +
					'<div>' +
						'<div id="g2e-actions">' +
							'<button id="g2e-submit-btn" class="g2e-btn" title="This can take a while.">Get gene lists</button>' +
						'</div>' +
						'<div id="g2e-progress-bar">' +
							'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
							'<div id="g2e-step2" class="g2e-progress">Cleaning data and identifying differential expression</div>' +
							'<div id="g2e-step3" class="g2e-progress">Done!</div>' +
						'</div>' +
					'</div>' +
					'<table id="g2e-results">' +
						'<tr>' +
							'<td>' +
								'<strong>Enriched genes:</strong>' +
							'</td>' +
							'<td>' +
								'<button id="g2e-enrichr-up">Up</button>' +
								'<button id="g2e-enrichr-down">Down</button>' +
								'<button id="g2e-enrichr-combined">All</button>' +
							'</td>' +
						'</tr>' +
						'<tr>' +
							'<td>' +
								'<strong>Downloads:</strong>' +
							'</td>' +
							'<td>' +
								'<button id="g2e-download-btn" class="g2e-btn">Download gene list</button>' +
							'</td>' +
						'</tr>' +
					'</div>' +
				'</div>' +
			'</div>' +
		'</div>';

	var templates = {
		'modal': modal,
		'gds': {
			'btn': '' +
				'<tr>' +
					// "azline" comes from the GEO website.
					'<td class="azline" id="g2e-embedded-button">' +
						'<b>Step 4: </b>' +
						'<span id="g2e-link">Pipe into Enrichr</span>' +
						'<img src="' + LOGO50X50 + '">' +
					'</td>' +
				'</tr>'
		},
		'gse': {
			'btn': '' +
				'<tr>' +
					'<td id="g2e-embedded-button">' +
						'<span id="g2e-link">Pipe into Enrichr</span>' +
						'<img src="' + LOGO50X50 + '">' +
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

	return {
		get: function(el, key) {
			if (key) {
				return templates[key][el];
			}
			return templates[el];
		}
	};
};
