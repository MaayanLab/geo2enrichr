
var BaseUi = function(comm, events, templater, notifier, scraper) {

	var $downloadIframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body');

	var dataConfig = {
		'g2e-accession': {
			key: 'accession',
			prompt: 'Please enter an accession number:'
		},
		'g2e-platform': {
			key: 'platform',
			prompt: 'Please enter a platform:'
		},
		'g2e-organism' : {
			key: 'organism',
			prompt: 'Please enter an organism:'
		},
		'g2e-control': {
			key: 'control',
			formatter: function(data) {
				return data.join(', ');
			}
		},
		'g2e-experimental': {
			key: 'experimental',
			formatter: function(data) {
				return data.join(', ');
			}
		}
	};
	
	var steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];

	var geneList, $overlay, $modal, $progress, $results;

	// This is called once at startup. All variables and bindings should be permanent.
	var init = function() {
		var htmlData = templater.get('modal');
		$overlay = $(htmlData).hide().appendTo('body');
		$modal = $('#g2e-container #g2e-modal').draggable();
		$progress = $progress || $('#g2e-progress-bar');
		$results = $results || $('.g2e-results');

		// Allow editing of the values, in case we scraped incorrectly.
		$('.g2e-editable').click(function(evt) {
			var id = $(evt.target).parent().attr('id');
			onEdit(id);
		});

		// Add event handlers
		$modal.find('#g2e-close-btn')
			  .click(resetModalBox)
			  .end()
			  .find('.g2e-confirm-tbl')
			  .eq(1)
			  .end();

		resetSubmitBtn();
	};

	// This function is called every time the "Pipe to Enrichr" button is clicked.
	var openModalBox = function() {
		var scrapedData;
		// Show the user the data we have scraped for confirmation.
		scrapedData = scraper.getData($modal);
		fillConfirmationTable(scrapedData);
		showModalBox();
	};

	var highlightNextStep = function() {
		$progress.find(steps.shift()).addClass('g2e-ready');
	};

	var setDownloadLinks = function(downloadLinks) {
		$results.find('#g2e-download-btn')
				.click(function() {
					downloadUrl(downloadLinks.up);
					setTimeout(function() {
						downloadUrl(downloadLinks.down);
					}, 1000);
				})
				.end();
	};

	var showResults = function(enrichrLinks) {
		$results.show()	
				.find('#g2e-enrichr-up')
				.click(function() {
					window.open(enrichrLinks.up, '_blank');
				})
				.end()
				.find('#g2e-enrichr-down')
				.click(function() {
					window.open(enrichrLinks.down, '_blank');
				})
				.end()
				.find('#g2e-enrichr-combined')
				.click(function() {
					window.open(enrichrLinks.combined, '_blank');
				});
	};

	var showModalBox = function() {
		$overlay.show();
		$modal.show();
	};

	var hideModalBox = function() {
		$overlay.hide();
		$modal.hide();
	};

	var resetModalBox = function() {
		resetFooter();
		hideModalBox();
	};

	var resetFooter = function() {
		// Reset progress bar.
		steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];
		$progress.hide()
				 .find('.g2e-progress')
				 .removeClass('g2e-ready');

		// Result any results.
		$results.hide()
				.find('button')
				.first()
				.unbind();

		resetSubmitBtn();	
	};

	var resetSubmitBtn = function() {
		// Reset submit button.
		$modal.find('#g2e-submit-btn')
			  // This doesn't do anything the first time.
			  .removeClass('g2e-lock')
			  // Remove any event handlers, just to be safe.
			  // This code smells like jQuery spaghetti.
			  .off()
			  .click(function() {
				  var scrapedData = scraper.getData($modal);
				  if (isValidData(scrapedData)) {
					  $progress.show();
					  highlightNextStep();
					  $(this).addClass('g2e-lock').off();
					  comm.downloadDiffExp(scrapedData);
				  } else {
					  resetFooter();
				  }
			  })
			  .end();
	};

	var onEdit = function(id) {
		var config = dataConfig[id],
			userInput = notifier.ask(config.prompt, $('#' + id + ' td').eq(1).text()),
			newData;
		if (userInput !== null) {
			scraper.setData(config.key, userInput);
			newData = scraper.getData();
			if (isValidData(newData)) {
				fillConfirmationTable(newData);
			}
		}
	};

	var fillConfirmationTable = function(scrapedData) {
		var elem, config, html;
		for (elem in dataConfig) {
			config = dataConfig[elem];
			if (config.formatter) {
				html = config.formatter(scrapedData[config.key]);
			} else {
				html = scrapedData[config.key];
			}
			$('#' + elem + ' td').eq(1).html(html);
		}
	};

	var downloadUrl = function(url) {
		$downloadIframe.attr('src', url);
	};

	var isValidData = function(data) {
		if (!data.control || data.control.length < 2) {
			notifier.warn('Please select 2 or more control samples');
			return false;
		}
		if (!data.experimental || data.experimental.length < 2) {
			notifier.warn('Please select 2 or more experimental samples');
			return false;
		}
		// * WARNINGS *
		// It is important to verify that the user has *tried* to select a gene before warning them.
		// $.inArray() returns -1 if the value is not found. Do not check for truthiness.
		if (geneList && data.gene && $.inArray(data.gene, geneList) === -1) {
			notifier.warn('Please input a valid gene.');
			return false;
		}
		return true;
	};

	events.on('requestFailed', function(errorData) {
		notifier.warn(errorData.message);
		resetFooter();
	});

	events.on('geneListFetched', function(geneList) {
		$('#geneList').autocomplete({
			source: function(request, response) {
				var results = $.ui.autocomplete.filter(geneList, request.term);
				response(results.slice(0, 10));
			},
			minLength: 2,
			delay: 250,
			autoFocus: true
		});
	});

	events.on('rareDiseasesFetched', function(diseaseList) {
		$('#diseaseList').autocomplete({
			source: function(request, response) {
				var results = $.ui.autocomplete.filter(diseaseList, request.term);
				response(results.slice(0, 10));
			},
			minLength: 2,
			delay: 250,
			autoFocus: true
		});
	});

	events.on('progressBar', highlightNextStep);
	events.on('dataDiffExped', setDownloadLinks);
	events.on('genesEnriched', showResults);
	
	init();

	return {
		openModalBox: openModalBox
	};
};
