
var Comm = function(events, notifier, SERVER) {

	var fileForDownload = [];

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
	var downloadDiffExp = function(userInput) {
		function dlgeo() {
			var endpoint = 'dlgeo?',
				qs = $.param({
					accession: userInput.accession,
					organism: userInput.organism,
					platform: userInput.platform,
					method: userInput.method,
					cell: userInput.cell,
					perturbation: userInput.perturbation,
					gene: userInput.gene
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'POST',
				success: function(data) {
				    debugger;
					if (data.status === 'error') {
						errorHandler(data);
						return;
					}
					notifier.log('GEO files were downloaded');
					notifier.log(data);
					events.fire('progressBar');
				}
			});
		}

		function diffexp(dlgeoData) {
			var endpoint = 'diffexp?',
				qs = $.param({
					// This is the SOFT file, not the gene file.
					filename: dlgeoData.filename,
					platform: userInput.platform,
					method: userInput.method,
					control: userInput.control.join('-'),
					experimental: userInput.experimental.join('-')
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'POST',
				success: function(data) {
					if (data.status === 'error') {
						errorHandler(data);
						return;
					}
					var DIR = 'static/genes/';
					notifier.log('GEO files were differentially expressed');
					notifier.log(data);
					events.fire('progressBar');
					events.fire('dataDiffExped', {
						'up': SERVER + DIR + data.up,
						'down': SERVER + DIR + data.down
					});
				}
			});
		}

		function enrichr(diffExpData) {
			var endpoint = 'enrichr?',
				qs = $.param({
					'up': diffExpData.up,
					'down': diffExpData.down,
					'combined': diffExpData.combined
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'POST',
				success: function(data) {
					if (data.status === 'error') {
						errorHandler(data);
						return;
					}
					notifier.log('Enrichr link was returned');
					notifier.log(data);
					events.fire('progressBar');
					events.fire('genesEnriched', data);
				}
			});
		}

		// Pass in noops so that we do nothing if the promise is not returned.
		dlgeo().then(diffexp, $.noop).then(enrichr, $.noop);
	};

	var fetchGeneList = function() {
		$.ajax({
			url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('geneListFetched', data);
			}
		});
	}();

	var fetchRareDiseases = function() {
 		$.ajax({
			url: SERVER + 'diseases',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('rareDiseasesFetched', data.rare_diseases);
			}
		});       
	}();

	var errorHandler = function(data) {
		events.fire('requestFailed', data);
	};

	return {
		downloadDiffExp: downloadDiffExp,
		fetchMetadata: fetchMetadata
	};
};
