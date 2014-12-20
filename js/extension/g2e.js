
var G2E = (function() {


var Comm = function(events, notifier, scraper, SERVER) {

	var ENTRY_POINT = 'g2e/',
		fileForDownload = [];

	// We need to make back-to-back AJAX requests to get the relevant data.
	// Querying GEO's esearch endpoint with an accession number returns some JSON with an ID.
	// Then we query GEO's esummary endpoint with the ID.
	// Finally, we fire an event so that any modules that want this data can subscribe.
	var fetchMetadata = function(accession) {
		var EUTILS_BASE = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
			DB = 'db=gds',
			SETTINGS = '&retmax=1&retmode=json',
			EUTILS_SEARCH = EUTILS_BASE + 'esearch.fcgi?' + DB + SETTINGS,
			EUTILS_SUMMARY = EUTILS_BASE + 'esummary.fcgi?' + DB + SETTINGS;
		$.ajax({
			url: EUTILS_SEARCH + '&term=' + accession + '[ACCN]',
			type: 'GET',
			success: function(search_data) {
				var id = search_data.esearchresult.idlist[0];
				$.ajax({
					url: EUTILS_SUMMARY + '&id=' + id,
					type: 'GET',
					success: function(summaryData) {
						events.fire('metadataFetched', summaryData.result[id]);
					},
					error: errorHandler
				});
			}
		});
	};

	// This is the workhorse function that chains together multiple AJX requests to the back-end.
	var downloadDiffexpEnrich = function($modal) {
		var userInput = scraper.getData($modal);

		function dlgeo() {
			var endpoint = 'dlgeo?',
				qs = $.param({
					accession: userInput.accession,
					organism: userInput.organism,
					platform: userInput.platform,
					method: userInput.method,
					cell: userInput.cell,
					perturbation: userInput.perturbation
				});

			return $.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('GEO files were downloaded');
					notifier.log(data);
					events.fire('progressBar');
				},
				error: errorHandler
			});
		}

		function diffexp(dlgeoData) {
			var endpoint = 'diffexp?',
				qs = $.param({
					// This is the SOFT file, not the gene file.
					filename: dlgeoData.filename,
					platform: userInput.platform,
					method: userInput.method,
					inclusion: userInput.inclusion,
					control: userInput.control.join('-'),
					experimental: userInput.experimental.join('-')
				});

			return $.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('GEO files were differentially expressed');
					notifier.log(data);
					events.fire('progressBar');
				},
				error: errorHandler
			});
		}

		function enrichr(diffexpData) {
			var endpoint = 'enrichr?',
				qs;

			fileForDownload = diffexpData.filename;
			qs = 'filename=' + fileForDownload;

			$.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('Enrichr link was returned');
					notifier.log(data);
					events.fire('progressBar');
					data.fileForDownload = SERVER + 'static/genes/' + fileForDownload;
					events.fire('dataDownloaded', data);
				},
				error: errorHandler
			});
		}

		dlgeo().then(diffexp).then(enrichr);
	};

	var fetchGenemap = function() {
		$.ajax({
			url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('genemapDownloaded', data);
			}
		});
	};

	var errorHandler = function(data) {
		events.fire('requestFailed', data.responseText);
	};

	return {
		downloadDiffexpEnrich: downloadDiffexpEnrich,
		fetchMetadata: fetchMetadata,
		fetchGenemap: fetchGenemap
	};
};


var Events = function() {

	var channel = {};

	var fire = function(eventName, args) {
		if (!channel[eventName]) {
			return false;
		}
		var i = 0,
			len = channel[eventName].length;
		for (; i < len; i++) {
			channel[eventName][i](args);
		}
	};

	var on = function(eventName, callback) {
		if (!channel[eventName]) {
			channel[eventName] = [];
		}
		channel[eventName].push(callback);
	};

	return {
		on: on,
		fire: fire,
	};
};


