
var BaseUi = function(comm, events, html, notifier, scraper) {

	var $downloadIframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body');

	var elemConfig = {
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
		}
	};
	
	var steps, $overlay, $modal, $progress, $results;

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

	events.on('dataDiffExped', function(data) {
		setDownloadLinks(data);
	});

	events.on('genesEnriched', function(data) {
		showAllResults(data);
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
		$('.g2e-editable').click(function(evt) {
			var id = $(evt.target).parent().attr('id');
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
			      comm.downloadDiffExp($modal);
			  })
			  .tooltip({
			      tooltipClass: 'g2e-tooltip'
			  })
			  .end()

			  .find('.g2e-confirm-tbl')
			  .eq(1)
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
			$('#' + elem + ' td').eq(1).html(html);
		}
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

	var showAllResults = function(enrichrLinks) {
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
		$results = $results || $('.g2e-results');		
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
			userInput = notifier.ask(config.prompt, $('#' + id + ' td').eq(1).text());
		if (userInput !== null) {
			scraper.setData(config.key, userInput);
			fillConfirmationTable(scraper.getData());
		}
	};

	var fillConfirmationTable = function(scrapedData) {
		var elem, config, html;
		for (elem in elemConfig) {
			config = elemConfig[elem];
			if (config.format) {
				html = config.format(scrapedData[config.key]);
			} else {
				html = scrapedData[config.key];
			}
			$('#' + elem + ' td').eq(1).html(html);
		}
	};

	var downloadUrl = function(url) {
		$downloadIframe.attr('src', url);
	};

	setup();

	return {
		openApp: openApp,
		initProgressBar: initProgressBar,
		highlightNextStep: highlightNextStep
	};
};