var Html = function() {

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
								'<input id="g2e-combined" type="radio" name="inclusion" value="combined">' +
								'<label for="g2e-combined" class="g2e-lbl">Combined</label>' +
							'</div>' +
						'</div>' +
					'</td>' +
					'<td id="g2e-confirm" class="g2e-column g2e-right">' +
						'<div class="g2e-lowlight">Please confirm your data is correct.</div>' +
						'<table class="g2e-confirm-tbl">' +
							'<tr>' +
								'<td class="g2e-subtitle">Accession num.&#42;:</td>' +
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
								'<td class="g2e-subtitle">Control:&#42;</td>' +
								'<td id="g2e-confirm-tbl-ctrl" class="g2e-strong"></td>' +
								'<td></td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle">Experimental:</td>' +
								'<td id="g2e-confirm-tbl-expmt" class="g2e-strong"></td>' +
								'<td></td>' +
							'</tr>' +
						'</table>' +
						'<div class="g2e-lowlight g2e-bottom">Please provide the manipulated gene.&#42;</div>' +
						'<div class="ui-widget">' +
							'<label for="genemap">Gene: </label>' +
							'<input id="genemap">' +
						'</div>' +
						'<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations.</div>' +
						'<table class="g2e-confirm-tbl">' +
							'<tr>' +
								'<td class="g2e-subtitle" title="This is useful for meta data and file naming">Cell type or tissue:</td>' +
								'<td id="g2e-confirm-cell" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
							'<tr>' +
								'<td class="g2e-subtitle" title="This is useful for meta data and file naming">Perturbation:</td>' +
								'<td id="g2e-confirm-pert" class="g2e-strong"></td>' +
								'<td class="g2e-edit">Edit</td>' +
							'</tr>' +
						'</table>' +
					'</td>' +
				'</tr></table>' +
				'<div id="g2e-footer">' +
					'<table><tr>' +
						'<td id="g2e-actions" class="g2e-column g2e-left">' +
							'<button id="g2e-submit-btn" class="g2e-btn" title="This can take a while.">Submit to Enrichr</button>' +
						'</td>' +
						'<td id="g2e-output" class="g2e-column g2e-right">' +
							'<div id="g2e-progress-bar">' +
								'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
								'<div id="g2e-step2" class="g2e-progress">Identifying differential expression</div>' +
								'<div id="g2e-step3" class="g2e-progress">Submitting genes to Enrichr</div>' +
								'<div id="g2e-step4" class="g2e-progress">Done!</div>' +
							'</div>' +
							'<div id="g2e-results">' +
								'<strong>Your data is ready:</strong>' +
								'<button href="">Open in Enrichr</button>' +
								'<button id="g2e-download-btn" class="g2e-btn">Download gene list(s)</button>' +
							'</div>' +
						'</td>' +
					'</tr></table>' +
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
						'<img src="http://amp.pharm.mssm.edu/Enrichr/images/enrichr-icon.png">' +
					'</td>' +
				'</tr>'
		},
		'gse': {
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

	return {
		get: function(el, key) {
			if (key) {
				return templates[key][el];
			}
			return templates[el];
		}
	};
};


var Notifier = function(DEBUG) {

	var log = function(msg) {
		if (DEBUG) {
			console.log(msg);
		}
	};

	var ask = function(msg, deflt) {
		return prompt(msg, deflt);
	};

	var warn = function(msg) {
		alert(msg);
	};

	return {
		log: log,
		ask: ask,
		warn: warn
	};
};


var BaseScraper = function(notifier) {

	var scrapedData = {};

	return {

		getData: function($modal) {
			var result;
			if ($modal) {
				this.getOptions($modal);
			}
			if (this.isValidData(scrapedData)) {
				result = $.extend({}, scrapedData);
				// TODO!!!!
				//ui.fill_confirm_tbl(result);
				return result;
			}
		},

		setData: function(key, val) {
			// Store any data we might overwrite.
			var temp = scrapedData[key];
			if (key == 'cell' || key == 'platform') {
				val = val.replace(/_|-|\./g, '');
			}
			scrapedData[key] = val;
			if (this.isValidData(scrapedData)) {
				// TODO: This should be handled by UI!
				ui.fill_confirm_tbl($.extend({}, scrapedData));	
			} else {
				scrapedData[key] = temp;
			}
		},

		scrapeData: function($modal) {
			var samples = this.getSamples();

			// `__scrape_options()` and `__scrape_annotations()` are called on `getData()`,
			// i.e. when the user clicks submit.
			scrapedData.control      = samples.control;
			scrapedData.experimental = samples.experimental;
			scrapedData.accession    = this.getAccession();
			scrapedData.organism     = this.getOrganism();
			scrapedData.platform     = this.getPlatform();

			if (this.isValidData(scrapedData)) {
				return $.extend({}, scrapedData);
			}
			return undefined;
		},

		getOptions: function($modal) {
			var method = $modal.find('input[type=radio][name=method]:checked').val(),
				inclusion = $modal.find('input[type=radio][name=inclusion]:checked').val(),
				cell = $modal.find('#g2e-confirm-cell').text(),
				perturbation = $modal.find('#g2e-confirm-pert').text();

			if (method) {
				scrapedData.method = method;
			}
			if (inclusion) {
				scrapedData.inclusion = inclusion;	
			}

			if (cell) {
				scrapedData.cell = cell.replace(/_|\.|-/, '');
			}
			if (perturbation) {
				scrapedData.perturbation = perturbation.replace(/_|\.|-/, '');	
			}
		},

		textFromHtml: function($el) {
			if (!($el instanceof $)) {
				$el = $($el);
			}

			return $el.contents().filter(function() {
				return this.nodeType == 3;
			}).text().trim();
		},

		normalizeText: function(el) {
			return el.replace(/\s/g, '').toLowerCase();
		},

		isValidData: function(data) {
			if (!data.control || data.control.length < 2) {
				notifier.warn('Please select 2 or more control samples');
				return false;
			}
			if (!data.experimental || data.experimental.length < 2) {
				notifier.warn('Please select 2 or more experimental samples');
				return false;
			}
			return true;
		}
	};	
};


var GdsScraper = function(events) {

	var $details,
		$hook,
		metadata = {};

	events.on('embedded', function(hook) {
		$hook = hook;
	});

	events.on('metadataFetched', function(data) {
		metadata = data;
	});

	return {
		
		init: function() {
			$details = $('#gds_details');
		},

		getAccession: function() {
			return metadata.accession || this.getAccessionFromPage();
		},

		getOrganism: function() {
			return this.getByName('organism');
		},

		getPlatform: function() {
			return this.getByName('platform');
		},

		getSamples: function() {
			var $groupRow = $($hook.children().find('tbody td')[0]),
				bkp_not_found = true,
				samplesStr = this.textFromHtml($groupRow),
				samplesArr = samplesStr.split(' '),
				samplesBkpIdx, control, experimental;

			$.each(samplesArr, function(i, val) {
				if (bkp_not_found && val.substr(val.length-1) !== ',') {
					samplesBkpIdx = i+1;
					bkp_not_found = false;
				} else {
					// WARNING: we're mutating the list while iterating over it. 
					// This should be okay since we're just trimming the comma.
					samplesArr[i] = val.replace(',', '');
				}
			});

			return {
				control: samplesArr.slice(0, samplesBkpIdx),
				experimental: samplesArr.slice(samplesBkpIdx, samplesArr.length)
			};
		},

		getByName: function(name) {
			// 1. Grab the text from the appropriate row
			// 2. Strip out all the whitespace (newlines, tabs, etc.)
			// 3. Split on the semicolon (notice there are two) and return just the code.
			var idx = this.getRowIdxFromName(name);
			var text = $($details.find('tr')[idx]).text();
			// Remove any preceding whitespace.
			return text.split(':')[1].replace(/\s*/, '');
		},

		getRowIdxFromName: function(attrName) {
			var self = this,
				result;
			$details.find('tr').each(function(i, tr) {
				var titleEl = $(tr).find('th')[0],
					titleText = self.normalizeText($(titleEl).text()),
					titleName = titleText.split(':')[0];
				if (titleName === attrName) {
					result = i;
					return false;
				}
			});
			return result;
		},

		getAccessionFromPage: function() {
			var record_caption = $details.find('.caption').text(),
				re = new RegExp(/(?:GDS|GSE)[0-9]*/);
			return re.exec(record_caption)[0];
		}
	};
};


var GseScraper = function(events, html) {

	var key = 'gse',
		$details,
		metadata = {};

	events.on('metadataFetched', function(data) {
		metadata = data;
	});

	return {

		init: function() {
			var $samplesTable;

			// Find the details table.
			$('table').each(function(i, el) {
				var $el = $(el);
				if ($el.attr('width') === '600' &&
					$el.attr('cellpadding') === '2' &&
					$el.attr('cellspacing') === '0')
				{
					$details = $el;
					return false;
				}
			});

			// Find the samples from the details table.
			$details.find('tr').each(function(i, tr) {
				if ($(tr).find('td')
						 .first()
						 .text()
						 .toLowerCase()
						 .indexOf('samples') === 0)
				{
					$samplesTable = $(tr);
					return false;
				}
			});

			$samplesTable.find('tr').each(function(i, tr) {
				$(tr).append(html.get('chkbxs', 'gse'));
			});

			$samplesTable.find('table')
						  .first()
						  .find('tr')
						  .first()
						  .before(html.get('thead'));
		},

		getByName: function(name) {
			var idx = this.getRowIdxByName(name);
			return $($details.find('tr')[idx]).find('a').text();
		},

		getRowIdxByName: function(attr_name) {
			var self = this,
				result;
			$details.find('tr').each(function(i, tr) {
				var text = $(tr).find('td')
								.first()
								.text();
				text = self.normalizeText(text).replace(/[^a-zA-Z]/g, '');
				if (text === attr_name) {
					result = i;
					return false;
				}
			});
			return result;
		},

		// If required, this can be used as a general purpose query param getter.
		// The accession number is not necessarily in the URL for GDS.
		// Should we check anyway?
		getAccessionFromUrl: function() {
			var params = window.location.search.substring(1).split('&'),
				i = 0,
				len = params.length;
			for (; i < len; i++)  {
				var keyVal = params[i].split('=');
				if (keyVal[0] == 'acc') {
					return keyVal[1];
				}
			}
		},

		getAccession: function() {
			var accession = this.getAccessionFromUrl();
			if (accession) {
				return accession;
			} else if (metadata.accession) {
				return metadata.accession;
			}
		},

		getOrganism: function() {
			if (typeof metadata !== 'undefined' && metadata.taxon) {
				return metadata.taxon;
			}
			return this.getByName('organism');
		},

		getPlatform: function() {
			return this.getByName('platforms');
		},

		getSamples: function() {
			var control = [],
				experimental = [];

			$('.g2e-chkbx').each(function(i, input) {
				var $input = $(input),
					gene;
				if ($input.is(':checked')) {
					gene = $(input).parent()
								   .siblings()
								   .first()
								   .find('a')
								   .text();

					if ($input.hasClass('g2e-control')) {
						control.push(gene);
					} else if ($input.hasClass('g2e-experimental')) {
						experimental.push(gene);
					}
				}
			});

			return {
				control: control,
				experimental: experimental
			};
		}
	};
};


var BaseUi = function(comm, events, html, notifier, scraper) {

	var $downloadIframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body'),
		elemConfig = {
			'g2e-confirm-tbl-acc': {
				key: 'accession',
				prompt: 'Please enter an accession number:'
			},
			'g2e-confirm-tbl-pltf': {
				key: 'platform',
				prompt: 'Please enter a platform:'
			},
			'g2e-confirm-tbl-org' : {
				key: 'organism',
				prompt: 'Please enter an organism:'
			},
			'g2e-confirm-tbl-ctrl': {
				key: 'control',
				format: function(data) {
					return data.join(', ');
				}
			},
			'g2e-confirm-tbl-expmt': {
				key: 'experimental',
				format: function(data) {
					return data.join(', ');
				}
			},
			'g2e-confirm-cell': {
				key: 'cell',
				prompt: 'Please enter a cell type or tissue:'
			},
			'g2e-confirm-pert': {
				key: 'perturbation',
				prompt: 'Please enter perturbation:'
			}
		},
		steps, $overlay, $modal, $progress, $results;

	events.on('requestFailed', function(errorMsg) {
		notifier.warn(errorMsg);
		resetProgressBar();
	});

	events.on('genemapDownloaded', function(genemap) {
		$('#genemap').autocomplete({
			source: function(request, response) {
				var results = $.ui.autocomplete.filter(genemap, request.term);
				response(results.slice(0, 10));
			},
			minLength: 2,
			delay: 500,
			autoFocus: true
		});
	});

	var openApp = function() {
		var scrapedData;

		// Show the user the data we have scraped for confirmation.
		scrapedData = scraper.scrapeData($modal);
		if (scrapedData) {
			fillConfirmTable(scrapedData);
			showModalBox();
		}
	};

	var setup = function() {
		setGlobalSelectors();

		// Allow editing of the values, in case we scraped incorrectly.
		$('.g2e-edit').click(function(evt) {
			var id = $(evt.currentTarget).siblings().eq(1).attr('id');
			onEdit(id);
		});

		// Add event handlers
		$modal.find('#g2e-close-btn')
			  .click(resetUi)
			  .end()

			  .find('#g2e-submit-btn')
			  .click(function() {
			      notifier.log('Input data was scraped');
			      notifier.log(scraper.getData($modal));
			      initProgressBar();
			      events.on('progressBar', highlightNextStep);
			      comm.downloadDiffexpEnrich($modal);
			  })
			  .tooltip()
			  .end()

			  .find('.g2e-confirm-tbl')
			  .eq(1)
			  .tooltip()
			  .end();
	};

	var initProgressBar = function() {
		resetProgressBar();
		steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];
		$progress.show();
		highlightNextStep();
	};

	var highlightNextStep = function() {
		$progress.find(steps.shift()).addClass('g2e-ready');
	};

	// `scraper` also calls this when new data is set.
	// TODO: It shouldn't.
	var fillConfirmTable = function(scrapedData) {
		var elem, config, html;
		for (elem in elemConfig) {
			config = elemConfig[elem];
			if (config.format) {
				html = config.format(scrapedData[config.key]);
			} else {
				html = scrapedData[config.key];
			}
			$('#' + elem).html(html);
		}
	};

	var showResults = function(link) {
		$results.show()
				.find('button')
				.first()
				.click(function() {
					window.open(link, '_blank');
				});
	};

	var resetResults = function() {
		$results.hide()
				.find('button')
				.first()
				.unbind();
	};

	var showModalBox = function() {
		$overlay.show();
		$modal.show();
	};

	var hideModalBox = function() {
		$overlay.hide();
		$modal.hide();
	};

	var setGlobalSelectors = function() {
		var htmlData = html.get('modal');
		$overlay = $(htmlData).hide().appendTo('body');
		$modal = $('#g2e-container #g2e-modal').draggable();
		$progress = $progress || $('#g2e-progress-bar');
		$results = $results || $('#g2e-results');		
	};

	var resetUi = function() {
		hideModalBox();
		resetProgressBar();
	};

	var resetProgressBar = function() {
		$progress.hide()
				 .find('.g2e-progress')
				 .removeClass('g2e-ready');
		resetResults();
	};

	var onEdit = function(id) {
		var config = elemConfig[id],
			userInput = notifier.ask(config.prompt, $('#' + id).text());
		if (userInput !== null) {
			scraper.set_data(config.key, userInput);
		}
	};

	var downloadUrl = function(url) {
		$downloadIframe.attr('src', url);
	};

	events.on('dataDownloaded', function(data) {
		showResults(data.link);
		$modal.find('#g2e-download-btn')
			  .click(function() {
			      downloadUrl(data.fileForDownload);
			  });
	});

	setup();

	return {
		openApp: openApp,
		initProgressBar: initProgressBar,
		highlightNextStep: highlightNextStep,
		showResults: showResults
	};
};


var GdsUi = function(html, events) {

	return {

		embed: function($hook) {
			var self = this;
			$hook.children().last().after(html.get('btn', 'gds'));
			$('#g2e-link').click(function() {
				self.openApp();
			});
		},

		init: function() {
			var self = this,
				id;
			id = setInterval(function() {
				var $hook = $('#diff_express > tbody');
				if ($hook.length) {
					events.fire('embedded', $hook);
					self.embed($hook);
					clearInterval(id);
				}
			}, 250);
		}
	};
};


var GseUi = function(html, events) {

	return {

		embed: function($hook) {
			var self = this;
			$hook.append(html.get('btn', 'gse'));
			$('#g2e-link').click(function() {
				self.openApp();
			});
		},

		init: function() {
			// Go up two parents to find the table.
			var $hook = $('#geo2r').next();
			if ($hook) {
				this.embed($hook);
			}
		}
	};
};



var main = function() {

	var isGds = function() {
		var path;
		if (window.location.pathname !== '/') {
			path = window.location.pathname.split('/')[1];
			if (path === 'sites') {
				return true;
			} else if (path === 'geo') {
				return false;
			}
		}
	};

	var init = function() {
		// Set these configuration values before deploying.
		var DEBUG = false,
			SERVER = 'http://amp.pharm.mssm.edu/',

			events = Events(),
			notifier = Notifier(DEBUG),
			html = Html(),

			scraper,
			ui,
			comm;

		if (isGds()) {
			scraper = $.extend(GdsScraper(events), BaseScraper(notifier));
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GdsUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		} else {
			scraper = $.extend(GseScraper(events, html), BaseScraper(notifier));
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GseUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		}

		// This executes in the background, collecting information about the page before the user even inputs.
		if (scraper.getAccessionFromUrl) {
			comm.fetchMetadata( scraper.getAccessionFromUrl() );
		}

		// Fetch and store the gene map for later.
		comm.fetchGenemap();

		scraper.init();
		ui.init();
		notifier.log('g2e loaded.');
	};

	init();
};


	window.onload = main();

})(jQuery);
